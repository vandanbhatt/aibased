import os
import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, request, flash, redirect
from werkzeug.utils import secure_filename

from base import app
from base.com.controller.login_controller \
    import admin_login_session, admin_logout_session, global_loginvo_list, admin_load_dashboard
from base.com.dao.login_dao import LoginDAO
from base.com.dao.user_dao import UserDAO
from base.com.vo.login_vo import LoginVO
from base.com.vo.user_vo import UserVO

USER_REPORT_FOLDER = 'base/static/adminResources/report/'
app.config['USER_REPORT_FOLDER'] = USER_REPORT_FOLDER


@app.route('/admin/load_user', methods=['GET'])
def admin_load_user():
    try:
        return render_template('user/addUser.html')
    except Exception as ex:
        print("in admin_load_user route exception occured>>>>>>>>>>", ex)


@app.route('/admin/insert_user', methods=['POST'])
def admin_insert_user():
    try:
        login_vo = LoginVO()
        login_dao = LoginDAO()

        user_vo = UserVO()
        user_dao = UserDAO()

        user_firstname = request.form.get('userFirstname')
        user_lastname = request.form.get('userLastname')
        user_age = request.form.get('userAge')
        user_phonenumber = request.form.get('userPhonenumber')
        user_email = request.form.get('userEmail')
        user_address = request.form.get('userAddress')
        user_gender = request.form.get('userGender')
        user_conditions = request.form.get('userConditions')
        user_painlevel = request.form.get('userPainlevel')
        user_bloodgroup = request.form.get('userBloodgroup')
        user_report = request.files.get('userReport')
        user_filename = secure_filename(user_report.filename)
        print(user_filename)
        user_filepath = os.path.join(app.config['USER_REPORT_FOLDER'])
        user_report.save(os.path.join(user_filepath, user_filename))

        login_password = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))
        print("in admin_insert_user login_password>>>>>>>>>", login_password)

        sender = "projectAImedical@gmail.com"
        receiver = user_email
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = "PYTHON PASSWORD"
        msg.attach(MIMEText(login_password, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, "@yrvv1234")
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()

        login_secretkey = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(32))
        print("in admin_insert_user login_secretkey>>>>>>>", login_secretkey)
        login_vo_list = login_dao.view_login()
        print("in admin_insert_user login_vo_list>>>>>>", login_vo_list)
        if len(login_vo_list) != 0:
            for i in login_vo_list:
                if i.login_secretkey == login_secretkey:
                    login_secretkey = ''.join(
                        (random.choice(string.ascii_letters + string.digits)) for x in range(32))
                elif i.login_username == user_email:
                    error_message = "The username is already exists !"
                    flash(error_message)
                    return redirect('/admin/load_user')

        login_vo.login_username = user_email
        login_vo.login_password = login_password
        login_vo.login_role = "user"
        login_vo.login_status = "active"
        login_vo.login_secretkey = login_secretkey
        login_dao.insert_login(login_vo)

        user_vo.user_firstname = user_firstname
        user_vo.user_lastname = user_lastname
        user_vo.user_age = user_age
        user_vo.user_phonenumber = user_phonenumber
        user_vo.user_email = user_email
        user_vo.user_address = user_address
        user_vo.user_gender = user_gender
        user_vo.user_conditions = user_conditions
        user_vo.user_painlevel = user_painlevel
        user_vo.user_bloodgroup = user_bloodgroup
        user_vo.user_filename = user_filename
        user_vo.user_filepath = user_filepath
        user_vo.user_login_id = login_vo.login_id
        user_dao.insert_user(user_vo)

        return redirect('/')
    except Exception as ex:
        print("in admin_insert_user route exception occured>>>>>>>>>>", ex)


@app.route('/admin/view_user')
def admin_view_user():
    try:
        if admin_login_session() == 'admin':
            user_dao = UserDAO()
            user_vo_list = user_dao.view_user()
            print(">>>>>>>>>>>>>>>>>>", user_vo_list)
            return render_template('admin/viewUser.html', user_vo_list=user_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print(ex)

