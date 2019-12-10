import csv
import time

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


def get_new_id(filename):
    all_q_or_a = get_data_from_csv(filename)
    if len(all_q_or_a) == 0:
        return 1

    return str(int(all_q_or_a[-1]['id'])+1)


def get_question(filename, as_question_id):
    return get_data_from_csv(filename, as_question_id)


def get_answers_for_question(filename, question_id):
    answers = []
    all_answers = get_data_from_csv(filename)
    for answer in all_answers:
        if question_id == answer['question_id']:
            answers.append(answer)
    return answers


def add_new_question(question):
    question['id'] = get_new_id(filename='question.csv')
    question['submission_time'] = int(time.time())

    add_new_q_or_a_to_file('question.csv', Q_HEADER, question, True)


def add_new_answer(answer, question_id):
    answer['id'] = get_new_id(filename='answer.csv')
    answer['submission_time'] = int(time.time())
    answer['question_id'] = question_id

    add_new_q_or_a_to_file('answer.csv', A_HEADER, answer, True)


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

