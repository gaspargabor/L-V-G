import data_manager2


def trystuff(question_id, answer_id):
    ultimatelista = []
    valaszlista = data_manager2.get_answers_for_question(question_id)
    print('valaszlista')
    print(valaszlista)
    for kerdes in valaszlista:
        kerdeslista = []
        kommentek = data_manager2.get_comments_for_answer(kerdes['id'])
        print(kommentek)
        kerdeslista.append(kerdes)
        kerdeslista.append(kommentek)
        ultimatelista.append(kerdeslista)
        print('kerdeslista')
        print(kerdeslista)
    print('ultimatelista')
    print(ultimatelista)
    return ultimatelista


trystuff(1, 1)