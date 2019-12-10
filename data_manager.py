import csv
import os

"""Layer between the server and the data. Functions here should be called from the server.py and these should use generic functions from the connection.py"""


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


def get_question(filename, question_id):
    return get_data_from_csv(filename, question_id)


def add_new_question(question):
    question['id'] = get_new_id(filename='question.csv')
    question['submission_time'] = 'get time'

    add_new_q_or_a_to_file('question.csv', question, True)


def add_new_q_or_a_to_file(filename, q_or_a, append=True):
    qs_or_as = get_data_from_csv(filename)
    fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in qs_or_as:
            if not append:
                if row['id'] == q_or_a['id']:
                    row = q_or_a
            writer.writerow(row)
        if append:
            writer.writerow(q_or_a)
