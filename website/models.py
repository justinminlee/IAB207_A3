from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True, nullable=False)
    firstname = db.Column(db.String(100), index=True, nullable=False) 
    lastname = db.Column(db.String(100), index=True, nullable=False) 
    emailid = db.Column(db.String(100), index=True, nullable=False) 
    #password is encrypted in database
    password_hash = db.column(db.String(255), nullable=False)
    comments = db.relationship('Comment,', backref='User')

class Event(db.Model): 
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.c
#Here we need to create Tables for the database.
#This will needs to be done before we run the application.

#class User(db.Model, UserMixin):

#class Event(db.Model):

#class Comment(db.Model):

#class Order(db.Model):