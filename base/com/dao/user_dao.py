from base import db
from base.com.vo.login_vo import LoginVO
from base.com.vo.user_vo import UserVO


class UserDAO:
    def insert_user(self, user_vo):
        print('insert Register')
        db.session.add(user_vo)
        db.session.query(UserVO).all()
        db.session.commit()

    def view_user(self):
        user_vo_list = db.session.query(UserVO, LoginVO).join(LoginVO, UserVO.user_login_id == LoginVO.login_id).all()
        return user_vo_list
