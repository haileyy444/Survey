from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret_key"
app.config['DEBUG_TD-inTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
RESPONSE_KEY = "responses"






@app.route("/")
def surveyBase():
    return render_template("home.html", survey = survey)






@app.route("/start", methods=["POST"])
def start_survey():
    session[RESPONSE_KEY] = []

    return redirect("/questions/0")





@app.route("/questions/<int:questionID>")
def show_question(questionID):
    responses = session.get(RESPONSE_KEY)

    if(not responses or responses is None):
        return redirect("/")
    
    if(len(responses) == len(survey.questions)):
        return redirect("/complete")
    
    if (len(responses) != questionID):
        flash(f"Error, invalid question id: {questionID}.")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[questionID]

    return render_template("questions.html", question_num=questionID, question=question)






@app.route("/answer", methods=["POST"])
def answers():
    choice = request.form['answer']

    responses = session.get[RESPONSE_KEY]
    responses.append(choice)
    session[RESPONSE_KEY] = responses

    if(len(responses) == len(survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")
  




@app.route("/complete")
def thanks():
    
    return render_template("thanks.html")



if __name__ == "__main__":
    app.run(debug=True, port=5000)
