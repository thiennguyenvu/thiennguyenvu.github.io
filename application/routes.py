from flask import render_template, flash, redirect, url_for, request
from application import app, db
from application.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from application.models import User
from werkzeug.urls import url_parse
from datetime import datetime
from application.custom import ProcessFile

brand = 'Thien\'s Website'
@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:    
        return render_template('index.html', brand=brand)
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return render_template('index.html', brand=brand, form=form)
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('index.html', brand=brand, form=form)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
    
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         # next_page = request.args.get('next')
#         # if not next_page or url_parse(next_page).netloc != '':
#         #     next_page = url_for('index')
#         # return redirect(url_for('next_page'))
#         return redirect(url_for('index'))
#     return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, \
                    fullname=form.fullname.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.html', brand=brand, form=form)

@app.route('/log_out')
def log_out():
    logout_user()
    return redirect(url_for('index'))

@app.route('/charts')
@login_required
def charts():
    return render_template('charts.html', brand=brand, title='Charts')

@app.route('/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first_or_404()
    posts = [
        {'author': uname, 'body': 'Bài viết #1'},
        {'author': uname, 'body': 'Bài viết #2'}
    ]
    return render_template('profile.html', brand=brand, title='Profile', \
                           user=user, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/interface-charts')
def interface_charts():
    pf = ProcessFile()
    json_str = pf.ExceltoJSON()
    return render_template('interface-charts.html', brand=brand, \
                                                    title='Test Data Chart', \
                                                    json_str = json_str
                                                    )
