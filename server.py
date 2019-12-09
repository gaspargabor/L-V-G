from flask import Flask, render_template, request, redirect, url_for

import data_handler

app = Flask(__name__)


"""Flask stuff (server, routes, request handling, session, etc.)
This layer should consist of logic that is related to Flask. (with other words: this should be the only file importing from flask)"""


@app.route('/')
@app.route('/list')
def route_index():
    return None


@app.route('/question/<question_id>')
def route_question():
    return None


@app.route('/add-question')
def route_add_question():
    return None


@app.route('/question/<question_id>/new-answer')
def route_edit_answer():
    return None


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )