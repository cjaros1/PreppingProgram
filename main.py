
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://prep-db:root@localhost:8889/prep-db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    def __init__(self, name):
        self.name = name


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method=='POST':
        task=request.form['task']
        tasks.append(task)

    return render_template('clockin.html',title="Clock In", task=tasks)





if __name__ == '__main__':
    app.run()
