from flask import Flask, render_template, request, redirect, url_for
import os
import data_manager2
import data_manager
from datetime import datetime
import util

app = Flask(__name__)


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


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def route_question(question_id):
    if request.method == 'POST':
        return redirect('/')
    if request.method == 'GET':
        route_view_counter(question_id)
        question = data_manager2.get_question_by_id(question_id)
        answers = data_manager2.get_answers_for_question(question_id)
        """ for answer in answers:
            comments_for_a = data_manager2.get_comments_for_answer(answer_id)"""
        answer_id = question[0]['id']
        ultimate = util.trystuff(question_id, answer_id)
        comments_for_q = data_manager2.get_comments_for_question(question_id)
        return render_template('display_question.html',
                               question_id=question_id,
                               question=question,
                               answers=answers,
                               answer_id=answer_id,
                               comments_for_q=comments_for_q,
                               ultimate=ultimate
                               )


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def route_edit_question(question_id):
    if request.method == 'GET':
        original_question = data_manager2.get_question_by_id(question_id)
        print(original_question)
        return render_template('edit-question.html', question_id=question_id, original_question=original_question)
    if request.method == 'POST':
        original_question = data_manager2.get_answer_by_id(question_id)
        question_id = original_question[0]['id']
        submission_time = datetime.now(),
        message = request.form.get('message'),
        data_manager2.update_question_by_id(question_id, submission_time, message)
        to_url = '/question/' + str(question_id)
        return redirect(to_url)


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def route_edit_answer(answer_id):
    if request.method == 'GET':
        original_answer = data_manager2.get_answer_by_id(answer_id)
        print(original_answer)
        return render_template('edit_answer.html', answer_id=answer_id, original_answer=original_answer)
    if request.method == 'POST':
        original_answer = data_manager2.get_answer_by_id(answer_id)
        question_id = original_answer[0]['question_id']
        submission_time = datetime.now(),
        message = request.form.get('message'),
        data_manager2.update_answer_by_id(answer_id, submission_time, message)
        to_url = '/question/' + str(question_id)
        return redirect(to_url)


@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def route_edit_comment(comment_id):
    if request.method == 'GET':
        original_comment = data_manager2.get_comment_by_id(comment_id)
        print(original_comment)
        return render_template('edit_comment.html', comment_id=comment_id, original_comment=original_comment)
    if request.method == 'POST':
        original_comment = data_manager2.get_comment_by_id(comment_id)
        question_id = original_comment[0]['question_id']
        if question_id is None:
            answer = data_manager2.get_answer_by_id(original_comment[0]['answer_id'])
            question_id = answer[0]['question_id']
        submission_time = datetime.now(),
        message = request.form.get('message'),
        data_manager2.update_comment_by_id(comment_id, submission_time, message)
        to_url = '/question/' + str(question_id)
        return redirect(to_url)


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
    if request.method == "GET":
        return render_template('addanswer.html', question_id=question_id)
    if request.method == 'POST':
        submission_time = datetime.now(),
        question_id = int(question_id)
        message = request.form.get('message'),
        image = request.form.get('image'),
        vote_number = 0
        data_manager2.add_new_answer(submission_time, vote_number, question_id, message, image)
        to_url = '/question/' + str(question_id)
        return redirect(to_url)
        #return render_template('display_question.html', question_id=question_id, question=question, answers=answers)


def route_view_counter(question_id):
    data_manager2.get_question_by_id(question_id)
    data_manager2.add_one_to_view_number(question_id)


@app.route('/addvote-question')
def addvote_question(question_id=None):
    question_id = request.args.get('question_id')
    question = data_manager2.get_question_by_id(question_id)
    print(question_id)
    print(question)
    print(question[0]['vote_number'])
    vote_number = question[0]['vote_number'] + 1
    data_manager2.update_question_votenum_by_id(question_id, vote_number)
    question = data_manager2.get_question_by_id(question_id)
    answers = data_manager2.get_answers_for_question(question_id)
    return render_template('display_question.html',
                           question_id=question_id,
                           question=question,
                           answers=answers)


