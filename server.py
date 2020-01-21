import uuid

from flask import Flask, render_template, request, redirect, url_for, session, escape, make_response
import data_manager2
from datetime import datetime
import util
import os, string


super_secret_key = os.urandom(8)

app = Flask(__name__)

app.secret_key = b'\xe9\xac)\x88\xc9r\x84c\xd9n\xf3n(H\xdb\x13'


@app.route('/', methods=['POST', 'GET'])
def route_index():
    if request.method == "GET":
        if 'username' in session:
            logged_in = 'Logged in as %s' % escape(session['username'])
        logged_in = 'You are not logged in'
        questions = data_manager2.get_5_latest()
        print(session)
        return render_template('layout.html', questions=questions, logged_in=logged_in)
    elif request.method == "POST":
        return redirect('/list')



@app.route('/login', methods=['GET', 'POST'])
def route_login():
    print(session)
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        valid = util.verify_password(session['password'], '$2b$12$Gj9WEZBHrDIHqjvHTh0R3.r.E3ZOqtZ5Llelfp4zRi0754hBEhpyq')
        print(session)
        print(valid)
        return redirect('/')
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/registration', methods=['GET', 'POST'])
def route_registration():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = util.hash_password(request.form['password'])
        session['_id'] = uuid.uuid4()
        print(session['username'], session['password'])
        print(session['_id'])
        return redirect('/')
    return'''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=text name=password>
            <p><input type=submit value=Register>
        </form>
    '''


@app.route('/list')
def route_all_question(sort_criteria=None, ascordesc=None):
    sort_criteria = request.args.get('sort_criteria')
    ascordesc = request.args.get('ascordesc')
    if sort_criteria is None:
        sort_criteria = 'submission_time'
        ascordesc = 'ASC'
    crit = [sort_criteria, ascordesc]
    criteria = ' '.join(crit)
    questions = data_manager2.sort_qs_or_as(criteria)
    return render_template('list.html', questions=questions)


@app.route('/question/<question_id>')
def route_question(question_id):
    question = data_manager2.get_question_by_id(question_id)
    answers = data_manager2.get_answers_for_question(question_id)
    answer_id = None
    if len(answers) != 0:
        answer_id = answers[0]['id']
    ultimate = util.trystuff(question_id, answer_id)
    comments_for_q = data_manager2.get_comments_for_question(question_id)
    return render_template('display_question.html',
                           question=question,
                           question_id=question_id,
                           comments_for_q=comments_for_q,
                           ultimate=ultimate
                           )


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def route_edit_question(question_id):
    if request.method == 'GET':
        original_question = data_manager2.get_question_by_id(question_id)
        return render_template('edit-question.html', question_id=question_id, original_question=original_question)
    else:
        submission_time = datetime.now(),
        message = request.form.get('message'),
        data_manager2.update_question_by_id(question_id, submission_time, message)
        return redirect(url_for("route_question", question_id=question_id))


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def route_edit_answer(answer_id):
    if request.method == 'GET':
        original_answer = data_manager2.get_answer_by_id(answer_id)
        return render_template('edit_answer.html', answer_id=answer_id, original_answer=original_answer)
    if request.method == 'POST':
        original_answer = data_manager2.get_answer_by_id(answer_id)
        question_id = original_answer[0]['question_id']
        submission_time = datetime.now(),
        message = request.form.get('message'),
        data_manager2.update_answer_by_id(answer_id, submission_time, message)
        return redirect(url_for("route_question", question_id=question_id))


@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def route_edit_comment(comment_id):
    if request.method == 'GET':
        original_comment = data_manager2.get_comment_by_id(comment_id)
        return render_template('edit_comment.html', comment_id=comment_id, original_comment=original_comment)
    if request.method == 'POST':
        original_comment = data_manager2.get_comment_by_id(comment_id)
        question_id = original_comment[0]['question_id']
        if question_id is None:
            answer = data_manager2.get_answer_by_id(original_comment[0]['answer_id'])
            question_id = answer['question_id']
        submission_time = datetime.now(),
        message = request.form.get('message'),
        edited_count = original_comment[0]['edited_count'] + 1
        data_manager2.update_comment_by_id(comment_id, submission_time, message, edited_count)
        return redirect(url_for("route_question", question_id=question_id))


@app.route('/add-question', methods=['GET', 'POST'])
def route_add_question():
    if request.method == 'POST':
        title = request.form.get('title'),
        message = request.form.get('message'),
        image = request.form.get('image'),
        data_manager2.add_new_question(title, message, image)
        return redirect('/')
    return render_template('addquestion.html')


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_new_answer(question_id):
    if request.method == "GET":
        return render_template('addanswer.html', question_id=question_id)
    if request.method == 'POST':
        submission_time = datetime.now(),
        question_id = int(question_id)
        message = request.form.get('message'),
        image = request.form.get('image'),
        vote_number = 0
        data_manager2.add_new_answer(submission_time, vote_number, question_id, message, image)
        return redirect(url_for("route_question", question_id=question_id))


