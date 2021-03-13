from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail
import os
import yaml

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    config = yaml.load(open('config.yaml'), Loader=yaml.BaseLoader)
    app.config['SQLALCHEMY_DATABASE_URI'] = config['SQLALCHEMY_DATABASE_URI']
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL") #heroku config var

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Bug(db.Model):
    __tablename__ = 'bug'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    type = db.Column(db.String(200))
    priority = db.Column(db.String(200))
    summary = db.Column(db.Text())

    def __init__(self, name, type, priority, summary):
        self.name = name
        self.type = type
        self.priority = priority
        self.summary = summary


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
        if db.session.query(Bug).filter(Bug.name == developername).count() == 0:
            data = Bug(developername, bugtype, bugpriority, bugsummary)
            db.session.add(data)
            db.session.commit()
            send_mail(developername, bugtype, bugpriority, bugsummary)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback.')


if __name__ == '__main__':
    app.run()