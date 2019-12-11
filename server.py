from flask import Flask, render_template, request, redirect, url_for
import os
import data_manager

app = Flask(__name__)
GET_COUNTER = 0
question_route = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "question.csv"))
answer_route = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__), "answer.csv"))
"""Flask stuff (server, routes, request handling, session, etc.)
This layer should consist of logic that is related to Flask. (with other words: this should be the only file importing 
from flask)"""


@app.route('/')
@app.route('/list')
def route_index(sort_criteria='submission_time'):
    questions = data_manager.get_data_from_csv(question_route)
    questions = data_manager.sort_qs_or_as(questions, True, sort_criteria)
    return render_template('layout.html', questions=questions)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def route_question(question_id):
    if request.method == 'POST':
        return redirect('/')
    if request.method == 'GET':
        route_view_counter(question_id)
        question = data_manager.get_data_from_csv(question_route, question_id=question_id)
        answers = data_manager.get_answers_for_question(answer_route, question_id)
        return render_template('display_question.html',
                               question_id=question['id'],
                               question=question,
                               answers=answers
                               )


@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    if request.method == 'POST':
        question = {
            'title': request.form.get('title'),
            'message': request.form.get('message'),
            'image': request.form.get('image'),
            'view_number': 0
        }
        data_manager.add_new_question(question)
        return redirect('/')
    return render_template('addquestion.html')


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_new_answer(question_id):
    if request.method == 'POST':
        answer = {
            'id': '<question_id>',
            "message": request.form.get('message'),
            "image": request.form.get('image')
        }
        data_manager.add_new_answer(answer, question_id)
        question = data_manager.get_data_from_csv(question_route, question_id)
        answers = data_manager.get_answers_for_question(answer_route, question_id)
        print(answers)
        return render_template('display_question.html', question_id=question_id, question=question, answers=answers)
    return render_template('addanswer.html', question_id=question_id)


def route_view_counter(question_id):
    question = data_manager.get_question(question_route, question_id)
    question['view_number'] = str(int(question['view_number']) + 1)
    data_manager.edit_question(question)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )