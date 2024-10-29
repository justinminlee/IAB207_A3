from . import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Enum

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True, nullable=False)
    firstname = db.Column(db.String(100), index=True, nullable=False) 
    lastname = db.Column(db.String(100), index=True, nullable=False) 
    emailid = db.Column(db.String(100), index=True, nullable=False) 
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Relationships
    comments = db.relationship('Comment', backref='user', lazy=True)
    order = db.relationship('Order', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Event(db.Model): 
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(150), nullable=False)  # Store path to the image
    price = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(150), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    status = db.Column(
        Enum(
            'Open', 'Inactive', 'Cancelled','Sold out', name='status of event'
        ),
        default='Open',
        nullable=False)
    
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comments = db.relationship('Comment', backref='event', lazy=True)
    order = db.relationship('Order', backref='event', lazy=True)
    
    def __repr__(self):
        return f'<Event {self.name}>'

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable = False)
    total_price = db.Column(db.Float, nullable = False)
    booked_date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)