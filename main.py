
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
    invEmpID=db.Column(db.String(120), db.ForeignKey(Employee.empID))

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
    prepIngr1=db.Column(db.Integer, db.ForeignKey(Ingredients.ingID))
    prepIngr2=db.Column(db.Integer, db.ForeignKey(Ingredients.ingID))
    prepIngr3=db.Column(db.Integer, db.ForeignKey(Ingredients.ingID))
    prepIngr4=db.Column(db.Integer, db.ForeignKey(Ingredients.ingID))
    prepIngr5=db.Column(db.Integer, db.ForeignKey(Ingredients.ingID))

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

@app.route("/ingredients",methods=['POST','GET'])
def ingredients():

    ings=(Ingredients.query.all())
    table="<table>"
    table_row="<tr>"
    table_row+="<th>Ingredient Number</th>"
    table_row+="<th>Ingredient Name</th>"
    table_row+="<th>Ingredient Shelf Life</th>"
    table_row+="<th>Checked</th>"
    table_row+="</tr>"
    table+=table_row
    for i in range(len(ings)):
        table_row="<tr>"
        table_row+="<td>"+str(ings[i].ingID)+"</td>"
        table_row+="<td>"+str(ings[i].ingName)+"</td>"
        table_row+="<td align='right'>"+str(ings[i].ingShelfLife)+" hours</td>"
        table_row+="<td align='right'><input type='checkbox' name=ingid"+str(ings[i].ingID)+"</td>"
        table_row+="</tr>"
        table+=table_row
    table+="</table>"

    return render_template("ingredients.html", title="Ingredients List", table=table)

@app.route("/preps",methods=['POST','GET'])
def preps():

    prepsList=(Preps.query.all())
    table="<table border='4px'>"
    table_row="<tr>"
    table_row+="<th>Prep Number</th>"
    table_row+="<th>Prep Name</th>"
    table_row+="<th>Prep Ingredients</th>"
    table_row+="<th>Prep Shelf Life</th>"
    table_row+="<th>Checked</th>"
    table_row+="</tr>"
    table+=table_row
    for i in range(len(prepsList)):

        prepIngs=Ingredients.query.get(prepsList[i].prepIngr1).ingName
        if prepsList[i].prepIngr2:
            prepIngs+=", "+Ingredients.query.get(prepsList[i].prepIngr2).ingName
        if prepsList[i].prepIngr3:
            prepIngs+=", "+Ingredients.query.get(prepsList[i].prepIngr3).ingName
        if prepsList[i].prepIngr4:
            prepIngs+=", "+Ingredients.query.get(prepsList[i].prepIngr4).ingName
        if prepsList[i].prepIngr5:
            prepIngs+=", "+Ingredients.query.get(prepsList[i].prepIngr5).ingName
        table_row="<tr>"
        table_row+="<td>"+str(prepsList[i].prepID)+"</td>"
        table_row+="<td>"+str(prepsList[i].prepName)+"</td>"
        table_row+="<td>"+prepIngs+"</td>"
        table_row+="<td align='right'>"+str(prepsList[i].prepShelfLife)+" hours</td>"
        table_row+="<td align='right'><input type='checkbox' name=prepid"+str(prepsList[i].prepID)+"</td>"
        table_row+="</tr>"
        table+=table_row
    table+="</table>"
    return table

@app.route("/getemployee", methods=['POST'])
def getemployee():
    employee_id=request.form['empID']
    employee_password=request.form['password']
    employee=Employee.query.filter_by(empID=employee_id).first()
    employee_pos=""
    if employee_id=="" or employee==None:
        return render_template('clockin.html',title='Clock In', employee_error="Employee {} Not Found: Please make sure your employee ID you've entered is correct".format(employee_id))
    elif employee_password=="" or int(employee_password) != employee.empPassword:
        print("form password: "+ employee_password)
        print("db password: "+str(employee.empPassword))
        return render_template('clockin.html',title='Clock In', password_error="Password incorrect, please enter the valid password")

    if employee.empPosition=="M":
        employee_pos="Manager"
        managerPerms=True
    elif employee.empPosition=="B":
        employee_pos="Baker"
        managerPerms=False
    elif employee.empPosition=="G":
        employee_pos="General Manager"
        managerPerms=True
    elif employee.empPosition=="T":
        employee_pos="Trainer"
        managerPerms=False
    else:
        employee_pos="Associate"
        managerPerms=False

    #employee.empFName="William"
    #db.session.commit()
    welcome_msg="Welcome, {}: {} {}.".format(employee_pos, employee.empFName, employee.empLName)
    clockin_msg="You have clocked in at {}".format(datetime.now().strftime('%H:%M:%S'))
    print("Successful Clock In with employee_id: {} and employee_password: {} at time: {} Manager Permissions are: {}".format(employee_id,employee_password,datetime.now().strftime('%H:%M:%S'),managerPerms))
    return render_template('menu.html', title='Menu', error='', welcome_msg=welcome_msg, clockin_msg=clockin_msg)

if __name__ == '__main__':
    app.run()
