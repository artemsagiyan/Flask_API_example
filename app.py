from flask import Flask, render_template, url_for, redirect, Response, request
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
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Article %r' % self.id

#the own page
@app.route('/', methods=['GET'])
def index():
    return Response({"message":"page is opened"}, status=200, mimetype='application/json')

@app.route("/register/", methods=['GET', 'POST'])
def registerdata():
    if request.method == "POST":        
        
        request_data = request.get_json(force=True)
        name = request_data['name']
        last_name = request_data['last_name']
        middle_name = request_data['middle_name']
        num_of_pasport = request_data['num_of_pasport']

        person = Human(name=name, last_name=last_name, middle_name=middle_name, num_of_pasport=num_of_pasport)

        try:
            db.session.add(person)
            db.session.commit()
            return Response({"message":"Request completed successfully"}, status=200, mimetype='application/json')
        except:
            db.session.rollback()
            return Response({"message":"Warning:Haven't been add"}, status=400, mimetype='application/json')
    else:
        return Response({"message":"Your request isn't valid"})

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

        try:
            db.session.commit()
            return Response({"message":"Data in DB is changed"}, status=200, mimetype='application/json')
        except:
            db.session.rollback()
            return Response({"message":"Warning: Data haven't been change"}, status=400, mimetype="application/json")
    else:
        return Response({"message":"Your request isn't valid"}, mimetype='application/json')

#delete a definite data
@app.route("/delete/<int:id>/", methods=['DELETE'])
def deletedata(id):
    article = Human.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return Response({"message":"Data is deleted"}, status=200, mimetype='application/json')
    except:
        db.session.rollback()
        return Response({"message":"Don't find such data"}, mimetype='application/json')

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
    return Response({"message":"Image is uplouded"}, status=200, mimetype='application/json')

#all data
@app.route("/posts/")
def get():
    article = Human.query.order_by(Human.last_name).all()
    return article

if __name__ == "__main__":
    app.run(debug=True)