# -*- coding:utf-8 -*-

from apps.extensions import db

class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    def __repr__(self):
        return self.username
