from base import db
from base.com.vo.complaint_vo import ComplaintVO
from base.com.vo.login_vo import LoginVO


class ComplaintDAO:
    def insert_complaint(self, complaint_vo):  # user insert the complain
        db.session.add(complaint_vo)
        db.session.commit()

    def user_view_complaint(self):  # admin side view the all complain
        complaint_vo_list = db.session.query(LoginVO, ComplaintVO) \
            .filter(LoginVO.login_id == ComplaintVO.complaint_from_login_id) \
            .all()
        return complaint_vo_list

    def admin_view_complaint(self):  # admin side view the all complain
        complaint_vo_list = db.session.query(ComplaintVO, LoginVO) \
            .join(LoginVO, ComplaintVO.complaint_from_login_id == LoginVO.login_id) \
            .all()
        return complaint_vo_list

    def delete_complaint(self, complaint_vo):  # admin delete the complain
        complaint_vo_delete = ComplaintVO.query.get(complaint_vo.complaint_id)
        db.session.delete(complaint_vo_delete)
        db.session.commit()

    def edit_complaint(self, complaint_vo):  # admin give the reply of complain ,fetch the complain data
        complaint_vo_list = ComplaintVO.query.get(complaint_vo.complaint_id)
        return complaint_vo_list

    def update_complaint(self, complaint_vo):  # update data into complain table
        db.session.merge(complaint_vo)
        db.session.commit()
