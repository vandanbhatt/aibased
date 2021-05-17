from flask import *

from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session


@app.route('/user/user_aboutus')
def user_aboutus():
    try:
        if admin_login_session() == "user":
            return render_template('user/aboutUS.html')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_load_home route exception occured>>>>>>>>>>", ex)
