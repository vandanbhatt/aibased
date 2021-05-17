from base import db
from base.com.vo.classification_vo import ClassificationVO
from base.com.vo.login_vo import LoginVO


class ClassificationDAO:
    def insert_classification(self, classification_vo):  # user insert the complain
        db.session.add(classification_vo)
        db.session.commit()

    def admin_view_classification(self):
        classification_vo_list = db.session.query(ClassificationVO, LoginVO).filter(
            LoginVO.login_id == ClassificationVO.classification_login_id).all()
        return classification_vo_list

    def user_view_classification(self, classification_vo):
        classification_vo_list = ClassificationVO.query.filter_by(
            classification_login_id=classification_vo.classification_login_id).all()
        return classification_vo_list
