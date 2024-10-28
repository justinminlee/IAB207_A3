from . import db
from datetime import datetime
from flask_login import UserMixin

#Here we need to create Tables for the database.
#This will needs to be done before we run the application.

class User(db.Model, UserMixin):

class Event(db.Model):

class Comment(db.Model):

class Order(db.Model):