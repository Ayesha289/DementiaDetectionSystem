from . import db 
import jwt
from time import time
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from sqlalchemy.sql import func
import os

class MedHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    visit = db.Column(db.Integer)
    mr_delay = db.Column(db.Integer)
    gender = db.Column(db.Integer)
    age = db.Column(db.Integer)
    edu = db.Column(db.Integer)
    ses = db.Column(db.Float)
    mmse = db.Column(db.Float)
    cdr = db.Column(db.Float)
    etiv = db.Column(db.Integer)
    nwbv = db.Column(db.Float)
    asf = db.Column(db.Float)
    result = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name= db.Column(db.String(150))
    notes = db.relationship('MedHistory')

    def get_reset_token(self, expires=300):
        return jwt.encode({'reset_password': self.email, 'exp': time() + expires},
                           key=os.getenv('SECRET_KEY'),algorithm="HS256")
    
    def set_password(self, password, commit=False):
        self.password = generate_password_hash(password)
        if commit:
            db.session.commit()

    @staticmethod
    def verify_reset_token(token):
        try:
            email = jwt.decode(token, key=os.getenv('SECRET_KEY'), algorithms=["HS256"])['reset_password']
            print(email)
        except Exception as e:
            print(e)
            return
        return User.query.filter_by(email=email).first()