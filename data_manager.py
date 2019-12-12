import csv
import time
import os
question_route = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "sample_data/question.csv"))
answer_route = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "sample_data/answer.csv"))
Q_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
A_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_data_from_csv(filename, question_id=None):
    qs_or_as = []
    with open(filename, newline='') as data_file:
        reader = csv.DictReader(data_file)
        for row in reader:
            q_or_a = dict(row)
            if question_id is not None and question_id == q_or_a['id']:
                return q_or_a
            qs_or_as.append(q_or_a)
    return qs_or_as

def get_data_answ_from_csv(filename, question_id):
    qs_or_as = []
    with open(filename, newline='') as data_file:
        reader = csv.DictReader(data_file)
        for row in reader:
            q_or_a = dict(row)
            if question_id == q_or_a['question_id']:
                qs_or_as.append(q_or_a)
    return qs_or_as


def get_answer(answer_id=None):
    with open(answer_route, newline='') as data_file:
        reader = csv.DictReader(data_file)
        for row in reader:
            answer = dict(row)
            if answer_id == answer['id']:
                return answer


def get_new_id(filename):
    all_q_or_a = get_data_from_csv(filename)
    if len(all_q_or_a) == 0:
        return 1

    return str(int(all_q_or_a[-1]['id'])+1)


def get_question(filename, question_id):
    return get_data_from_csv(filename, question_id)


def get_answers_for_question(filename, question_id):
    answers = []
    all_answers = get_data_from_csv(filename)
    for answer in all_answers:
        if question_id == answer['question_id']:
            answers.append(answer)
    return answers


def add_new_question(question):
    question['id'] = get_new_id(filename=question_route)
    question['submission_time'] = int(time.time())

    add_new_q_or_a_to_file(question_route, Q_HEADER, question, True)


def edit_question(question):
    add_new_q_or_a_to_file(question_route, Q_HEADER, question, False)


def edit_answer(answer):
    add_new_q_or_a_to_file(answer_route, A_HEADER, answer, False)


def add_new_answer(answer, question_id):
    answer['id'] = get_new_id(filename=answer_route)
    answer['submission_time'] = int(time.time())
    answer['question_id'] = question_id

    add_new_q_or_a_to_file(answer_route, A_HEADER, answer, True)


def add_new_q_or_a_to_file(filename, header, q_or_a, append=True):
    qs_or_as = get_data_from_csv(filename)
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writeheader()
        for row in qs_or_as:
            if not append:
                if row['id'] == q_or_a['id']:
                    row = q_or_a
            writer.writerow(row)
        if append:
            writer.writerow(q_or_a)


def sort_qs_or_as(list_to_sort, reverse, criteria):
    sorted_list = sorted(list_to_sort, key=lambda i: i[criteria], reverse=reverse)
    return sorted_list

def delete_question(filename, question, question_id):
    questions = get_data_from_csv(filename, question_id)
    for question in questions:
        print(questions)
        print(question)
        print(question_id)
        print(question['id'])
        if question_id == int(question['id']):
            questions.remove(question)



