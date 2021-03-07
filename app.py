from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:IShallOvercome@localhost/lexus'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qlodaemmvyawth:d7d8741f260da924ff32c455b6975b3e401e783fece05ffebc2ff1b3c86becf2@ec2-18-211-97-89.compute-1.amazonaws.com:5432/d1evkrmjak1kmi'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    developername = db.Column(db.String(200), unique=True)
    bugtype = db.Column(db.String(200))
    bugpriority = db.Column(db.String(200))
    bugsummary = db.Column(db.Text())

    def __init__(self, developername, bugtype, bugpriority, bugsummary):
        self.developername = developername
        self.bugtype = bugtype
        self.bugpriority = bugpriority
        self.bugsummary = bugsummary


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        developername = request.form['developername']
        bugtype = request.form['bugtype']
        bugpriority = request.form['bugpriority']
        bugsummary = request.form['bugsummary']
        if developername == '' or bugtype == '':
            return render_template('index.html', message='Please enter required fields.')
        if db.session.query(Feedback).filter(Feedback.developername == developername).count() == 0:
            data = Feedback(developername, bugtype, bugpriority, bugsummary)
            db.session.add(data)
            db.session.commit()
            send_mail(developername, bugtype, bugpriority, bugsummary)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback.')


if __name__ == '__main__':
    app.run()