#!/myenv/Scripts/python.exe
## import Library
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL 
import MySQLdb.cursors
import re

## import Class
from server.security import Security
from server.read_db import Read_DB

## app config
app = Flask(__name__, static_url_path='', static_folder='../client/static', template_folder='../client/templates')
app.secret_key = '8e422c119fcc0bdb1e78777d4febaaf7'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

## Intialize MySQL
mysql = MySQL(app)
db_text = Read_DB()

@app.route("/sign-in/", methods=['GET', 'POST'])
def sign_in():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        security = Security()
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM tbluser WHERE username = "%s"' % username)
            account = cursor.fetchone()
            if security.check_password(account['password'], password):
                session['loggedin'] = True 
                session['userid'] = account['userid']
                session['username'] = account['username']
                return redirect(url_for('home'))
            else:
                msg = 'Incorrect username/password!'
        except:
            msg = 'Incorrect username/password!'
        
    return render_template('index.html', msg=msg)

@app.route('/sign-up')
def sign_up():
    return render_template('404.html'), 404

@app.route('/log-out')
def log_out():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('username', None)
    return redirect(url_for('sign_in'))

@app.route('/')
def home():
    if 'loggedin' in session:
        data = db_text.read_txt('db_log.txt')
        return render_template('home.html', username=session['username'], data=data)
    return redirect(url_for('sign_in'))

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tbluser WHERE userid = "%s"' % (session['userid']))
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('sign_in'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

app.run(debug=True)
