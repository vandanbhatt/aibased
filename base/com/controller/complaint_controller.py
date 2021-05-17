from datetime import datetime

from flask import *

from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.dao.complaint_dao import ComplaintDAO
from base.com.dao.login_dao import LoginDAO
from base.com.vo.complaint_vo import ComplaintVO
from base.com.vo.login_vo import LoginVO


@app.route('/admin/view_complaint')
def admin_view_complaint():
    try:
        if admin_login_session() == "admin":
            complaint_dao = ComplaintDAO()
            complaint_vo_list = complaint_dao.admin_view_complaint()
            print(complaint_vo_list)
            return render_template('admin/viewComplaint.html', complaint_vo_list=complaint_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_complaint route exception occured>>>>>>>>>>", ex)


@app.route("/admin/delete_complaint")
def admin_delete_complaint():
    try:
        if admin_login_session() == 'admin':
            complaint_vo = ComplaintVO()
            complaint_dao = ComplaintDAO()

            complaint_id = request.args.get("complaintId")
            print(complaint_id)

            complaint_vo.complaint_id = complaint_id
            complaint_dao.delete_complaint(complaint_vo)

            return redirect(url_for("admin_view_complaint"))
        else:
            return admin_logout_session()
    except Exception as ex:
        print('admin_delete_complaint route error occured>>>>>>>>>>', ex)


@app.route('/admin/load_complaint_reply')
def admin_load_complaint_reply():
    try:
        if admin_login_session() == "admin":
            complaint_vo = ComplaintVO()
            complaint_vo.complaint_id = request.args.get('complaintId')
            complaint_dao = ComplaintDAO()
            complaint_vo_list = complaint_dao.edit_complaint(complaint_vo)
            print("complain_vo_list>>>>>", complaint_vo_list)
            return render_template('admin/addReplyComplaint.html', complaint_vo_list=complaint_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_complaint_reply route exception occured>>>>>>>>>>", ex)


@app.route("/admin/insert_complaint_reply", methods=["POST"])
def admin_complaint_replied():
    try:
        if admin_login_session() == "admin":
            complaint_vo = ComplaintVO()
            complaint_dao = ComplaintDAO()
            login_vo = LoginVO()
            login_dao = LoginDAO()

            login_vo.login_username = request.cookies.get('login_username')
            login_id = login_dao.find_login_id(login_vo)

            complaint_id = request.form.get("complaintId")
            complaint_vo.complaint_reply_description = request.form.get("complaintReplyDescription")
            complaint_vo.complaint_reply_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            complaint_vo.complaint_status = "Replied"
            complaint_vo.complaint_to_login_id = login_id
            complaint_vo.complaint_id = complaint_id
            complaint_dao.update_complaint(complaint_vo)

            return redirect(url_for("admin_view_complaint"))
        else:
            return admin_login_session()
    except Exception as ex:
        print("amin_complaint_replied route error occured>>>>>", ex)


@app.route('/user/insert_complaint', methods=['POST'])
def user_insert_complaint():
    try:
        if admin_login_session() == "user":
            login_vo = LoginVO()
            login_dao = LoginDAO()

            login_vo.login_username = request.cookies.get('login_username')
            user_login_id = login_dao.find_login_id(login_vo)
            complaint_dao = ComplaintDAO()
            complaint_vo = ComplaintVO()

            complaint_subject = request.form.get('complaintSubject')
            complaint_description = request.form.get('complaintDescription')

            complaint_vo.complaint_subject = complaint_subject
            complaint_vo.complaint_description = complaint_description
            complaint_vo.complaint_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            complaint_vo.complaint_status = 'pending'
            complaint_vo.complaint_from_login_id = user_login_id
            complaint_dao.insert_complaint(complaint_vo)
            return redirect('/user/view_complaint')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("in user_insert_complaint route exception occured>>>>>>>>>>", ex)


@app.route("/user/view_complaint")  # fetch all the data of complain and admin reply
def user_view_complaint():
    try:
        if admin_login_session() == 'user':
            complaint_dao = ComplaintDAO()
            complaint_vo = ComplaintVO()
            login_vo = LoginVO()
            login_dao = LoginDAO()

            login_vo.login_username = request.cookies.get('login_username')
            user_login_id = login_dao.find_login_id(login_vo)
            complaint_vo.complaint_from_login_id = user_login_id
            complaint_vo_updated_list = []
            complaint_vo_list = complaint_dao.user_view_complaint()
            print("complaint_vo_list=", complaint_vo_list)
            if len(complaint_vo_list) != 0:
                for index in range(len(complaint_vo_list)):
                    if user_login_id == complaint_vo_list[index][1].complaint_from_login_id:
                        complaint_vo_updated_list.append(complaint_vo_list[index])
                if len(complaint_vo_updated_list) == 0:
                    return render_template("user/addComplaint.html", complaint_vo_updated_list=None)
                else:
                    admin_login_username = None
                    for index in range(len(complaint_vo_updated_list)):
                        if complaint_vo_updated_list[index][1].complaint_to_login_id is not None:
                            print("complaint_vo_updated_list[0][1].complaint_to_login_id", complaint_vo_updated_list)
                            admin_login_id = complaint_vo_updated_list[index][1].complaint_to_login_id
                            print("admin_login_id=", admin_login_id)
                            admin_login_vo = LoginVO()
                            admin_login_vo.login_id = admin_login_id
                            admin_login_username = login_dao.find_login_username(admin_login_vo)
                            print("admin_login_username=", admin_login_username)
                    return render_template("user/addComplaint.html",
                                           complaint_vo_updated_list=complaint_vo_updated_list,
                                           admin_login_username=admin_login_username)
            else:
                return render_template("user/addComplaint.html", complaint_vo_updated_list=None)
        else:
            return admin_logout_session()

    except Exception as ex:
        print("in user_view_complaint route exception occured>>>>>>>>>>", ex)
