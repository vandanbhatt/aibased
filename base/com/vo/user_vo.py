from base import db
from base.com.vo.login_vo import LoginVO


class UserVO(db.Model):
    __tablename__ = 'user_table'

    user_id = db.Column('user_id', db.Integer, primary_key=True, autoincrement=True)
    user_firstname = db.Column('user_firstname', db.String(100), nullable=False)
    user_lastname = db.Column('user_lastname', db.String(100), nullable=False)
    user_age = db.Column('user_age', db.String(100), nullable=False)
    user_phonenumber = db.Column('user_phonenumber', db.String(100), nullable=False)
    user_email = db.Column('user_email', db.String(100), nullable=False)
    user_address = db.Column('user_address', db.String(100), nullable=False)
    user_gender = db.Column('user_gender', db.String(100), nullable=False)
    user_conditions = db.Column('user_conditions', db.String(100), nullable=False)
    user_painlevel = db.Column('user_painlevel', db.String(100), nullable=False)
    user_bloodgroup = db.Column('user_bloodgroup', db.String(100), nullable=False)
    user_filename = db.Column('user_filename', db.String(255), nullable=False)
    user_filepath = db.Column('user_filepath', db.String(255), nullable=False)
    user_login_id = db.Column('user_login_id', db.Integer, db.ForeignKey(LoginVO.login_id))

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'user_firstname': self.user_firstname,
            'user_lastname': self.user_lastname,
            'user_age': self.user_age,
            'user_phonenumber': self.user_phonenumber,
            'user_email': self.user_email,
            'user_address': self.user_address,
            'user_gender': self.user_gender,
            'user_condition': self.user_conditions,
            'user_painlevel': self.user_painlevel,
            'user_bloodgroup': self.user_bloodgroup,
            'user_filename': self.user_filename,
            'user_filepath': self.user_filepath,
            'user_login_id': self.user_login_id
        }


db.create_all()
