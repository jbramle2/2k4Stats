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

def get_player_stats(player):
    query = ("SELECT * "
             "FROM utstatsdb_views.player_ppr "
             "WHERE player_name = '" + str(player) + "'"
             )

    player_stats = conn.ssh_query(query)

    return player_stats

def get_player_avg_10(player):
    query = ("SELECT * "
             "FROM utstatsdb_views.player_averages_10 "
             "WHERE p_name = '" + str(player) + "'" + " ORDER BY p_num DESC"

             )

    player_stats = conn.ssh_query(query)

    return player_stats