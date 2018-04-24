
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://prep-db:root@localhost:8889/prep-db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

login = False
employee_id=0
managerPerms=False

class Employee(db.Model):

    __tablename__="employees"
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

    __tablename__="ingredients"
    ingID= db.Column(db.Integer, primary_key=True)
    ingName=db.Column(db.String(120))
    ingShelfLife=db.Column(db.Integer)

    def __init__(self,ingID,ingName,ingShelfLife):
        self.ingID=ingID
        self.ingName=ingName
        self.ingShelfLife=ingShelfLife


class Inventory(db.Model):

    __tablename__="inventory"
    invID=db.Column(db.Integer, primary_key=True)
    invName=db.Column(db.String(120))
    invIsPrepped=db.Column(db.Integer)
    invLocation=db.Column(db.String(3))
    invDateAdded=db.Column(db.DateTime())
    invExpDate=db.Column(db.DateTime())
    invEmpID=db.Column(db.String(120))

    def __init__(self,invID,invName,invIsPrepped,invLocation,invDateAdded,invExpDate,invEmpID):
        self.invID=invEmpID
        self.invName=invName
        self.invIsPrepped=invIsPrepped
        self.invLocation=invLocation
        self.invDateAdded=invDateAdded
        self.invExpDate=invExpDate
        self.invEmpID=invEmpID

class Preps(db.Model):

    __tablename__="preps"
    prepID=db.Column(db.Integer,primary_key=True)
    prepName=db.Column(db.String(120))
    prepShelfLife=db.Column(db.Integer)
    prepIngr1=db.Column(db.Integer)
    prepIngr2=db.Column(db.Integer)
    prepIngr3=db.Column(db.Integer)
    prepIngr4=db.Column(db.Integer)
    prepIngr5=db.Column(db.Integer)

    def __init__(self, prepID, prepName, prepShelfLife, prepIngr1, prepIngr2, prepIngr3, prepIngr4, prepIngr5):
        self.prepID=prepID
        self.prepName=prepName
        self.prepShelfLife=prepShelfLife
        self.prepIngr1=prepIngr1
        self.prepIngr2=prepIngr2
        self.prepIngr3=prepIngr3
        self.prepIngr4=prepIngr4
        self.prepIngr5=prepIngr5


@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template('clockin.html',title='Clock In', error = "")


@app.route("/clockin", methods=['GET'])
def clockin():
    print("endget")
    return render_template('clockin.html',title='Clock In', error="")

@app.route("/clockin",methods=['POST'])
def clockin_post():
    print ("endpost")
    print(request.form)
    employee_id=request.form['empID']
    employee_password=request.form['password']

    return "employeeid: {} password: {}".format(employee_id, employee_password)

@app.route("/clockout", methods=['POST', 'GET'])
def clockout():
    return render_template('clockout.html', title='Clock Out', error="")

@app.route("/manager", methods=['POST', 'GET'])
def manager():
    return render_template('manager.html',title='Manager', error="")

@app.route("/getemployee", methods=['POST'])
def getemployee():
    employee_id=request.form['empID']
    employee_password=request.form['password']
    employee=Employee.query.filter_by(empID=employee_id).first()
    employee_pos=""
    print(employee)
    if employee_id=="" or employee==None:
        return render_template('clockin.html',title='Clock In', error="Employee {} Not Found: Please make sure your employee ID you've entered is correct".format(employee_id))

    if employee.empPosition=="M":
        employee_pos="Manager"
        managerPerms=True
    elif employee.empPosition=="B":
        employee_pos="Baker"
    elif employee.empPosition=="G":
        employee_pos="General Manager"
        managerPerms=True
    elif employee.empPosition=="T":
        employee_pos="Trainer"
    else:
        employee_pos="Associate"

    #employee.empFName="William"
    #db.session.commit()
    return "<h1>Welcome, {}: {} {}.</h1><p> You have clocked in at {}</p>".format(employee_pos, employee.empFName, employee.empLName, datetime.now().strftime('%H:%M:%S'))

if __name__ == '__main__':
    app.run()
