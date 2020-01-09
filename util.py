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


def make_searching_great_again(q):
    only_title = data_manager2.search_question(q)
    only_message = data_manager2.search_question_message(q)
    title_and_message = []
    if len(only_message) > len(only_title):
        for message in only_message:
            for title in only_title:
                if message['id'] == title['id']:
                    title_and_message.append(title)
    else:
        for title in only_title:
            a = title
    pass