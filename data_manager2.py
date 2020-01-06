import database_common


@database_common.connection_handler
def get_all_data(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ; 
                    """)
    all_data = cursor.fetchall()
    return all_data

@database_common.connection_handler
def get_some_data(cursor, select_, mytable, condition, orderby):
    cursor.execute("""
                    SELECT %(select_)s FROM %(mytable)s
                    WHERE %(condition)s
                    ORDER BY %(orderby)s;""",
                    {'select_': select_, 'mytable':mytable, 'condition':condition, 'orderby':orderby })


@database_common.connection_handler
def sort_qs_or_as(cursor, criteria):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY %s;"""% ''.join(criteria))
    sorted_data = cursor.fetchall()
    return sorted_data


#only used by delete_question in server, used to be save_updated_data
@database_common.connection_handler
def delete_data(cursor, mytable, criteria):
    cursor.execute("""
                    DELETE FROM mytable
                    WHERE criteria;""")

#not sure if this would work
@database_common.connection_handler
def get_new_id(table):
    """generates a new id for the new entries"""
    all_q_or_a = get_all_data(table)
    if all_q_or_a.id == 0:
        return 1
    else:
        return all_q_or_a.id + 1

@database_common.connection_handler
def add_new_q_or_a_to_file(cursor, mytable, column, new_value):
    cursor.execute("""
                    UPDATE mytable
                    SET column = new_value
                    WHERE condition;
                    """)
    updated_data = cursor.fetchall()
    return updated_data




