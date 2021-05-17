import os
from datetime import datetime

import cv2
import imutils
import keras.backend as k
import numpy as np
from flask import render_template, redirect, request
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from werkzeug.utils import secure_filename

from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.dao.classification_dao import ClassificationDAO
from base.com.dao.login_dao import LoginDAO
from base.com.vo.classification_vo import ClassificationVO
from base.com.vo.login_vo import LoginVO


@app.route('/user/load_classification')
def user_load_classification():
    try:
        if admin_login_session() == "user":
            return render_template('user/addClassification.html')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("user_load_classification route exception occured>>>>>>>>>>", ex)


@app.route("/user/insert_classification", methods=['POST'])
def user_insert_classification():
    try:
        if admin_login_session() == 'user':
            global classification_status
            input_filepath = "base/static/adminResources/input_image/"
            input_image = request.files.get('xrayImage')
            input_filename = secure_filename(input_image.filename)
            input_image.save(os.path.join(input_filepath, input_filename))
            output_filename = "output_" + input_filename
            input_file = input_filepath + input_filename
            modelName = "base/static/adminResources/model/knee.model"

            image = cv2.imread(r"{}".format(input_file))
            orig = image.copy()
            image = cv2.resize(image, (28, 28))
            image = image.astype("float") / 255.0
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)
            model = load_model(modelName)
            (replace_not_require, replace_require) = model.predict(image)[0]
            k.clear_session()
            detection_status = "replacement_required" if replace_require > replace_not_require else "replacement_not_required"
            accuracy = replace_require if replace_require > replace_not_require else replace_not_require
            detection_accuracy = "{:.2f}%".format(accuracy * 100)
            detection_output = "{} {}".format(detection_status, detection_accuracy)
            output = imutils.resize(orig, width=400)
            if accuracy == replace_not_require:
                classification_status = "Not Required"
                cv2.putText(output, detection_output, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.imshow("Output", output)
                output_filepath = "base/static/adminResources/output_image/replace_not_require/"
                output_file = output_filepath + output_filename
                cv2.imwrite(r"{}".format(output_file), output)
            else:
                classification_status = "Not Required"
                cv2.putText(output, detection_output, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.imshow("Output", output)
                output_filepath = "base/static/adminResources/output_image/replace_require/"
                output_file = output_filepath + output_filename
                cv2.imwrite(r"{}".format(output_file), output)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()

            login_vo = LoginVO()
            login_dao = LoginDAO()

            login_vo.login_username = request.cookies.get('login_username')
            print(login_vo.login_username)
            user_login_id = login_dao.find_login_id(login_vo)

            classification_vo = ClassificationVO()
            classification_dao = ClassificationDAO()

            classification_vo.classification_input_filename = input_filename
            classification_vo.classification_input_filepath = input_filepath.replace("base", "..")
            classification_vo.classification_output_filename = output_filename
            classification_vo.classification_output_filepath = output_filepath.replace("base", "..")
            classification_vo.classification_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            classification_vo.classification_status = classification_status
            classification_vo.classification_login_id = user_login_id
            classification_dao.insert_classification(classification_vo)
            return redirect("/user/view_classification")

        else:
            return admin_logout_session()
    except Exception as ex:
        print("in user_insert_classification route exception occured>>>>>>>>>>", ex)


@app.route('/admin/view_classification')
def admin_view_classification():
    try:
        if admin_login_session() == "admin":
            classification_dao = ClassificationDAO()
            classification_vo_list = classification_dao.admin_view_classification()
            return render_template('admin/viewClassification.html', classification_vo_list=classification_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_classification route exception occured>>>>>>>>>>", ex)


@app.route('/user/view_classification')
def user_view_classification():
    try:
        if admin_login_session() == "user":
            login_vo = LoginVO()
            login_dao = LoginDAO()
            login_vo.login_username = request.cookies.get('login_username')
            login_id = login_dao.find_login_id(login_vo)
            classification_vo = ClassificationVO()
            classification_dao = ClassificationDAO()
            classification_vo.classification_login_id = login_id
            classification_vo_list = classification_dao.user_view_classification(classification_vo)
            return render_template('user/viewClassification.html', classification_vo_list=classification_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("user_view_classification route exception occured>>>>>>>>>>", ex)
