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
def add_new_question(cursor, submission_time, view_number, vote_number, title, message, image):
    cursor.execute("""
                    INSERT INTO question
                    (submission_time, view_number, vote_number, title, message, image)
                    VALUES(%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s)
                    """, {'submission_time': submission_time, 'view_number': view_number, 'vote_number': vote_number, 'title': title, 'message': message, 'image': image})
    return None




