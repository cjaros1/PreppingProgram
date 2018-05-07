
from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os, math

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://prep-db:root@localhost:8889/prep-db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

global clocked_in
global employee
global clockin_time
global hours

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
    prepCount=db.Column(db.Integer)

    def __init__(self, prepID, prepName, prepShelfLife, prepIngr1, prepIngr2, prepIngr3, prepIngr4, prepIngr5, prepCount):
        self.prepID=prepID
        self.prepName=prepName
        self.prepShelfLife=prepShelfLife
        self.prepIngr1=prepIngr1
        self.prepIngr2=prepIngr2
        self.prepIngr3=prepIngr3
        self.prepIngr4=prepIngr4
        self.prepIngr5=prepIngr5
        self.prepCount=prepCount


class Inventory(db.Model):

    __tablename__="inventory"
    invID=db.Column(db.Integer, primary_key=True)
    invName=db.Column(db.String(120))
    invLocation=db.Column(db.String(3))
    invDateAdded=db.Column(db.DateTime())
    invExpDate=db.Column(db.DateTime())
    invEmpID=db.Column(db.String(120), db.ForeignKey(Employee.empID))
    invPrepID=db.Column(db.Integer, db.ForeignKey(Preps.prepID))
    invIngID=db.Column(db.Integer, db.ForeignKey(Ingredients.ingID))
    invQOH=db.Column(db.Float)

    def __init__(self,invID,invName,invLocation,invDateAdded,invExpDate,invEmpID, invPrepID, invIngID, invQOH):
        self.invID=invID
        self.invName=invName
        self.invLocation=invLocation
        self.invDateAdded=invDateAdded
        self.invExpDate=invExpDate
        self.invEmpID=invEmpID
        self.invPrepID=invPrepID
        self.invIngID=invIngID
        self.invQOH=invQOH

class Hours(db.Model):

    __tablename__="hours"
    hrLogID=db.Column(db.Integer, primary_key=True)
    hrEmpID=db.Column(db.Integer, db.ForeignKey(Employee.empID))
    hrCInTime=db.Column(db.DateTime())
    hrCOutTime=db.Column(db.DateTime())
    hrShiftHrs=db.Column(db.Integer)

    def __init__(self, hrLogID, hrEmpID, hrCInTime, hrCOutTime, hrShiftHrs):
        self.hrLogID=hrLogID
        self.hrEmpID=hrEmpID
        self.hrCInTime=hrCInTime
        self.hrCOutTime=hrCOutTime
        self.hrShiftHrs=hrShiftHrs


@app.route("/", methods=['POST', 'GET'])
def index():

    clocked_in=False
    session['clocked_in']=clocked_in
    return render_template('clockin.html',title='Clock In', error = "", clocked_in=session['clocked_in'])


@app.route("/clockin", methods=['GET'])
def clockin():

    clocked_in=False
    prepStart=False
    session['prepStart']=prepStart
    session['clocked_in']=clocked_in
    return render_template('clockin.html',title='Clock In', error="", clocked_in=session['clocked_in'])

@app.route("/clockin",methods=['POST'])
def clockin_post():
    clocked_in=False
    prepStart=False
    session['prepStart']=prepStart
    session['clocked_in']=clocked_in
    employee_id=request.form['empID']
    employee_password=request.form['password']

    return "employeeid: {} password: {}".format(employee_id, employee_password)

@app.route("/menu",methods=['POST','GET'])
def menu():
    clocked_in=session['clocked_in']
    managerPerms=session['managerPerms']
    employee_name=session['employee_First']+" "+session['employee_Last']
    employee_pos=session['employee_pos']
    header_msg=employee_pos+": "+employee_name
    return render_template('menu.html',title='Menu',error='', welcome_msg=header_msg, clocked_in=clocked_in,managerPerms=managerPerms)

@app.route("/clockout", methods=['POST', 'GET'])
def clockout():

    hoursID=Hours.query.count()+1
    while Hours.query.filter_by(hrLogID=hoursID).first() != None:
        hoursID+=1

    clockin_time=session['clockin_time']
    employee_ID=session['employee_ID']
    clockout_time=datetime.now()
    shiftHrs=(clockout_time.hour+clockout_time.minute/60+clockout_time.second/3600)-(clockin_time.hour+clockin_time.minute/60+clockin_time.second/3600)

    hours=Hours(hoursID, employee_ID, clockin_time, clockout_time, shiftHrs)
    clockout_msg="{}: {} {} Clock In Time: {} Clock Out Time: {}".format(session['employee_pos'], session['employee_First'], session['employee_Last'], clockin_time.strftime('%H:%M:%S'), clockout_time.strftime('%H:%M:%S'))
    hours_msg="Hours: {:.2f}".format(shiftHrs)
    clocked_in=False
    managerPerms=False
    session['managerPerms']=managerPerms
    session['clocked_in']=clocked_in
    db.session.add(hours)
    db.session.commit()
    return render_template('clockout.html', title='Clock Out', error="", clockout_msg=clockout_msg, hours_msg=hours_msg, clocked_in=session['clocked_in'], managerPerms=session['managerPerms'])