@app.route('/addvote-question')
def addvote_question(question_id=None):
    question_id = request.args.get('question_id')
    question = data_manager2.get_question_by_id(question_id)
    vote_number = question[0]['vote_number'] + 1
    data_manager2.update_question_votenum_by_id(question_id, vote_number)
    return redirect(url_for("route_question", question_id=question_id))


@app.route('/downvote-question')
def downvote_question(question_id=None):
    question_id = request.args.get('question_id')
    question = data_manager2.get_question_by_id(question_id)
    vote_number = question[0]['vote_number'] - 1
    data_manager2.update_question_votenum_by_id(question_id, vote_number)
    return redirect(url_for("route_question", question_id=question_id))


@app.route('/addvote_answer/<answer_id>')
def addvote_answer(answer_id):
    answerss = data_manager2.get_answer_by_id(answer_id)
    print(answerss)
    question_id = answerss['question_id']
    vote_number = answerss['vote_number'] + 1
    data_manager2.update_answer_votenum_by_id(answer_id, vote_number)
    return redirect(url_for("route_question", question_id=question_id))


@app.route('/downvote_answer/<answer_id>')
def downvote_answer(answer_id):
    answerss = data_manager2.get_answer_by_id(answer_id)
    question_id = answerss['question_id']
    vote_number = answerss['vote_number'] - 1
    data_manager2.update_answer_votenum_by_id(answer_id, vote_number)
    return redirect(url_for("route_question", question_id=question_id))


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def addcomment_question(question_id):
    if request.method == "GET":
        return render_template('addcomment.html', question_id=question_id)
    if request.method == "POST":
        question_id = question_id
        submission_time = datetime.now(),
        message = request.form.get("message"),
        edited_count = 0,
        answer_id = None
        data_manager2.add_comment_for_question(submission_time, message, edited_count, question_id, answer_id)
        return redirect(url_for("route_question", question_id=question_id))


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def addcomment_answer(answer_id):
    if request.method == "GET":
        return render_template('addcomment2.html', answer_id=answer_id)
    if request.method == "POST":
        answer_id = answer_id
        submission_time = datetime.now(),
        message = request.form.get("message"),
        answer = data_manager2.get_answer_by_id(answer_id)
        print(answer)
        question_id = answer['question_id']
        print(question_id)
        edited_count = 0,
        data_manager2.add_comment_for_answer(submission_time, message, edited_count, answer_id)
        return redirect(url_for("route_question", question_id=question_id))


@app.route('/search')
def search():
    q = request.args.get('q')
    search_result = data_manager2.search_question2(q)
    question_id = request.args.get('question_id')
    return render_template('search2.html', q=q, search_result=search_result,
                           question_id=question_id,)



@app.route('/delete-question')
def delete_question(question_id=None):
    question_id = request.args.get('question_id')
    answer_ids = data_manager2.get_ansver_id_by_question_id(question_id)
    for element in answer_ids:
        data_manager2.delete_comment_by_answer_id(element['id'])
    data_manager2.delete_question_tag_by_question_id(question_id)
    data_manager2.delete_comment_by_question_id(question_id)
    data_manager2.delete_answer_by_question_id(question_id)
    data_manager2.delete_question(question_id)
    return redirect('/list')


@app.route('/delete_answer/<answer_id>')
def delete_answer(answer_id):
    answer_id = answer_id
    answers = data_manager2.get_answer_by_id(answer_id)
    question_id = answers['question_id']
    data_manager2.delete_comment_by_answer_id(answer_id)
    data_manager2.delete_answer_by_answer_id(answer_id)
    return redirect(url_for("route_question", question_id=question_id))


@app.route('/delete-comment/<comment_id>')
def delete_comment(comment_id):
    comment_id = comment_id
    comment = data_manager2.get_comment_by_id(comment_id)
    if comment[0]['question_id'] is not None:
        question_id = comment[0]['question_id']
    else:
        answer = data_manager2.get_answer_by_id(comment[0]['answer_id'])
        question_id = answer['question_id']
    data_manager2.delete_comment_by_comment_id(comment_id)
    return redirect(url_for("route_question", question_id=question_id))


@app.route('/add-view-counter/<question_id>')
def add_view_counter(question_id):
    data_manager2.get_question_by_id(question_id)
    data_manager2.add_one_to_view_number(question_id)
    return redirect(url_for("route_question", question_id=question_id))


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
