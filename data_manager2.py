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
def get_5_latest(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY "submission_time" DESC
                    LIMIT 5;""")
    latest_5 = cursor.fetchall()
    return latest_5


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
                    WHERE answer.question_id=%(question_id)s;
                    """,
                   {'question_id': question_id})
    answers=cursor.fetchall()
    return answers


@database_common.connection_handler
def get_comments_for_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE comment.question_id=%(question_id)s;
                    """,
                   {'question_id': question_id})
    comments_for_q = cursor.fetchall()
    return comments_for_q


@database_common.connection_handler
def get_comments_for_answer(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE comment.answer_id=%(answer_id)s;
                    """,
                   {'answer_id': answer_id})
    comments_for_a = cursor.fetchall()
    return comments_for_a


@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id=%(question_id)s;
                    """,
                   {'question_id': question_id})
    question = cursor.fetchall()
    return question


@database_common.connection_handler
def get_answer_by_id(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id=%(answer_id)s;
                    """, {'answer_id': answer_id})
    answer = cursor.fetchall()
    return answer


@database_common.connection_handler
def update_answer_by_id(cursor, answer_id, submission_time, message):
    cursor.execute("""
                    UPDATE answer
                    SET submission_time = %(submission_time)s, message = %(message)s
                    WHERE id = %(answer_id)s;
                    """, { 'submission_time': submission_time, 'message': message , 'answer_id': answer_id})


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
def add_new_answer(cursor, submission_time, vote_number, question_id, message, image):
    cursor.execute("""
                    INSERT INTO answer
                    (submission_time, vote_number, question_id, message, image)
                    VALUES(%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s)
                    """, {'submission_time': submission_time, 'vote_number': vote_number, 'question_id': question_id, 'message': message, 'image': image})
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


@database_common.connection_handler
def get_comment_by_id(cursor, comment_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE id=%(comment_id)s;
                    """, {'comment_id': comment_id})
    answer = cursor.fetchall()
    return answer


@database_common.connection_handler
def update_comment_by_id(cursor, comment_id, submission_time, message):
    cursor.execute("""
                    UPDATE comment
                    SET submission_time = %(submission_time)s, message = %(message)s
                    WHERE id = %(comment_id)s;
                    """, {'submission_time': submission_time, 'message': message , 'comment_id': comment_id})


@database_common.connection_handler
def add_comment_for_question(cursor, submission_time, message, edited_count, question_id, answer_id):
    cursor.execute("""
                    INSERT INTO comment
                    (submission_time, edited_count, question_id, answer_id, message)
                    VALUES(%(submission_time)s, %(edited_count)s, %(question_id)s, %(answer_id)s, %(message)s)
                    """, {'submission_time': submission_time, 'edited_count': edited_count, 'question_id': question_id, 'answer_id': answer_id, 'message': message})


@database_common.connection_handler
def update_question_by_id(cursor, question_id, vote_number):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = %(vote_number)s
                    WHERE id = %(question_id)s;
                    """, {'vote_number': vote_number, 'question_id': question_id})

@database_common.connection_handler
def update_answer_by_id2(cursor, answer_id, vote_number):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = %(vote_number)s
                    WHERE id = %(answer_id)s;
                    """, {'vote_number': vote_number, 'answer_id': answer_id})


@database_common.connection_handler
def delete_answer_by_question_id(cursor, question_id):
    cursor.execute("""
                """)
