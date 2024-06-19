import MySQLdb
from sshtunnel import SSHTunnelForwarder

file = open('credentials.txt')
creds = file.readlines()

for x in range(len(creds)):
    creds[x] = creds[x].rstrip("\n")

##########################################
ssh_ip_address = creds[1]
ssh_p_username = creds[2]
ssh_p_password = creds[3]
ssh_port = int(creds[4])
###########################################
ssh_remote_bind_address = creds[7]
db_server_ip = creds[8]
db_server_port = int(creds[9])
db_user = creds[10]
db_user_password = creds[11]
db_name = creds[12]

tunneled_host = '127.0.0.1'
###########################################


def ssh_query(query):
    with SSHTunnelForwarder(
            (ssh_ip_address, ssh_port),
            ssh_password=ssh_p_password,
            ssh_username=ssh_p_username,
            remote_bind_address=(db_server_ip, db_server_port)) as server:
        conn = MySQLdb.connect(host=tunneled_host,
                               port=server.local_bind_port,
                               user=db_user,
                               passwd=db_user_password,
                               db=db_name)
        c = conn.cursor()

        c.execute(query)

        results = c.fetchone()

        return results


def ssh_query_multi(query):
    with SSHTunnelForwarder(
            (ssh_ip_address, ssh_port),
            ssh_password=ssh_p_password,
            ssh_username=ssh_p_username,
            remote_bind_address=(db_server_ip, db_server_port)) as server:
        conn = MySQLdb.connect(host=tunneled_host,
                               port=server.local_bind_port,
                               user=db_user,
                               passwd=db_user_password,
                               db=db_name)
        c = conn.cursor()

        c.execute(query)

        results = c.fetchall()

        return results