@app.route("/manager", methods=['POST', 'GET'])
def manager():
    return render_template('manager.html', title='Manager', error="", clocked_in=session['clocked_in'], managerPerms=session['managerPerms'])

@app.route("/inventory",methods=['POST','GET'])
def inventory():
    invs=(Inventory.query.all())
    table=[]

    location=""


    for i in range(len(invs)):
        row=[]

        if invs[i].invLocation=="WIC":
            location="Walk In Cooler"
        elif invs[i].invLocation=="FRZ":
            location="Freezer"
        elif invs[i].invLocation=="SWB":
            location="Sandwich Bar"
        elif invs[i].invLocation=="SAB":
            location="Salad Bar"
        else:
            location="Other"

        hr3=datetime.now()+timedelta(hours=3)

        isExpired="fresh"
        if invs[i].invExpDate<datetime.now():
            isExpired="expired"
        elif invs[i].invExpDate<hr3:
            isExpired="3hr"
        elif invs[i].invExpDate.date()==datetime.now().date():
            isExpired="today"



        emp=Employee.query.filter_by(empID=invs[i].invEmpID).first()
        row.append(str(invs[i].invID))
        row.append(str(invs[i].invName))
        row.append(str(invs[i].invQOH))
        row.append(location)
        row.append(str(invs[i].invDateAdded))
        row.append(str(invs[i].invExpDate))
        row.append(str(emp.empLName)+", "+str(emp.empFName)[0])
        row.append(isExpired)
        table.append(row)


    return render_template('inventory.html', title='Inventory', error='', table=table, clocked_in=session['clocked_in'], managerPerms=session['managerPerms'])



@app.route("/addinventory",methods=['POST','GET'])
def addinventory():
    ings=(Ingredients.query.all())
    preps=(Preps.query.all())
    ingNames=[]
    prepNames=[]
    for i in range(len(ings)-1):
        ingNames.append(ings[i].ingName)
    session['ingNames']=ingNames
    for i in range(len(preps)-1):
        prepNames.append(preps[i].prepName)
    session['prepNames']=prepNames

    return render_template('addinventory.html', title='Add To Inventory', error='', ingNames=session['ingNames'], prepNames=session['prepNames'], clocked_in=session['clocked_in'], managerPerms=session['managerPerms'])


@app.route("/inventoryadded", methods=['POST'])
def inventoryadded():

    quantity=int(request.form['quantity'])

    if quantity < 0 :
        error="Cannot add negative quantity to inventory, please select a positive number."
        return render_template('addinventory.html', title='Add To Inventory', error='', ingNames=session['ingNames'],  clocked_in=session['clocked_in'], managerPerms=session['managerPerms'])
    elif quantity==0:
        error="You have added 0 {} to the inventory.".format(ingredient)
        return render_template('addinventory.html', title='Add To Inventory', error='', ingNames=session['ingNames'],  clocked_in=session['clocked_in'], managerPerms=session['managerPerms'])


    idNum=int(request.form.get('num'))
    invLoc=request.form.get('location')
    dateAdded=datetime.now()
    employee_ID=session['employee_ID']


    if idNum>=30:
        idNum-=29
        prep=Preps.query.filter_by(prepID=idNum).first()
        expiration= dateAdded + timedelta(hours=prep.prepShelfLife)
        invName=prep.prepName
        invPrepID=prep.prepID
        invIngID=30
    else:
        ing=Ingredients.query.filter_by(ingID=idNum).first()
        expiration=dateAdded+timedelta(hours=ing.ingShelfLife)
        invName=ing.ingName
        invPrepID=19
        invIngID=ing.ingID

    if invLoc=="FRZ":
        loc="freezer"
    elif invLoc=="WIC":
        loc="walk in cooler"
    elif invLoc=="SAB":
        loc="salad bar"
    elif invLoc=="SWB":
        loc="sandwich bar"
    else:
        loc="other location"






    invID=Inventory.query.count()+1
    while Inventory.query.filter_by(invID=invID).first() != None:
        invID+=1

    inventory=Inventory(invID,invName,invLoc,dateAdded,expiration,employee_ID,invPrepID,invIngID,quantity)
    db.session.add(inventory)
    db.session.commit()

    add_msg="You have added {} {} to the inventory in the {}".format(quantity, invName, loc)

    return render_template('addinventory.html', title='Add To Inventory', error='', ingNames=session['ingNames'], prepNames=session['prepNames'], add_msg=add_msg, clocked_in=session['clocked_in'], managerPerms=session['managerPerms'])


@app.route("/inventorydeleted", methods=['POST'])
def inventorydeleted():


    deletedMsg="You have deleted "
    invSelect=request.form.getlist("invSelect")

    if invSelect!= []:
        for i in invSelect:
            invID=i
            inventory=Inventory.query.filter_by(invID=i).first()
            deletedMsg+="{} {}".format(inventory.invQOH, inventory.invName)
            db.session.delete(inventory)
        db.session.commit()
    else:
        deletedMsg="Nothing has been deleted "

    deletedMsg+=" from the inventory."

    return render_template('inventorydeleted.html', title='Deleted From Inventory', deletedMsg=deletedMsg, prepStart=session['prepStart'], error='',  clocked_in=session['clocked_in'], managerPerms=session['managerPerms'])



@app.route("/delinventory",methods=['POST','GET'])
def delinventory():
    invs=(Inventory.query.order_by(Inventory.invExpDate).all())
    table=[]

    location=""


    for i in range(len(invs)):
        row=[]

        if invs[i].invLocation=="WIC":
            location="Walk In Cooler"
        elif invs[i].invLocation=="FRZ":
            location="Freezer"
        elif invs[i].invLocation=="SWB":
            location="Sandwich Bar"
        elif invs[i].invLocation=="SAB":
            location="Salad Bar"
        else:
            location="Other"

        hr3=datetime.now()+timedelta(hours=3)

        isExpired="fresh"
        if invs[i].invExpDate<datetime.now():
            isExpired="expired"
        elif invs[i].invExpDate<hr3:
            isExpired="3hr"
        elif invs[i].invExpDate.date()==datetime.now().date():
            isExpired="today"



        emp=Employee.query.filter_by(empID=invs[i].invEmpID).first()
        row.append(str(invs[i].invID))
        row.append(str(invs[i].invName))
        row.append(str(invs[i].invQOH))
        row.append(location)
        row.append(str(invs[i].invDateAdded))
        row.append(str(invs[i].invExpDate))
        row.append(str(emp.empLName)+", "+str(emp.empFName)[0])
        row.append(isExpired)
        table.append(row)
        prepStart=session['prepStart']

    return render_template('delinventory.html', title='Delete From Inventory', prepStart=session['prepStart'], error='', table=table, clocked_in=session['clocked_in'], managerPerms=session['managerPerms'])


@app.route("/ingredients",methods=['POST','GET'])
def ingredients():

    ings=(Ingredients.query.all())
    table=[]
    for i in range(len(ings)-1):
        row=[]
        row.append(str(ings[i].ingID))
        row.append(str(ings[i].ingName))
        row.append(str(ings[i].ingShelfLife))
        table.append(row)


    return render_template("ingredients.html", title="Ingredients List", table=table, clocked_in=session['clocked_in'], managerPerms=session['managerPerms'])

@app.route("/preps",methods=['POST','GET'])
def preps():

    prepsList=(Preps.query.all())
    table=[]

    for i in range(len(prepsList)-1):

        prepIngs=Ingredients.query.get(prepsList[i].prepIngr1).ingName
        if prepsList[i].prepIngr2:
            prepIngs+=", "+Ingredients.query.get(prepsList[i].prepIngr2).ingName
        if prepsList[i].prepIngr3:
            prepIngs+=", "+Ingredients.query.get(prepsList[i].prepIngr3).ingName
        if prepsList[i].prepIngr4:
            prepIngs+=", "+Ingredients.query.get(prepsList[i].prepIngr4).ingName
        if prepsList[i].prepIngr5:
            prepIngs+=", "+Ingredients.query.get(prepsList[i].prepIngr5).ingName

        row=[]
        row.append(str(prepsList[i].prepID))
        row.append(str(prepsList[i].prepName))
        row.append(prepIngs)
        row.append(str(prepsList[i].prepShelfLife))
        table.append(row)


    return render_template("preps.html", title="Preps List", table=table, clocked_in=session['clocked_in'], managerPerms=session['managerPerms'])

@app.route("/prepstart",methods=['POST','GET'])
def prepstart():
    invs=(Inventory.query.order_by(Inventory.invExpDate).all())
    table=[]

    location=""


    for i in range(len(invs)):
        row=[]

        if invs[i].invLocation=="WIC":
            location="Walk In Cooler"
        elif invs[i].invLocation=="FRZ":
            location="Freezer"
        elif invs[i].invLocation=="SWB":
            location="Sandwich Bar"
        elif invs[i].invLocation=="SAB":
            location="Salad Bar"
        else:
            location="Other"

        hr3=datetime.now()+timedelta(hours=3)

        isExpired="fresh"
        if invs[i].invExpDate<datetime.now():
            isExpired="expired"
        elif invs[i].invExpDate<hr3:
            isExpired="3hr"
        elif invs[i].invExpDate.date()==datetime.now().date():
            isExpired="today"



        emp=Employee.query.filter_by(empID=invs[i].invEmpID).first()
        row.append(str(invs[i].invID))
        row.append(str(invs[i].invName))
        row.append(str(invs[i].invQOH))
        row.append(location)
        row.append(str(invs[i].invDateAdded))
        row.append(str(invs[i].invExpDate))
        row.append(str(emp.empLName)+", "+str(emp.empFName)[0])
        row.append(isExpired)
        table.append(row)
        prepStart=True
        session['prepStart']=prepStart

    return render_template('delinventory.html', title='Delete From Inventory', prepStart=session['prepStart'], error='', table=table, clocked_in=session['clocked_in'], managerPerms=session['managerPerms'])



@app.route("/getemployee", methods=['POST'])
def getemployee():


    employee_id=request.form['empID']
    employee_password=request.form['password']
    employee=Employee.query.filter_by(empID=employee_id).first()
    employee_pos=""
    managerPerms=False


    if employee_id=="" or employee==None:
        session['clocked_in']=False
        session['managerPerms']=False
        return render_template('clockin.html',title='Clock In', employee_error="Employee {} Not Found: Please make sure your employee ID you've entered is correct".format(employee_id), clocked_in=session['clocked_in'], managerPerms=session['managerPerms'])
    elif employee_password=="" or int(employee_password) != employee.empPassword:
        session['clocked_in']=False
        session['managerPerms']=False
        return render_template('clockin.html',title='Clock In', password_error="Password incorrect, please enter the valid password", clocked_in=session['clocked_in'], managerPerms=session['managerPerms'])

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

    session['employee_First']=employee.empFName
    session['employee_Last']=employee.empLName
    session['employee_pos']=employee_pos
    session['managerPerms']=managerPerms
    session['employee_ID']=employee.empID





    clockin_time=datetime.now()
    session['clockin_time']=clockin_time
    welcome_msg="Welcome, {}: {} {}.".format(employee_pos, employee.empFName, employee.empLName)
    clockin_msg="You have clocked in at {}".format(clockin_time.strftime('%H:%M:%S'))
    clocked_in=True
    session['clocked_in']=clocked_in



    return render_template('menu.html', title='Menu', error='', welcome_msg=welcome_msg, clockin_msg=clockin_msg, managerPerms=managerPerms, clocked_in=clocked_in)


@app.route("/prepcount",methods=['POST','GET'])
def prepcount():
    prepsList=Inventory.query.filter_by(invIngID=30).all()

    table=[]
    for i in range(len(prepsList)):

        prep=Preps.query.filter_by(prepID=prepsList[i].invPrepID).first()
        print(str(prepsList[i]))
        if prepsList[i].invName in table:
            index=table.index(prepsList[i].invName)
            table[index][0]+=prepsList[i].invQOH
            table[index][3]-=prepsList[i].invQOH

        else:
            row=[]
            row.append(prepsList[i].invQOH)
            row.append(prepsList[i].invName)
            row.append(prep.prepCount)
            row.append(int(prep.prepCount-math.floor(prepsList[i].invQOH)))
            table.append(row)



    return render_template("prepcount.html", title="Prep Count", table=table )

@app.route("/hireemployee", methods=['POST'])
def hireemployee():

    return render_template('hireemployee.html', title="Hire Employee")

@app.route("/fireemployee", methods=['POST'])
def fireemployee():

    return render_template('fireemployee.html', title="Fire Employee")

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run()
