from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Storage(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    price = db.Column(db.Float)
    type = db.Column(db.String(15))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    data_generated = db.Column(db.Float)
    price = db.Column(db.Float)
    lifetime = db.Column(db.Float)
    start_date = db.Column(db.String(15))
    initial_size = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    histories = db.relationship('History')
    storage = db.relationship('Storage')
