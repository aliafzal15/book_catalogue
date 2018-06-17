from bookcat import db, bcrypt

from datetime import datetime

from bookcat import login_manager

from flask_login import UserMixin


class User(UserMixin,db.Model):

    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}


    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(30))
    user_email = db.Column(db.String(50), unique=True, index=True)
    user_password = db.Column(db.String(60))
    registration_date = db.Column(db.DateTime, default=datetime.now)


    def check_password(self,password):
        return bcrypt.check_password_hash(self.user_password, password)

    @classmethod   ## This annotation is called a decorator in python
    def create_user(cls, user, email, password):

        user = cls(user_name=user,
                   user_email=email,
                   user_password=bcrypt.generate_password_hash(password).decode('utf-8')
                   )

        db.session.add(user)
        db.session.commit()
        return user


@login_manager.user_loader    #user _loader is a call back
def load_user(id):
    return User.query.get(int(id))
