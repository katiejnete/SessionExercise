from flask import Flask, render_template, flash
from flask import request, redirect, session
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret830923'

@app.route("/")
def start_survey():
    """Shows start page of survey."""
    session['title'] = survey.title
    session['instrucs'] = survey.instructions
    return render_template(
        'base.html')

@app.route("/session", methods=["POST"])
def start_session():
    """Clear session of responses and asked questions."""
    session['responses'] = []
    responses = session['responses']
    num = len(responses)
    return redirect(f"/questions/{num}")

@app.route("/questions/<int:num>")
def question_handler(num):
    """Displays current question."""
    responses = session['responses']
    if len(responses) == len(survey.questions):
        return redirect("/thanks")
    elif num == len(responses):
        q = survey.questions[num]
        return render_template(
            'q.html',qnum=num,q=q.question,choices=q.choices)
    else:
        flash('You are tying to access an invalid question. Please answer questions in order.','invalid')
        num = len(responses)
        return redirect(f"/questions/{num}")      

@app.route("/answer", methods=["POST"])
def answer_handler():
    """Saves responses and redirects to next question."""
    responses = session['responses']
    if  len(responses) == len(survey.questions):
        ans = request.form['answer']
        responses.append(ans)
        session['responses'] = responses
        return redirect("/thanks")
    else:
        ans = request.form['answer']
        responses.append(ans)
        session['responses'] = responses
        num = len(responses)            
        return redirect(f"/questions/{num}")

@app.route("/thanks")
def thank_user():
    """Survey complete. Shows 'Thank You' page."""
    session.pop('responses', default=None)
    return render_template(
        'thanks.html')


