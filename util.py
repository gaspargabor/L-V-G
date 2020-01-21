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
    print(all_data)
    return all_data



def make_searching_great_again(q):
    print('run')
    only_title = data_manager2.search_question(q)
    print(len(only_title))
    only_message = data_manager2.search_question_message(q)
    print(len(only_message))
    title_and_message = []
    if len(only_message) > len(only_title):
        for message in only_message:
            print(message)
            print(only_title)
            for title in only_title:
                if message['id'] == title['id']:
                    title_and_message.append(title)
    else:
        for title in only_title:
            for message in only_message:
                if message['id'] == title['id']:
                    title_and_message.append(title)
        print(title_and_message)
    return title_and_message


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)