@app.route('/downvote-question')
def downvote_question(question_id=None):
    question_id = request.args.get('question_id')
    question = data_manager2.get_question_by_id(question_id)
    print(question_id)
    print(question)
    print(question[0]['vote_number'])
    vote_number = question[0]['vote_number'] - 1
    data_manager2.update_question_votenum_by_id(question_id, vote_number)
    question = data_manager2.get_question_by_id(question_id)
    answers = data_manager2.get_answers_for_question(question_id)
    return render_template('display_question.html',
                           question_id=question_id,
                           question=question,
                           answers=answers)


@app.route('/addvote_answer')
def addvote_answer(answer_id=None, question_id=None):
    question_id = request.args.get('question_id')
    answer_id = request.args.get('answer_id')
    answerss = data_manager2.get_answer_by_id(answer_id)
    question_id = answerss[0]['question_id']
    print(answerss)
    vote_number = answerss[0]['vote_number'] + 1
    print(vote_number)
    print(answer_id)
    data_manager2.update_answer_votenum_by_id(answer_id, vote_number)
    question = data_manager2.get_question_by_id(question_id)
    answers = data_manager2.get_answers_for_question(question_id)

    return render_template('display_question.html',
                           question_id=question_id,
                           question=question,
                           answers=answers)


@app.route('/downvote_answer')
def downvote_answer(answer_id=None, question_id=None):
    question_id = request.args.get('question_id')
    answer_id = request.args.get('answer_id')
    answerss = data_manager2.get_answer_by_id(answer_id)
    question_id = answerss[0]['question_id']
    print(answerss)
    vote_number = answerss[0]['vote_number'] - 1
    print(vote_number)
    print(answer_id)
    data_manager2.update_answer_votenum_by_id(answer_id, vote_number)
    question = data_manager2.get_question_by_id(question_id)
    answers = data_manager2.get_answers_for_question(question_id)
    return render_template('display_question.html',
                           question_id=question_id,
                           question=question,
                           answers=answers)


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
        question = data_manager2.get_question_by_id(question_id)
        answers = data_manager2.get_answers_for_question(question_id)
        #comment_for_question = data_manager2.get_comment_for_question(question_id)
        to_url = '/question/' + str(question_id)
        return redirect(to_url)
        """return render_template('display_question.html',
                               question_id=question_id,
                               question=question,
                               
                               answers=answers)"""
                               #comment_for_question=comment_for_question)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def addcomment_answer(answer_id):
    if request.method == "GET":
        return render_template('addcomment2.html', answer_id=answer_id)
    if request.method == "POST":
        answer_id = answer_id
        submission_time = datetime.now(),
        message = request.form.get("message"),
        answer = data_manager2.get_answer_by_id(answer_id)
        question_id = answer[0]['question_id']
        edited_count = 0,
        print(answer_id)
        data_manager2.add_comment_for_answer(submission_time, message, edited_count, answer_id)
        #question = data_manager2.get_question_by_id(question_id)
        #answers = data_manager2.get_answers_for_question(question_id)
        to_url = '/question/' + str(question_id)
        return redirect(to_url)
'''render_template('display_question.html',
                               question_id=question_id,
                               question=question,
                               answers=answers)
'''

@app.route('/search')
def search():
    q = request.args.get('q')
    search_result = data_manager2.search_question(q)
    search_result_answer = data_manager2.search_answer(q)
    search_result_message = data_manager2.search_question_message(q)
    empty_list = []
    question = data_manager2.get_all_data()
    question_id = request.args.get('question_id')

    return render_template('search.html', q=q, search_result=search_result, search_result_answer=search_result_answer, search_result_message=search_result_message, empty_list=empty_list, question_id=question_id, question=question)



@app.route('/delete-question')
def delete_question(question_id=None):
    question_id = request.args.get('question_id')
    data_manager2.delete_question_tag_by_question_id(question_id)
    data_manager2.delete_comment_by_question_id(question_id)
    data_manager2.delete_answer_by_question_id(question_id)
    data_manager2.delete_question(question_id)
    return redirect('/list')

@app.route('/delete_answer/<answer_id>')
def delete_answer(answer_id):
    answer_id = answer_id
    print(answer_id)
    data_manager2.delete_comment_by_answer_id(answer_id)
    data_manager2.delete_answer_by_answer_id(answer_id)
    return redirect('/list')


@app.route('/delete-comment')
def delete_comment(comment_id):
    comment_id=comment_id
    print(comment_id)
    data_manager2.delete_comment_by_comment_id(comment_id)
    return redirect('/list')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )