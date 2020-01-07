from flask import Flask, render_template, request, redirect, url_for
import os
import data_manager2
import data_manager
from datetime import datetime

app = Flask(__name__)
question_route = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "sample_data/question.csv"))
answer_route = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "sample_data/answer.csv"))
Q_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
A_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
"""Flask stuff (server, routes, request handling, session, etc.)
This layer should consist of logic that is related to Flask. (with other words: this should be the only file importing 
from flask)"""


#@app.route('/')
#def route_index(sort_criteria=None):
#    sort_criteria = request.args.get('sort_criteria')
#    if sort_criteria is None:
#        sort_criteria = 'submission_time'
#    questions = data_manager2.sort_qs_or_as(sort_criteria)
#    return render_template('layout.html', questions=questions)


@app.route('/', methods=['POST', 'GET'])
def route_index():
    if request.method == "GET":
        questions = data_manager2.get_5_latest()
        return render_template('layout.html', questions=questions)
    elif request.method == "POST":
        return redirect('/list')


@app.route('/list')
def route_all_question(sort_criteria=None):
    sort_criteria = request.args.get('sort_criteria')
    if sort_criteria is None:
        sort_criteria = 'submission_time'
    questions = data_manager2.sort_qs_or_as(sort_criteria)
    return render_template('list.html', questions=questions)


"""@app.route('/')
@app.route('/list')
def route_index(sort_criteria=None):
    sort_criteria = request.args.get('sort_criteria')
    if sort_criteria is None:
        sort_criteria = 'submission_time'
    questions = data_manager.get_data(question_route)
    questions = data_manager.sort_qs_or_as(questions, sort_criteria)
    return render_template('layout.html', questions=questions)"""


@app.route('/question/<question_id>/delete', methods=['DELETE', 'POST', 'GET'])
def delete_question(question_id):
    updated_q_data = data_manager.delete_question(question_route, question_id)
    data_manager.save_updated_data(question_route, Q_HEADER, updated_q_data)
    updated_a_data = data_manager.delete_answers_for_question(answer_route, question_id)
    data_manager.save_updated_data(answer_route, A_HEADER, updated_a_data)
    return redirect('/list')


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def route_question(question_id):
    if request.method == 'POST':
        return redirect('/')
    if request.method == 'GET':
        route_view_counter(question_id)
        question = data_manager2.get_question_by_id(question_id)
        print(question)
        answers = data_manager2.get_answers_for_question(question_id)
        return render_template('display_question.html',
                               question_id=question_id,
                               question=question,
                               answers=answers
                               )

""""@app.route('/question/<question_id>', methods=['GET', 'POST'])
def route_question(question_id):
    if request.method == 'POST':
        return redirect('/')
    if request.method == 'GET':
        route_view_counter(question_id)
        question = data_manager.get_data(question_route, question_id)
        answers = data_manager.get_answers_for_question(answer_route, question_id)
        return render_template('display_question.html',
                               question_id=question['id'],
                               question=question,
                               answers=answers
                               )"""


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def route_edit_question(question_id):
    if request.method == 'GET':
        question_original = data_manager.get_data(question_route, question_id)
        return render_template('edit-question.html', question_id=question_id, question_original=question_original)
    if request.method == 'POST':
        question_original = data_manager.get_data(question_route, question_id)
        question = {
            'id': question_id,
            'submission_time': question_original['submission_time'],
            'title': request.form.get('title'),
            'message': request.form.get('message'),
            'image': request.form.get('image'),
            'view_number': question_original['view_number'],
            'vote_number': question_original['view_number']
        }
        data_manager.edit_question(question)
        return redirect('/')


@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    if request.method == 'POST':
        submission_time = datetime.now(),
        title = request.form.get('title'),
        message = request.form.get('message'),
        image = request.form.get('image'),
        view_number = 0,
        vote_number = 0
        data_manager2.add_new_question(submission_time, view_number, vote_number, title, message, image)
        return redirect('/')
    return render_template('addquestion.html')


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_new_answer(question_id):
    if request.method == 'POST':
        answer = {
            'id': '<question_id>',
            "message": request.form.get('message'),
            "image": request.form.get('image'),
            "vote_number": 0
        }
        data_manager.add_new_answer(answer, question_id)
        question = data_manager.get_data(question_route, question_id)
        answers = data_manager.get_answers_for_question(answer_route, question_id)
        return render_template('display_question.html', question_id=question_id, question=question, answers=answers)
    return render_template('addanswer.html', question_id=question_id)


def route_view_counter(question_id):
    data_manager2.get_question_by_id(question_id)
    data_manager2.add_one_to_view_number(question_id)


"""def route_view_counter(question_id):
    question = data_manager2.get_question_by_id(question_id)
    question['view_number'] = str(int(question['view_number']) + 1)
    data_manager2.edit_question(question)"""


@app.route('/addvote-question')
def addvote_question(question_id=None):
    question_id = request.args.get('question_id')
    question = data_manager.get_data(question_route, question_id)
    answers = data_manager.get_answers_for_question(answer_route, question_id)
    question['vote_number'] = str(int(question['vote_number']) + 1)
    data_manager.edit_question(question)
    return render_template('display_question.html',
                           question_id=question['id'],
                           question=question,
                           answers=answers)


@app.route('/addvote_answer')
def addvote_answer(answer_id=None, question_id=None):
    answer_id = request.args.get('answer_id')
    question_id = request.args.get('question_id')
    question = data_manager.get_data(question_route, question_id)
    answers = data_manager.get_answers_for_question(answer_route, question_id)
    for answer in answers:
        if answer['id'] == answer_id:
            answer['vote_number'] = str(int(answer['vote_number']) + 1)
    data_manager.edit_answer(answer)
    return render_template('display_question.html',
                           question_id=question['id'],
                           question=question,
                           answers=answers)

@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    if request.method == 'POST':
        submission_time = datetime.now(),
        title = request.form.get('title'),
        message = request.form.get('message'),
        image = request.form.get('image'),
        view_number = 0,
        vote_number = 0
        data_manager2.add_new_question(submission_time, view_number, vote_number, title, message, image)
        return redirect('/')
    return render_template('addquestion.html')


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def addcomment_question(question_id):
    if request.method == "GET":
        return render_template('addcomment.html')
    elif request.method == "POST":
        submission_time = datetime.now(),
        message = request.form.get("message"),
        edited_count = 0,
        question_id = question_id,
        answer_id = None
        return render_template('display_question/<question_id,',
                               question_id=question_id,
                               answer=answer,)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )