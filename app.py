from flask import Flask,render_template,redirect, request, session,url_for
import acdatabase as db
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = 'karan-chin'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='account'

mysql=MySQL(app)


@app.route('/login',methods=["POST","GET"])
def login():
    if request.method=="POST":
        fmdata=request.form
        ename=fmdata['ename']
        password=fmdata['password']
        q = "select * from customer where ename='"+ename+"' and passw='"+password+"'"
        cursor = mysql.connection.cursor()
        cursor.execute(q)
        mysql.connection.commit()
        ac = cursor.fetchone()
        if ac:
            a=ac[1]
            b=ac[2]
            session['ename']=a
            session['password']=b
            return render_template("homepage.html",ename=session['ename'],password=session['password'],ac1=ac)
        else:
            msg="Sorry!!! Incorrect username/password"
            return render_template("login.html",msg=msg)

    else:
        if "ename" in session:
            return redirect(url_for("index"))
        return render_template("login.html")
    
    
@app.route("/")
def index():
    if "ename" in session:
        return render_template("homepage.html",ename=session['ename'],password=session['password'])
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("ename",None)
    return redirect(url_for("login"))
    
@app.route('/register',methods=["POST","GET"])
def register():
    if request.method=="POST":
        fmdata=request.form
        ename=fmdata['ename']
        password=fmdata['password']
        email=fmdata['email']
        mob=fmdata['mob']
        age=fmdata['age']
        address=fmdata['address']
        branch=fmdata['branch']
        adharno=fmdata['adharno']
        balance=fmdata['balance']
        gender=fmdata['gender']
        state=fmdata['state']
        if int(balance)>1000 and len(str(abs(int(mob))))==10 and int(age)>18:
            q = "insert into customer(ename,passw,email,mob,age,address,branch,adharno,balance,gender,state) values('"+ename+"','"+password+"','"+email+"','"+mob+"','"+age+"','"+address+"','"+branch+"','"+adharno+"','"+balance+"','"+gender+"','"+state+"')"
            cursor=mysql.connection.cursor()
            cursor.execute(q)
            mysql.connection.commit()
            return render_template("login.html")
        elif int(balance)<1000:
            msg="minimum balance should be 1000"
            return render_template("register.html",msg=msg)
        elif len(str(abs(int(mob))))!=10:
            msg="mob no should be 10 digit"
            return render_template("register.html",msg=msg)
        elif int(age)<18:
            msg="minimum age should be 18"
            return render_template("register.html",msg=msg)
        
    return render_template("register.html")



@app.route('/info')
def info():
    cursor= mysql.connection.cursor()
    q = "select * from customer where ename='"+session['ename']+"' and passw='"+session['password']+"'"
    cursor.execute(q)
    res=cursor.fetchone()
    return render_template("info.html",res=res)



@app.route('/bankdetails')
def bankdetails():
    return render_template("bform.html")


@app.route('/bankregister',methods=["POST","GET"])
def bankregister():
    if request.method=="POST":
        fmdata=request.form
        ename=fmdata['ename']
        lname=fmdata['lname']
        age=fmdata['age']
        address=fmdata['address']
        branch=fmdata['branch']
        adharno=fmdata['adharno']
        ideposit=fmdata['ideposit']
        gender=fmdata['gender']
        state=fmdata['state']
        q = "insert into bankmember(ename,lname,age,address,branch,adharno,ideposit,gender,state) values('"+ename+"','"+lname+"','"+age+"','"+address+"','"+branch+"','"+adharno+"','"+ideposit+"','"+gender+"','"+state+"')"
        cursor=mysql.connection.cursor()
        cursor.execute(q)
        mysql.connection.commit()
        msg="register successfully"
        if msg:
            return render_template("bform.html",msg=msg)
        else:
            msg="incomplete info"
            return render_template("bform.html",msg=msg)

@app.route('/forgotpassword',methods=["POST","GET"])
def changepassword():
    if request.method=="POST":
        fmdata=request.form
        ename=fmdata['ename']
        email=fmdata['email']
        newpassword=fmdata['npassword']
        q1 = "select * from customer where ename='"+ename+"' and email='"+email+"'"
        cursor = mysql.connection.cursor()
        cursor.execute(q1)
        mysql.connection.commit()
        ac = cursor.fetchone()
        if ac[1]==ename and ac[3]==email:
            q = "update customer set passw='"+newpassword+"' where ename='"+ename+"' and email='"+email+"'"
            cursor=mysql.connection.cursor()
            cursor.execute(q)
            mysql.connection.commit()
            ac = cursor.fetchone()
            return render_template("forgotpass.html",msg=ac)
        elif ac[1]!=ename or ac[3]!=email:
            msg="fail"
            return render_template("forgotpass.html",msg=msg)

    return render_template("forgotpass.html")     



@app.route('/withdraw',methods=["POST","GET"])
def withdraw():
    if request.method=="POST":
        fmdata=request.form
        withdraw=fmdata['withdraw']
        ename=fmdata['ename']
        password=fmdata['password']
        q1 = "select * from customer where ename='"+ename+"' and passw='"+password+"'"
        cursor = mysql.connection.cursor()
        cursor.execute(q1)
        mysql.connection.commit()
        ac = cursor.fetchone()
        no=int(withdraw)
        curt=ac[9]
        if curt>no and no>50 :
            balan=str(curt-no)
            q = "update customer set balance='"+balan+"' where ename='"+ename+"' and passw='"+password+"'"
            cursor=mysql.connection.cursor()
            cursor.execute(q)
            mysql.connection.commit()
            msg= f"Transation successfully \n current balance is RS {balan}"
            return render_template("withdraw.html",msg=msg)
        elif curt<no:
            msg="Sorry!!! Insufficient money"
            return render_template("withdraw.html",msg=msg)
        elif no<50:
            msg="Sorry!!! minimum withdraw should be RS 50"
            return render_template("withdraw.html",msg=msg)


    return render_template("withdraw.html")



@app.route('/credit',methods=["POST","GET"])
def credit():
    if request.method=="POST":
        fmdata=request.form
        credit=fmdata['credit']
        ename=fmdata['ename']
        password=fmdata['password']
        q1 = "select * from customer where ename='"+ename+"' and passw='"+password+"'"
        cursor = mysql.connection.cursor()
        cursor.execute(q1)
        mysql.connection.commit()
        ac = cursor.fetchone()
        no=int(credit)
        curt=ac[9]
        if  no>200 :
            balan=str(curt+no)
            q = "update customer set balance='"+balan+"' where ename='"+ename+"' and passw='"+password+"'"
            cursor=mysql.connection.cursor()
            cursor.execute(q)
            mysql.connection.commit()
            msg= f"Transation successfully current balance is RS {balan}"
            return render_template("credit.html",msg=msg)
    
        elif no<200:
            msg="Sorry!!! minimum credit should be RS 200"
            return render_template("credit.html",msg=msg)

    return render_template("credit.html")



@app.route('/balane')
def balance():
    q = "select * from customer where ename='"+session['ename']+"' and passw='"+session['password']+"'"
    cursor=mysql.connection.cursor()
    cursor.execute(q)
    mysql.connection.commit()
    ac=cursor.fetchone()
    return render_template("balance.html",ac=ac)



@app.route('/modify')
def modify():
    cursor= mysql.connection.cursor()
    q = "select * from customer where ename='"+session['ename']+"' and passw='"+session['password']+"'"
    cursor.execute(q)
    res=cursor.fetchone()
    return render_template("modify.html",a=res)


@app.route('/update',methods=["POST","GET"])
def update():
    if request.method=="POST":
        fm=request.form
        ename=fm["ename"]
        email=fm["email"]
        mob=fm["mob"]
        age=fm["age"]
        address=fm["address"]
        eid=fm['eid']
        q1 = "update customer set ename='"+ename+"',email='"+email+"',mob='"+mob+"',age='"+age+"',address='"+address+"' where id='"+eid+"' "
        cursor = mysql.connection.cursor()
        cursor.execute(q1)
        mysql.connection.commit()
        a=cursor.fetchone()
        msg="Profile has been updated successfully!!"
        return render_template("modify.html",msg=msg,a=a)

  
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

app.run()