from flask import Flask, render_template, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


RESPONSES_KEY = "responses"


@app.route('/')
def show_survey_start():
    
    return render_template('survey_start.html', survey = survey)

@app.route('/begin', methods = ['POST'])
def start_survey():
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')

@app.route('/answer', methods =["POST"])
def handle_question():
    """ Save answers from questions"""

    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect('/complete')
    else: 
        return redirect(f"/questions/{len(responses)}")

@app.route('/questions/<int:qid>')
def show_question(qid):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect("/")

    if (len(responses)==len(survey.questions)):
        return redirect('/complete')

    if (len(responses)!= qid):
        flash (f"Invalid question id: {qid}")

    question = survey.questions[qid]
    return render_template('question.html', question_num=qid, question = question)

@app.route('/complete')
def complete():
    return render_template('completion.html')