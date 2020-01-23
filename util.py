import bcrypt

import data_manager2



def trystuff(question_id, answer_id):
    ultimatelista = []
    valaszlista = data_manager2.get_answers_for_question(question_id)
    for kerdes in valaszlista:
        kerdeslista = []
        kommentek = data_manager2.get_comments_for_answer(kerdes['id'])
        kerdeslista.append(kerdes)
        kerdeslista.append(kommentek)
        ultimatelista.append(kerdeslista)

    return ultimatelista



def get_all_question_data_for_display(question_id):
    all_data = []
    q_n_comm = []
    q_n_comm.append(data_manager2.get_question_by_id(question_id))
    q_n_comm.append(data_manager2.get_comments_for_question(question_id))
    all_ans = data_manager2.get_answers_for_question(question_id)
    all_data.append(q_n_comm)
    for kerdes in all_ans:
        a_n_comm = []
        comm_for_a = data_manager2.get_comments_for_answer(kerdes['id'])
        a_n_comm.append(kerdes)
        a_n_comm.append(comm_for_a)
        all_data.append(a_n_comm)
    return all_data




def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def check_user_in_use(username):
    usedornot = data_manager2.check_user_in_use(username)
    if usedornot:
        return True
    else:
        return False
