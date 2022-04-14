from flask import Flask, render_template, url_for, redirect
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from datetime import datetime 
from flask import request
import json

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
'''
@app.route('/picture', methods=['GET', 'POST'])
def picture():
    return "Photo:"

url = 'http:/127.0.0.1:7000/picture'
img = 'home/kmk/Pictures/Screenshot from 2022-04-12 12-15-11.png'   

with open(img, 'rb') as f:
    img_bytes = f.read()
files = {'photo':('img.png', img_bytes)}
response = requests.post(url, files=files)
vec2 = response.json()['vecs']
'''

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

        person = Human(name=name, last_name=last_name, middle_name=middle_name, num_of_pasport=num_of_pasport)

        try:
            db.session.add(person)
            db.session.commit()
            return redirect('/')
        except:
            db.session.rollback()
            return "Warning: Data haven't been add"
    else:
        return render_template("registerdata.html")

@app.route("/update/<int:id>", methods=['PUT'])
def updatedata(id):
    article = Human.query.get_or_404(id)

    print(article)

    print("method:")
    print(request.method)
    print(request.form)

    if request.method == "PUT":
        
        request_data = request.get_json(force=True)
        article.name = request_data['name']
        article.last_name = request_data['last_name']
        article.middle_name = request_data['middle_name']
        article.num_of_pasport = request_data['num_of_pasport']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            db.session.rollback()
            return "Warning: Data haven't been change"
    else:
        return render_template("updatedata.html", article=article)

@app.route("/delete/<int:id>", methods=['GET'])
def deletedata(id):
    article = Human.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        db.session.rollback()
        return "Warning!"

@app.route("/posts")
def posts():
    articles = Human.query.order_by(Human.last_name).all()
    return render_template("posts.html", articles=articles)

if __name__ == "__main__":
    app.run(debug=True)