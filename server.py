from flask import Flask, render_template, request, redirect, url_for

import data_handler

app = Flask(__name__)


@app.route('/')
def route_index():
    return None


@app.route('/list')
def route_list():
    return None


@app.route('/question/<question_id>')
def route_question():
    return None


@app.route('/add-question')
def route_add_question():
    return None


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )