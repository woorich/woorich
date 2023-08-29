# from woorichApp import db
from flask import current_app as app

db = SQLAlchemy(app)
class Board(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    b_title = db.Column(db.String(45), nullable=False)
    b_content = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    user_no = db.Column(db.Integer, db.ForeignKey('user.no', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('board_set'))

class Reply(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    r_content = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    admin_no = db.Column(db.Integer, db.ForeignKey('Admin.no', ondelete='CASCADE'))
    board_no = db.Column(db.Integer, db.ForeignKey('Board.no', ondelete='CASCADE'))
    board = db.relationship('Board', backref=db.backref('reply'))
    admin = db.relationship('Admin', backref=db.backref('reply_set'))

class Admin(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.String(45), unique=True, nullable=False)
    admin_pw = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    reply = db.relationship('Reply', backref=db.backref('admin_set'))

class User(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(45), unique=True, nullable=False)
    user_pw = db.Column(db.String(45), nullable=False)
    username = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    phone = db.Column(db.String(45), unique=True, nullable=False)
    address = db.Column(db.String(45), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class History(db.Model):
    no = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(45), nullable=False)
    job_type = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    user_no = db.Column(db.Integer, db.ForeignKey('user.no', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('history_set'))

# class Userinfo(db.Model):
#     no = db.Column(db.Integer, primary_key=True)
#     user_no = db.Column(db.Integer, db.ForeignKey('user.no', ondelete='CASCADE'), nullable=False)
#     age = db.Column(db.Integer, nullable=False)
#     job = db.Column(db.String(45), nullable=False)
#     marital = db.Column(db.Integer, nullable=False)
#     education = db.Column(db.String(45), nullable=False)
#     default = db.Column(db.Integer, nullable=False)
#     housing = db.Column(db.Integer, nullable=False)
#     loan = db.Column(db.Integer, nullable=False)
#     balance = db.Column(db.Integer, nullable=False)



