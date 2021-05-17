import os
from datetime import datetime

from flask import request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

from base import app
from base.com.controller.login_controller import admin_login_session, admin_logout_session
from base.com.dao.dataset_dao import DatasetDAO
from base.com.vo.dataset_vo import DatasetVO

DATASET_FOLDER = 'base/static/adminResources/dataset/'

app.config['DATASET_FOLDER'] = DATASET_FOLDER


@app.route('/admin/load_dataset')
def admin_load_dataset():
    try:
        if admin_login_session() == "admin":
            return render_template('admin/addDataset.html')
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_load_home route exception occured>>>>>>>>>>", ex)


@app.route('/admin/insert_dataset', methods=['POST'])
def admin_insert_dataset():
    try:
        dataset_description = request.form.get('datasetDescription')
        dataset_image = request.files.get('datasetImage')

        dataset_filename = secure_filename(dataset_image.filename)
        dataset_filepath = os.path.join(app.config['DATASET_FOLDER'])
        dataset_image.save(os.path.join(dataset_filepath, dataset_filename))

        dataset_vo = DatasetVO()
        dataset_dao = DatasetDAO()

        dataset_vo.dataset_description = dataset_description
        dataset_vo.dataset_filename = dataset_filename
        dataset_vo.dataset_filepath = dataset_filepath.replace("base", "..")
        dataset_vo.dataset_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dataset_dao.insert_dataset(dataset_vo)
        return redirect(url_for('admin_view_dataset'))
    except Exception as ex:
        print("admin_insert_dataset route exception occured>>>>>>>>>>", ex)


@app.route('/admin/view_dataset')
def admin_view_dataset():
    try:
        if admin_login_session() == "admin":
            dataset_dao = DatasetDAO()
            dataset_vo_list = dataset_dao.view_dataset()
            return render_template('admin/viewDataset.html', dataset_vo_list=dataset_vo_list)
        else:
            return admin_logout_session()
    except Exception as ex:
        print("admin_view_dataset route exception occured>>>>>>>>>>", ex)


@app.route('/admin/delete_dataset', methods=['GET'])
def admin_delete_dataset():
    try:
        dataset_dao = DatasetDAO()
        dataset_id = request.args.get('datasetId')
        # dataset_vo=DatasetVO()
        # dataset_vo.dataset_id = dataset_id
        dataset_vo_list = dataset_dao.delete_dataset(dataset_id)
        filepath = os.path.join(
            dataset_vo_list.dataset_filepath.replace("..", "base") + dataset_vo_list.dataset_filename)
        os.remove(filepath)
        return redirect('admin/view_dataset')

    except Exception as ex:
        print("admin_delete_dataset route exception occured>>>>>>>>>>", ex)
