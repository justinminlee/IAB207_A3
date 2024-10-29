from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable = False)
    username = db.Column(db.String(100), index=True, unique=True, nullable=False)
    firstname = db.Column(db.String(100), index=True, nullable=False) 
    lastname = db.Column(db.String(100), index=True, nullable=False) 
    emailid = db.Column(db.String(100), index=True, nullable=False) 
    #password is encrypted in database
    password_hash = db.column(db.String(255), nullable=False)
    comments = db.relationship('Comment,', backref='User')

class Event(db.Model): 
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True, nullable = False)
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    ticketprice = db.Column(db.String(80))
    #Creates the comments 
    comments = db.relationship('Comment', backref = 'destination')

    def __rep__(self):
        return f"Name: {self.name}"
    
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    # add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    # string print method
    def __repr__(self):
        return f"Comment: {self.text}"

#class User(db.Model, UserMixin):

#class Event(db.Model):

#class Comment(db.Model):

#class Order(db.Model):