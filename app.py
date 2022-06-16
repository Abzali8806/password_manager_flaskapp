from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:passwd@172.17.0.1/users'

db=SQLAlchemy(app)

class Users(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(40))
    sitename=db.Column(db.String(40))
    password=db.Column(db.String(40))

    def __init__(self, name, sitename, password):
        self.name=name
        self.sitename=sitename
        self.password=password


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name=request.form['name']
        sitename=request.form['sitename']
        password=request.form['password']

        user=Users(name, sitename, password)
        db.session.add(user)
        db.session.commit()
    
    return render_template('index.html')



@app.route('/submit')
def submit():
    return render_template('submit.html')


@app.route('/retrieve', methods=['GET', 'POST'])
def retrieve():
    if request.method == 'POST':
        userResult=db.session.query(Users)
        for user in userResult:
            print(user.name)
            print(user.password)
        
        return render_template('retrieve.html')


if __name__ == "__main__":
    app.run(port=8080,debug=True)
