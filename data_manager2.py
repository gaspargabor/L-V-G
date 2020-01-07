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

@database_common.connection_handler
def get_answers_for_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id=%(question_id)s;
                    """,
                   {'question_id': question_id})
    answers=cursor.fetchall()
    return answers

@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id=%(question_id)s;
                    """,
                   {'question_id': question_id})
    question = cursor.fetchall()
    return question

#only used by delete_question in server, used to be save_updated_data
@database_common.connection_handler
def delete_data(cursor, mytable, criteria):
    cursor.execute("""
                    DELETE FROM %(mytable)s
                    WHERE %(criteria)s;""",
                   {'mytable': mytable, 'criteria': criteria})

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

@database_common.connection_handler
def add_one_to_view_number(cursor, question_id):
    cursor.execute("""
                    UPDATE question
                    SET view_number = view_number+1
                    WHERE id=%s;
                    """% ''.join(question_id),
                   {'question_id': question_id})

@database_common.connection_handler
def search(cursor, question):
    search_phrase = "%" + question + "%"
    cursor.execute("""
                    SELECT * FROM question
                    WHERE title ILIKE %(search_phrase)s;
                    """,
                   {'search_phrase': search_phrase}
                   )
    search_result = cursor.fetchall()
    return search_result



