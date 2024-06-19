import SSHConnector as conn

def get_match_num(back):
    query = ("SELECT match_num "
             "FROM utstatsdb_views.match_ppr_w_bad "
             "GROUP BY match_num "
             "ORDER BY match_num "
             "DESC LIMIT " + str(back) + ",1")

    previous_match = conn.ssh_query_multi(query)

    return previous_match[0][0]

def get_match_info(natch_num):
    query = ("SELECT * "
             "FROM utstatsdb_views.match_ppr_w_bad "
             "WHERE match_num = " + str(natch_num)
             )

    match_info = conn.ssh_query_multi(query)

    return match_info
