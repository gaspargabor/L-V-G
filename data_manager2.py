from datetime import datetime

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
                    ORDER BY %s;""" % (criteria))
    sorted_data = cursor.fetchall()
    return sorted_data


@database_common.connection_handler
def sort_as_by_q_id(cursor, question_id,criteria):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id=%(question_id)s
                    ORDER BY %s;""" % criteria,
                   {'question_id': question_id})
    sorted_answers = cursor.fetchall()
    return sorted_answers


@database_common.connection_handler
def get_answers_for_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE answer.question_id=%(question_id)s
                    ORDER BY vote_number DESC;
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
def update_question_by_id(cursor, question_id, submission_time, message):
    cursor.execute("""
                    UPDATE question
                    SET submission_time = %(submission_time)s, message = %(message)s
                    WHERE id = %(question_id)s;
                    """, { 'submission_time': submission_time, 'message': message , 'question_id': question_id})


@database_common.connection_handler
def get_answer_by_id(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id=%(answer_id)s;
                    """, {'answer_id': answer_id})
    answer = cursor.fetchone()
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
def add_new_question(cursor, title, message, image, user_id):
    submission_time = datetime.now()
    view_number = 0
    vote_number = 0
    cursor.execute("""
                    INSERT INTO question
                    (submission_time, view_number, vote_number, title, message, image, user_id)
                    VALUES(%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s, %(user_id)s)
                    """, {'submission_time': submission_time, 'view_number': view_number, 'vote_number': vote_number, 'title': title, 'message': message, 'image': image, 'user_id': user_id})
    return None

@database_common.connection_handler
def add_new_answer(cursor, submission_time, vote_number, question_id, message, image, user_id):
    cursor.execute("""
                    INSERT INTO answer
                    (submission_time, vote_number, question_id, message, image, user_id)
                    VALUES(%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s, %(user_id)s)
                    """, {'submission_time': submission_time, 'vote_number': vote_number, 'question_id': question_id, 'message': message, 'image': image, 'user_id': user_id})
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
def get_comment_by_id(cursor, comment_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE id=%(comment_id)s;
                    """, {'comment_id': comment_id})
    answer = cursor.fetchall()
    return answer


@database_common.connection_handler
def update_comment_by_id(cursor, comment_id, submission_time, message, edited_count):
    cursor.execute("""
                    UPDATE comment
                    SET submission_time = %(submission_time)s, message = %(message)s, edited_count = %(edited_count)s
                    WHERE id = %(comment_id)s;
                    """, {'submission_time': submission_time, 'message': message , 'comment_id': comment_id, 'edited_count': edited_count})


@database_common.connection_handler
def add_comment_for_question(cursor, submission_time, message, edited_count, question_id, answer_id, user_id):
    cursor.execute("""
                    INSERT INTO comment
                    (submission_time, edited_count, question_id, answer_id, message, user_id)
                    VALUES(%(submission_time)s, %(edited_count)s, %(question_id)s, %(answer_id)s, %(message)s, %(user_id)s)
                    """, {'submission_time': submission_time, 'edited_count': edited_count, 'question_id': question_id, 'answer_id': answer_id, 'message': message, 'user_id': user_id})


@database_common.connection_handler
def update_question_votenum_by_id(cursor, question_id, vote_number):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = %(vote_number)s
                    WHERE id = %(question_id)s;
                    """, {'vote_number': vote_number, 'question_id': question_id})

@database_common.connection_handler
def update_answer_votenum_by_id(cursor, answer_id, vote_number):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = %(vote_number)s
                    WHERE id = %(answer_id)s;
                    """, {'vote_number': vote_number, 'answer_id': answer_id})


@database_common.connection_handler
def delete_answer_by_question_id(cursor, question_id):
    cursor.execute("""
                    DELETE FROM answer
                    WHERE question_id = %(question_id)s
                    """, {'question_id': question_id})


@database_common.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(question_id)s
                    """, {'question_id': question_id})


@database_common.connection_handler
def delete_comment_by_question_id(cursor, question_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE question_id = %(question_id)s
                    """, {'question_id': question_id})


@database_common.connection_handler
def delete_question_tag_by_question_id(cursor, question_id):
    cursor.execute("""
                    DELETE FROM question_tag
                    WHERE question_id = %(question_id)s
                    """, {'question_id': question_id})


@database_common.connection_handler
def delete_answer_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    DELETE FROM answer
                    WHERE id = %(answer_id)s
                    """, {'answer_id': answer_id})


@database_common.connection_handler
def delete_comment_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE answer_id = %(answer_id)s
                    """, {'answer_id': answer_id})


@database_common.connection_handler
def delete_comment_by_comment_id(cursor, comment_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE id = %(comment_id)s
                    """, {'comment_id': comment_id})


@database_common.connection_handler
def add_comment_for_answer(cursor, submission_time, message, edited_count, answer_id, user_id):
    cursor.execute("""
                    INSERT INTO comment
                    (submission_time, edited_count, answer_id, message, user_id)
                    VALUES(%(submission_time)s, %(edited_count)s, %(answer_id)s, %(message)s, %(user_id)s)
                    """, {'submission_time': submission_time, 'edited_count': edited_count, 'answer_id': answer_id, 'message': message, 'user_id': user_id})


@database_common.connection_handler
def update_question_viewnumber_by_id(cursor, question_id, view_number):
    cursor.execute("""
                    UPDATE question
                    SET view_number = %(view_number)s
                    WHERE id = %(question_id)s;
                    """, {'view_number': view_number, 'question_id': question_id})


@database_common.connection_handler
def update_question_asd_by_id(cursor, question_id, view_number):
    cursor.execute("""
                    UPDATE question
                    SET view_number = %(view_number)s
                    WHERE id = %(question_id)s;
                    """, {'view_number': view_number, 'question_id': question_id})



    #TESTING STUFFgfxfycgjhbnjlkgvcty



@database_common.connection_handler
def get_joined(cursor, question_id):
    cursor.execute("""
                    SELECT title, question.id FROM question inner join answer a on question.id = a.question_id
                    WHERE question.id=%(question_id)s AND a.message IS NOT NULL;""",
                   {'question_id': question_id})
    joined = cursor.fetchall()
    return joined

@database_common.connection_handler
def search_question2(cursor, question):
    cursor.execute("""
                    SELECT question.id, title, question.message, COALESCE(a.message, 'No answers yet') as ans FROM question left join answer a on question.id = a.question_id 
                    WHERE (title ILIKE %(search_phrase)s  AND question.message ILIKE %(search_phrase)s AND a.message ILIKE %(search_phrase)s)
                    OR (title ILIKE %(search_phrase)s  AND question.message ILIKE %(search_phrase)s AND a.message NOT ILIKE %(search_phrase)s)
                    OR (title ILIKE %(search_phrase)s  AND question.message NOT ILIKE %(search_phrase)s AND a.message ILIKE %(search_phrase)s)
                    OR (title ILIKE %(search_phrase)s  AND question.message NOT ILIKE %(search_phrase)s AND a.message NOT ILIKE %(search_phrase)s)
                    OR (title NOT ILIKE %(search_phrase)s  AND question.message ILIKE %(search_phrase)s AND a.message ILIKE %(search_phrase)s)
                    OR (title NOT ILIKE %(search_phrase)s  AND question.message NOT ILIKE %(search_phrase)s AND a.message ILIKE %(search_phrase)s)
                    OR (title NOT ILIKE %(search_phrase)s  AND question.message ILIKE %(search_phrase)s AND a.message NOT ILIKE %(search_phrase)s)
                    OR (title ILIKE %(search_phrase)s  AND question.message ILIKE %(search_phrase)s)
                    OR (title ILIKE %(search_phrase)s AND question.message NOT ILIKE %(search_phrase)s)
                    OR (title NOT ILIKE %(search_phrase)s AND question.message ILIKE %(search_phrase)s)
                    GROUP BY question.id, a.message, title, question.message
                    ;
                    """,
                   {'search_phrase': ("%" + question + "%")}
                   )
    search_result = cursor.fetchall()
    return search_result


@database_common.connection_handler
def get_ansver_id_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT id FROM answer
                    WHERE answer.question_id = %(question_id)s
                    """,
                   {'question_id': question_id})
    ids = cursor.fetchall()
    return ids


@database_common.connection_handler
def delete_comment_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    DELETE FROM comment
                    WHERE answer_id = %(answer_id)s
                    """, {'answer_id': answer_id})


@database_common.connection_handler
def check_if_username_exists(cursor, username):
    cursor.execute("""
                    SELECT user_name from users
                    WHERE user_name = %(username)s;""",
                   {'username': username})
    user = cursor.fetchall()
    return user

@database_common.connection_handler
def get_user_data(cursor, username):
    cursor.execute("""
                    SELECT * FROM users
                    WHERE user_name = %(username)s;
                    """, {'username':username })
    user_data = cursor.fetchall()
    return user_data

@database_common.connection_handler
def get_users_questions_by_userid(cursor, userid):
    cursor.execute("""
                    SELECT * FROM ask_mate2.public.question
                    WHERE user_id=%(userid)s;""",
                   {'userid' : userid})
    users_questions = cursor.fetchall()
    return users_questions


@database_common.connection_handler
def get_user_id_by_session_id(cursor, session_id):
    cursor.execute("""
                    SELECT user_id FROM sessions
                    WHERE session_id = %(session_id)s
                    """,
                   {'session_id': session_id})
    user_id = cursor.fetchall()
    return user_id
@database_common.connection_handler
def save_registered_data(cursor, username, password):
    registration_time = datetime.now()
    cursor.execute("""
                    INSERT INTO users
                    (user_name, password, registration_time)
                     VALUES(%(username)s, %(password)s, %(registration_time)s) """,
                   {'username':username, 'password': password, 'registration_time': registration_time})

@database_common.connection_handler
def get_user_id(cursor, username):
    cursor.execute("""
                    SELECT id from users
                    WHERE user_name=%(username)s""",
                   {'username': username})
    userid=cursor.fetchone()
    return userid

@database_common.connection_handler
def save_registered_data_to_session(cursor, session_id, username, userid):
    session_start_time = datetime.now()
    cursor.execute("""
                    INSERT INTO sessions
                    (session_id, user_name, user_id, session_start_time)
                    VALUES(%(session_id)s, %(username)s, %(userid)s, %(session_start_time)s)""",
                   {'session_id': session_id, 'username': username, 'userid': userid, 'session_start_time': session_start_time})


@database_common.connection_handler
def get_password_for_username(cursor, username):
    cursor.execute("""
                    SELECT password FROM users
                    where user_name=%(username)s""",
                   {'username': username})
    password = cursor.fetchone()
    return password

@database_common.connection_handler
def get_user_by_id(cursor, userid):
    cursor.execute("""
                    SELECT * FROM users
                    WHERE id=%s""" % ''.join(userid),
                   {'userid': userid})
    username = cursor.fetchall()
    return username
