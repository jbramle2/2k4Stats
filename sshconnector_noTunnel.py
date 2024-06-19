import MySQLdb

file = open('credentials.txt')
creds = file.readlines()

for x in range(len(creds)):
    creds[x] = creds[x].rstrip("\n")

db_server_ip = creds[8]
db_server_port = int(creds[9])
db_user = creds[10]
db_user_password = creds[11]
db_name = creds[12]


def ssh_query(query):
    conn = MySQLdb.connect(host=db_server_ip,
                           port=db_server_port,
                           user=db_user,
                           passwd=db_user_password,
                           db=db_name)
    c = conn.cursor()

    c.execute(query)

    results = c.fetchone()

    return results


def ssh_query_multi(query):
    conn = MySQLdb.connect(host=db_server_ip,
                           port=db_server_port,
                           user=db_user,
                           passwd=db_user_password,
                           db=db_name)
    c = conn.cursor()

    c.execute(query)

    results = c.fetchall()

    return results
