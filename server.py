from flask import Flask, render_template, request, redirect, url_for

import data_manager

app = Flask(__name__)

"""Flask stuff (server, routes, request handling, session, etc.)
This layer should consist of logic that is related to Flask. (with other words: this should be the only file importing 
from flask)"""


@app.route('/')
@app.route('/list')
def route_index():
    return render_template('layout.html')


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def route_question(question_id):
    if request.method == 'POST':
        if request.form.get('id') != question_id:
            raise ValueError('The received id is not valid!')

        question = {
            'id': question_id,
            'title': request.form.get('title')
        }
        data_manager.update_user_story(question)
        return redirect('/')


@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    if request.method == 'POST':
        question = {
            'title': request.form.get('title'),
            'message': request.form.get('message'),
        }
        print('call add new q')
        data_manager.add_new_question(question)
        return redirect('/')
    return render_template('addquestion.html')


@app.route('/question/<question_id>/new-answer')
def route_edit_answer():
    return None


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )