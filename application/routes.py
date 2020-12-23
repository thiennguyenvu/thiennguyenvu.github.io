from flask import render_template, flash, redirect, url_for, request
from application import app, db, file_manager
from application.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from application.models import User
from werkzeug.urls import url_parse
from datetime import datetime, date
import os.path
import pandas as pd
import xlsxwriter
import xlrd
import openpyxl

brand = 'Thien\'s Website'
now = datetime.utcnow()

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
        user = User(username=form.username.data, email=form.email.data,
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
    return render_template('profile.html', brand=brand, title='Profile',
                           user=user, posts=posts)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/diagram')
@login_required
def diagram():
    filename = 'test'
    path = app.static_folder + '/excel/' + filename

    data = file_manager.FileManagement()
    data.writeTXTFile(path + '.xlsx', 'Sheet',
                      path.replace('/excel/', '/txt/') + '.txt')
    data.readExcelFile(path + '.xlsx', 'Sheet')
    data_json = data.convertToJSON()
    data.writeJSONFile(path + '.json', data_json)

    return render_template('diagram.html', brand=brand, title='Diagram')


@app.route('/demo-app', methods=['GET', 'POST'])
def demo_app():
    # Get data on server
    path = app.static_folder + '/excel/'
    message = ''

    model_data = pd.read_excel(path + 'Database.xlsx', 'Model')
    dict_model = model_data.to_dict()
    department = pd.read_excel(path + 'Database.xlsx', 'Department')
    dict_dept = department.to_dict()
    line_data = pd.read_excel(path + 'Database.xlsx', 'Line')
    dict_line = line_data.to_dict()

    # Get data Log file
    dict_log = ''
    if os.path.isfile(path + 'Log.xlsx'):
        log_data = pd.read_excel(path + 'Log.xlsx', 'Sheet1')
        dict_log = log_data.to_dict()

    if request.method == 'POST':
        if 'form-plan' in request.form:
            # Handle data form
            data = {}
            log_name = 'Log.xlsx'
            log_writer = pd.ExcelWriter(path + log_name, engine='xlsxwriter')
            log_df_head = pd.DataFrame(
                columns=['Date', 'Time', 'Department', 'Line', 'Model', 'Plan', 'File Name'])

            start = 0
            count = 0
            pause = 0
            time = datetime.now().strftime('%H:%M:%S')
            timestamp = datetime.now().timestamp()
            my_date = date.today().strftime('%Y-%m-%d')
            dept = request.form.get('department')
            line = request.form.get('line')
            model = request.form.get('model')
            plan = int(request.form.get('plan'))
            version = request.form.get('version')
            per_plan = 0 if (count == 0) else plan/count
            st = 0
            for i in dict_model['Model']:
                if (dict_model['Model'][i] == model):
                    st = dict_model[dept][i]

            nonspace_model = model.replace(' ', '-')
            filename = str(my_date) + '_' + dept + '_' + line + '_' + nonspace_model \
                                    + '_' + str(plan) + '_ver' + \
                version + '.xlsx'

            data['Start/Stop'] = start
            data['Count'] = count
            data['Pause/Continue'] = pause
            data['Time'] = time
            data['Date'] = my_date
            data['Department'] = dept
            data['Line'] = line
            data['Model'] = model
            data['Plan'] = plan
            data['% Plan'] = per_plan
            data['% ST'] = st
            data['Timestamp'] = timestamp
            # print(data)

            # Check exist log file
            if not os.path.isfile(path + log_name):
                # Create new log file
                log_df_head.to_excel(
                    log_writer, sheet_name='Sheet1', index=False)
                log_writer.save()

            # Check exists data file
            if os.path.isfile(path + filename):
                # Show warning message
                message = '<b>You have a previous version of this plan. \
                    <br>Please change different version and try again.</b>'
                return render_template('demo.html', brand=brand, title='Demo App',
                                        data=dict_model, department=dict_dept,
                                       line=dict_line, msg=message, log=dict_log, now=now)
            else:
                # Create new data file
                message = ''
                writer = pd.ExcelWriter(path + filename, engine='openpyxl')
                df = pd.DataFrame([data])
                df.to_excel(writer, sheet_name='Sheet1', index=False)
                writer.save()

                # Insert data in log file
                log_df = pd.read_excel(path + log_name, header=None)
                last_row = len(log_df) + 1
                log_workbook = openpyxl.load_workbook(filename=path+log_name)
                log_sheet = log_workbook.active

                log_sheet['A' + str(last_row)] = my_date
                log_sheet['B' + str(last_row)] = time
                log_sheet['C' + str(last_row)] = dept
                log_sheet['D' + str(last_row)] = line
                log_sheet['E' + str(last_row)] = model
                log_sheet['F' + str(last_row)] = plan
                log_sheet['G' + str(last_row)] = filename

                log_workbook.save(filename=path+log_name)

            return render_template('demo.html', brand=brand, title='Demo App',
                                data=dict_model, department=dict_dept,
                                   line=dict_line, msg=message, log=dict_log, now=now)
       
        elif 'form-history' in request.form:
            # Filter data
            #selected_date = request.form.get('date-history')

            return render_template('demo.html', brand=brand, title='Demo App',
                                   data=dict_model, department=dict_dept,
                                   line=dict_line, msg=message, log=dict_log, now=now)
            pass

    return render_template('demo.html', brand=brand, title='Demo App',
                           data=dict_model, department=dict_dept,
                           line=dict_line, msg=message, log=dict_log, now=now)
