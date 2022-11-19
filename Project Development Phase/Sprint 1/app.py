from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re
app = Flask(__name__)

app.secret_key = 'a'


conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=3883e7e4-18f5-4afe-be8c-fa31c41761d2.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=31498;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=tvy96317;PWD=jXY7SrIQGCauusOf", '', '')


@app.route('/')
def home():
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global userid
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username=? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid = account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in successfully !'

            return render_template('dashboard.html', msg=msg)
        else:
            msg = 'Incorrect username/password !'
    return render_template('login.html', msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        else:
            insert_sql = "INSERT INTO  users VALUES (?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2, password)
            ibm_db.execute(prep_stmt)
            msg = 'You have successfully registered !'
            return render_template('login.html')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


# @app.route('/dashboard')
# def dash():
#     return render_template('dashboard.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    global userid
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        file = request.form['file']
        sql = "INSERT INTO  data VALUES (?, ?)"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, file)
        ibm_db.execute(stmt)

    return render_template('dashboard.html', msg=msg)


@app.route('/dashboardAdd', methods=['GET', 'POST'])
def dashboardAdd():
    global userid
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        empId = request.form['empId']
        envSatisfaction = request.form['envSatisfaction']
        wlbalance = request.form['wlbalance']
        age = request.form['age']
        attrition = request.form['attrition']
        businessTravel = request.form['businessTravel']
        dept = request.form['dept']
        distancefromhone = request.form['distancefromhone']
        education = request.form['education']
        educationField = request.form['educationField']
        gender = request.form['gender']
        jobLevel = request.form['jobLevel']
        status = request.form['status']
        income = request.form['income']
        sql = "INSERT INTO  fields VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, empId)
        ibm_db.bind_param(stmt, 3, envSatisfaction)
        ibm_db.bind_param(stmt, 4, wlbalance)
        ibm_db.bind_param(stmt, 5, age)
        ibm_db.bind_param(stmt, 6, attrition)
        ibm_db.bind_param(stmt, 7, businessTravel)
        ibm_db.bind_param(stmt, 8, dept)
        ibm_db.bind_param(stmt, 9, distancefromhone)
        ibm_db.bind_param(stmt, 10, education)
        ibm_db.bind_param(stmt, 11, educationField)
        ibm_db.bind_param(stmt, 12, gender)
        ibm_db.bind_param(stmt, 13, jobLevel)
        ibm_db.bind_param(stmt, 14, status)
        ibm_db.bind_param(stmt, 15, income)
        ibm_db.execute(stmt)

    return render_template('dashboard.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
