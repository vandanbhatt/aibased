from base import db
from base.com.vo.dataset_vo import DatasetVO


class DatasetDAO:
    def insert_dataset(self, dataset_vo):
        db.session.add(dataset_vo)
        db.session.commit()

    def view_dataset(self):
        dataset_vo_list = DatasetVO.query.all()
        return dataset_vo_list

    def delete_dataset(self, dataset_id):
        dataset_vo_list = DatasetVO.query.get(dataset_id)
        db.session.delete(dataset_vo_list)
        db.session.commit()
        return dataset_vo_list
