
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://prep-db:root@localhost:8889/prep-db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Employee(db.Model):

    empID = db.Column(db.Integer, primary_key=True)
    empFName = db.Column(db.String(120))
    empLName = db.Column(db.String(120))
    empPassword = db.Column(db.Integer)
    empPosition = db.Column(db.String(1))
    empDOB = db.Column(db.DateTime())
    empHireDate = db.Column(db.DateTime())

    def __init__(self, empFName, empLName, empPassword, empPosition, empDOB, empHireDate):
        self.name = name
        self.empFName=empFName
        self.empLName=empLName
        self.empPassword=empPassword
        self.empPosition=empPosition
        self.empDOB=empDOB
        self.empHireDate=empHireDate


class Ingredients(db.Model):

    ingID= db.Column(db.Integer, primary_key=True)
    ingName=db.Column(db.String(120))
    ingShelfLife=db.Column(db.Integer)

    def __init__(self,ingID,ingName,ingShelfLife):
        self.ingID=ingID
        self.ingName=ingName
        self.ingShelfLife=ingShelfLife


class Inventory(db.Model):
    invID=db.Column(db.Integer, primary_key=True)
    invName=db.Column(db.String(120))
    invIsPrepped=db.Column(db.Integer)
    invLocation=db.Column(db.String(3))
    invDateAdded=db.Column(db.DateTime())
    invExpDate=db.Column(db.DateTime())
    invEmpID=db.Column(db.String(120))

@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template('clockin.html',title='Clock In', error = "")


@app.route("/clockin", methods=['POST', 'GET'])
def clockin():
    return render_template('clockin.html',title='Clock In', error="")

@app.route("/clockout", methods=['POST', 'GET'])
def clockout():
    return render_template('clockout.html', title='Clock Out', error="")

@app.route("/manager", methods=['POST', 'GET'])
def manager():
    return render_template('manager.html',title='Manager', error="")

if __name__ == '__main__':
    app.run()
