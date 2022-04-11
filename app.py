from flask import Flask, render_template, url_for, redirect
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from datetime import datetime 
from flask import request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 

class Human(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    middle_name = db.Column(db.String(20))

    num_of_pasport = db.Column(db.String(10))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Article %r' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("index.html")

@app.route("/register/", methods=['POST', 'GET'])
def registerdata():
    if request.method == "POST":
        name = request.form['name']
        last_name = request.form['last_name']
        middle_name = request.form['middle_name']
        num_of_pasport = request.form['num_of_pasport']

        person = Human(name=name, last_name=last_name, middle_name=middle_name, num_of_pasport=num_of_pasport)

        try:
            db.session.add(person)
            db.session.commit()
            return redirect('/')
        except:
            return "Warning: Data haven't been add"
    else:
        return render_template("registerdata.html")

    return render_template("registerdata.html")


@app.route("/get/", methods=['POST', 'GET'])
def getdata():
    return render_template("getdata.html")

@app.route("/update/", methods=['POST', 'GET'])
def updatedata():
    return render_template("updatedata.html")

@app.route("/delete/", methods=['POST', 'GET'])
def deletedata():
    return render_template("deletedata.html")

if __name__ == "__main__":
    app.run(debug=True)