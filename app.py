from flask import Flask, render_template, url_for, redirect, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from datetime import datetime 
import json
import os

UPLOAD_FOLDER = '/home/kmk/Pictures'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app) 

class Human(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    middle_name = db.Column(db.String(20))

    num_of_pasport = db.Column(db.String(10))
    face = db.Column(db.LargeBinary, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Article %r' % self.id

#the own page
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/register/", methods=['GET', 'POST'])
def registerdata():
    if request.method == "POST":        
        
        request_data = request.get_json(force=True)
        name = request_data['name']
        last_name = request_data['last_name']
        middle_name = request_data['middle_name']
        num_of_pasport = request_data['num_of_pasport']
        face = request_data['face']

        person = Human(name=name, last_name=last_name, middle_name=middle_name, num_of_pasport=num_of_pasport, face=face)

        try:
            db.session.add(person)
            db.session.commit()
            return redirect('/')
        except:
            db.session.rollback()
            return "Warning: Data haven't been add"
    else:
        return render_template("registerdata.html")

#update a definite data
@app.route("/update/<int:id>/", methods=['PUT'])
def updatedata(id):
    article = Human.query.get_or_404(id)

    if request.method == "PUT":
        
        request_data = request.get_json(force=True)
        article.name = request_data['name']
        article.last_name = request_data['last_name']
        article.middle_name = request_data['middle_name']
        article.num_of_pasport = request_data['num_of_pasport']
        article.face = request_data['face']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            db.session.rollback()
            return "Warning: Data haven't been change"
    else:
        return render_template("updatedata.html", article=article)

#delete a definite data
@app.route("/delete/<int:id>/", methods=['DELETE'])
def deletedata(id):
    article = Human.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        db.session.rollback()
        return "Warning!"

#to add a new picture in way: "UPLOAD_FOLDER"
@app.route('/image/', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)
        return path
    return render_template("image.html")

#all data
@app.route("/posts/")
def posts():
    articles = Human.query.order_by(Human.last_name).all()
    return render_template("posts.html", articles=articles)

if __name__ == "__main__":
    app.run(debug=True)