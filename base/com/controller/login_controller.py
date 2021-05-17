import random
import smtplib
import string
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import *

from base import app
from base.com.dao.login_dao import LoginDAO
from base.com.vo.login_vo import LoginVO

global_loginvo_list = []
global_login_secretkey_set = {0}
login_username = ""


@app.route('/', methods=['GET'])
def admin_load_login():
    try:
        return render_template('admin/login.html')
    except Exception as ex:
        print("admin_load_login route exception occured>>>>>>>>>>", ex)


@app.route("/admin/validate_login", methods=['POST'])
def admin_validate_login():
    try:
        global global_loginvo_list
        global global_login_secretkey_set

        login_username = request.form.get('loginUsername')
        login_password = request.form.get('loginPassword')
        print(login_username, login_password)
        login_vo = LoginVO()
        login_dao = LoginDAO()

        login_vo.login_username = login_username
        login_vo.login_password = login_password

        login_vo_list = login_dao.validate_login(login_vo)
        print("login_vo_list>>>>>>>>>>>>>>>>>>>>>>>>>>", login_vo_list)
        login_list = [i.as_dict() for i in login_vo_list]
        print("in admin_validate_login login_list>>>>>>>>>>>", login_list)
        len_login_list = len(login_list)
        if len_login_list == 0:
            error_message = 'username or password is incorrect !'
            flash(error_message)
            return redirect('/')
        elif login_list[0]['login_status'] == 'inactive':
            error_message = 'You have been temporarily blocked by website admin !'
            flash(error_message)
            return redirect('/')
        else:
            for row1 in login_list:
                login_id = row1['login_id']
                login_username = row1['login_username']
                login_role = row1['login_role']
                login_secretkey = row1['login_secretkey']
                login_vo_dict = {
                    login_secretkey: {'login_username': login_username, 'login_role': login_role, 'login_id': login_id}}
                if len(global_loginvo_list) != 0:
                    for i in global_loginvo_list:
                        tempList = list(i.keys())
                        global_login_secretkey_set.add(tempList[0])
                    login_secretkey_list = list(global_login_secretkey_set)
                    if login_secretkey not in login_secretkey_list:
                        global_loginvo_list.append(login_vo_dict)
                else:
                    global_loginvo_list.append(login_vo_dict)
                if login_role == 'admin':
                    response = make_response(redirect(url_for('admin_load_dashboard')))
                    response.set_cookie('login_secretkey', value=login_secretkey, max_age=timedelta(minutes=30))
                    response.set_cookie('login_username', value=login_username, max_age=timedelta(minutes=30))
                    login_secretkey = request.cookies.get('login_secretkey')
                    login_username = request.cookies.get('login_username')
                    print("in admin_validate_login login_secretkey>>>>>>>>>>>>>>>", login_secretkey)
                    print("in admin_validate_login login_username>>>>>>>>>>>>>>>", login_username)
                    return response
                elif login_role == 'user':
                    response = make_response(redirect(url_for('user_load_dashboard')))
                    response.set_cookie('login_secretkey', value=login_secretkey, max_age=timedelta(minutes=30))
                    response.set_cookie('login_username', value=login_username, max_age=timedelta(minutes=30))
                    login_secretkey = request.cookies.get('login_secretkey')
                    login_username = request.cookies.get('login_username')
                    print("in user_validate_login login_secretkey>>>>>>>>>>>>>>>", login_secretkey)
                    print("in user_validate_login login_username>>>>>>>>>>>>>>>", login_username)
                    return response
                else:
                    return redirect(url_for('admin_logout_session'))

    except Exception as ex:

        print("admin_validate_login route exception occured>>>>>>>>>>", ex)


@app.route('/admin/load_dashboard', methods=['GET'])
def admin_load_dashboard():
    try:
        if admin_login_session() == 'admin':
            return render_template('admin/index.html')
        else:
            return redirect(url_for('admin_logout_session'))
    except Exception as ex:
        print("admin_load_dashboard route exception occured>>>>>>>>>>", ex)


@app.route('/user/load_dashboard', methods=['GET'])
def user_load_dashboard():
    try:
        if admin_login_session() == 'user':
            return render_template('user/userIndex.html')
        else:
            return redirect(url_for('admin_logout_session'))
    except Exception as ex:
        print("user_load_dashboard route exception occured>>>>>>>>>>", ex)


@app.route('/admin/login_session')
def admin_login_session():
    try:
        global global_loginvo_list
        login_role_flag = ""

        login_secretkey = request.cookies.get('login_secretkey')
        print("in admin_login_session login_secretkey>>>>>>>>>", login_secretkey)

        if login_secretkey is None:
            return redirect('/')
        for i in global_loginvo_list:
            if login_secretkey in i.keys():
                if i[login_secretkey]['login_role'] == 'admin':
                    login_role_flag = "admin"
                if i[login_secretkey]['login_role'] == 'user':
                    login_role_flag = "user"

        print("after login_role_flag>>>>>>>>>>", login_role_flag)
        print("after len(login_role_flag)>>>>>>>>>>", len(login_role_flag))

        if len(login_role_flag) != 0:
            print("<<<<<<<<<<<<<<<<True>>>>>>>>>>>>>>>>>>>>")
        return login_role_flag
    except Exception as ex:
        print("admin_login_session route exception occured>>>>>>>>>>", ex)


@app.route('/admin/block_user', methods=['GET'])
def admin_block_user():
    try:
        if admin_login_session() == 'admin':
            login_vo = LoginVO()
            login_dao = LoginDAO()

            login_id = request.args.get('login_id')

            login_status = "inactive"

            login_vo.login_id = login_id

            login_vo.login_status = login_status

            login_dao.update_login(login_vo)

            return redirect(url_for('admin_view_user'))
        else:

            return admin_logout_session()
    except Exception as ex:
        print(ex)


@app.route('/admin/unblock_user', methods=['GET'])
def admin_unblock_user():
    try:
        if admin_login_session() == 'admin':
            login_vo = LoginVO()
            login_dao = LoginDAO()

            login_id = request.args.get('login_id')

            login_status = "active"

            login_vo.login_id = login_id

            login_vo.login_status = login_status

            login_dao.update_login(login_vo)

            return redirect(url_for('admin_view_user'))
        else:

            return admin_logout_session()
    except Exception as ex:
        print(ex)


@app.route("/admin/logout_session", methods=['GET'])
def admin_logout_session():
    try:
        global global_loginvo_list
        login_secretkey = request.cookies.get('login_secretkey')
        login_username = request.cookies.get('login_username')
        print("in admin_logout_session login_secretkey>>>>>>>>>", login_secretkey)
        print("in admin_logout_session login_username>>>>>>>>>", login_username)
        print("in admin_logout_session type of login_secretkey>>>>>>>>>", type(login_secretkey))
        print("in admin_logout_session type of login_username>>>>>>>>>", type(login_username))

        response = make_response(redirect('/'))
        if login_secretkey is not None and login_username is not None:
            response.set_cookie('login_secretkey', login_secretkey, max_age=0)
            response.set_cookie('login_username', login_username, max_age=0)
            print(global_loginvo_list)
            for i in global_loginvo_list:
                if login_secretkey in i.keys():
                    global_loginvo_list.remove(i)
                    print("in admin_logout_session global_loginvo_list>>>>>>>>>>>>>>>", global_loginvo_list)
                    break

        return response
    except Exception as ex:
        print("in admin_logout_session route exception occured>>>>>>>>>>", ex)






# -------------------------------------FORGET PASSWORD--------------------------------------#

@app.route('/admin/load_forget_password', methods=['GET'])
def admin_load_forget_password():
    try:
        return render_template('admin/forgetPassword.html')
    except Exception as ex:
        print("admin_load_forget_password route exception occured>>>>>>>>>>", ex)


@app.route('/admin/validate_login_username', methods=['post'])
def admin_validate_login_username():
    global login_username
    try:
        login_username = request.form.get("loginUsername")

        login_dao = LoginDAO()
        login_vo = LoginVO()

        login_vo.login_username = login_username
        login_vo_list = login_dao.login_validate_username(login_vo)
        login_list = [i.as_dict() for i in login_vo_list]
        print("in admin_validate_login_username login_list>>>>>>>>>>>", login_list)
        len_login_list = len(login_list)
        if len_login_list == 0:
            error_message = 'username is incorrect !'
            flash(error_message)
            return redirect(url_for('admin_load_forget_password'))
        else:
            for row in login_list:
                login_id = row['login_id']
                print(login_id)
                session['login_id'] = login_id
                login_username = row['login_username']
                print(login_username)
                sender = "projectAImedical@gmail.com"
                receiver = login_username
                msg = MIMEMultipart()
                msg['From'] = sender
                msg['To'] = receiver
                msg['Subject'] = "PYTHON OTP"
                otp = random.randint(1000, 9999)
                session['session_otp_number'] = otp
                message = str(otp)
                print(message)
                msg.attach(MIMEText(message, 'plain'))
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender, "@yrvv1234")
                text = msg.as_string()
                server.sendmail(sender, receiver, text)
                server.quit()
                return render_template('admin/otpPassword.html')
    except Exception as ex:
        print("admin_validate_login_username route exception occured>>>>>>>>>>", ex)


@app.route('/admin/validate_otp_number', methods=['POST'])
def admin_validate_otp_number():
    global login_username
    try:
        otp_number = int(request.form.get("otpNumber"))
        session_otp_number = session['session_otp_number']
        if otp_number == session_otp_number:
            sender = "projectAImedical@gmail.com"
            receiver = login_username
            msg = MIMEMultipart()
            msg['From'] = sender
            msg['To'] = receiver
            msg['Subject'] = "PYTHON RESET PASSWORD"
            login_password = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

            message = str(login_password)
            print(message)
            msg.attach(MIMEText(message, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender, "@yrvv1234")
            text = msg.as_string()
            server.sendmail(sender, receiver, text)
            server.quit()

            login_id = session['login_id']
            print("login_id>>>>>>>>>>>>", login_id)
            login_dao = LoginDAO()
            login_vo = LoginVO()
            login_vo.login_id = login_id
            login_vo.login_password = login_password
            login_dao.update_login(login_vo)

            return redirect('/')
        else:
            session.clear()
            error_message = 'otp is incorrect !'
            flash(error_message)
            return redirect(url_for('admin_load_forget_password'))
    except Exception as ex:
        print("admin_validate_otp_number route exception occured>>>>>>>>>>", ex)


@app.route('/admin/insert_reset_password', methods=['POST'])
def admin_insert_reset_password():
    try:
        login_password = request.form.get("loginPassword")
        print("login_password>>>>>>>>>>>>", login_password)
        login_id = session['login_id']
        print("login_id>>>>>>>>>>>>", login_id)
        login_dao = LoginDAO()
        login_vo = LoginVO()
        login_vo.login_id = login_id
        login_vo.login_password = login_password
        login_dao.update_login(login_vo)
        return redirect('/')
    except Exception as ex:
        print("admin_insert_reset_password route exception occured>>>>>>>>>>", ex)
