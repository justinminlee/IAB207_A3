from flask import Blueprint, request, render_template, redirect, url_for, flash
from .models import Event, Comment, Booking  # Ensure Booking is added in models
from .forms import EventForm, UpdateEventForm, CancelEvent, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import datetime

# Define the event blueprint
eventbp = Blueprint('event', __name__, url_prefix='/event')

# Route to create new events
@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = EventForm()
    if form.validate_on_submit():
        # Securely save uploaded file and get the database path
        db_file_path = check_file_uploaded(form)
        # Create a new Event object
        event = Event(
            name=form.name.data,
            description=form.description.data,
            image=db_file_path,  # Store image path in database
            price=form.price.data,
            location=form.location.data,
            datetime=datetime.strptime(form.datetime.data, '%d/%m/%Y %I:%M %p'),
            capacity=form.capacity.data,
            category=form.category.data,
            status='Open',  # Default status
            user_id=current_user.id
        )
        # Add and commit the new event to the database
        db.session.add(event)
        db.session.commit()
        flash("New Event Created Successfully", 'success')
        return redirect(url_for('main.index'))  # Redirect to the homepage or event listing
    return render_template('create-event.html', form=form)  # Specify the correct template

# Route to show event details, including comments
@eventbp.route('/<int:id>')
def show(id):
    # Retrieve the event by ID
    event = db.session.get(Event, id)
    if not event:
        flash("Event not found.", "error")
        return redirect(url_for('main.index'))
    
    form = CommentForm()
    comments = Comment.query.filter_by(event_id=id).all()  # Fetch comments related to this event
    return render_template('event-details.html', event=event, form=form, comments=comments)  # Render event details

# Helper function to handle file upload securely
def check_file_uploaded(form):
    file = form.image.data
    filename = secure_filename(file.filename)
    upload_path = os.path.join('static/img', filename)  # Save to static/img folder
    file.save(upload_path)
    return f'/static/img/{filename}'  # Path to save in the database

# Route to add comments to an event
@eventbp.route('/<int:id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()
    if form.validate_on_submit():
        event = db.session.get(Event, id)
        if not event:
            flash("Event not found.", "error")
            return redirect(url_for('main.index'))
        
        # Create a Comment object
        new_comment = Comment(
            text=form.text.data,
            event_id=event.id,
            user_id=current_user.id,
            timestamp=datetime.now()  # Store comment timestamp
        )
        # Add and commit the comment to the database
        db.session.add(new_comment)
        db.session.commit()
        flash("Comment posted successfully.", "success")
    return redirect(url_for('event.show', id=id))

# Additional routes to handle booking, updating, and canceling events

# Route to book tickets for an event
@eventbp.route('/<int:id>/book', methods=['POST'])
@login_required
def book(id):
    event = db.session.get(Event, id)
    # Check if the event is open and has capacity
    if event.status == 'Open' and event.capacity > 0:
        # Update booking capacity and save a Booking record
        event.capacity -= 1
        if event.capacity == 0:
            event.status = 'Sold Out'
        booking = Booking(user_id=current_user.id, event_id=event.id, quantity=1)  # Adjust as needed
        db.session.add(booking)
        db.session.commit()
        flash("Successfully booked the event!", "success")
    else:
        flash("Event is not available for booking.", "error")
    return redirect(url_for('event.show', id=id))

# Route to update an existing event (accessible to event owner only)
@eventbp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    event = db.session.get(Event, id)
    if event.user_id != current_user.id:
        flash("You do not have permission to update this event.", "error")
        return redirect(url_for('event.show', id=id))

    form = UpdateEventForm(obj=event)
    if form.validate_on_submit():
        form.populate_obj(event)
        db.session.commit()
        flash("Event updated successfully.", "success")
        return redirect(url_for('event.show', id=id))
    return render_template('create-event.html', form=form)

# Route to cancel an event (accessible to event owner only)
@eventbp.route('/<int:id>/cancel', methods=['POST'])
@login_required
def cancel(id):
    event = db.session.get(Event, id)
    if event.user_id == current_user.id:
        event.status = 'Cancelled'
        db.session.commit()
        flash("Event cancelled successfully.", "success")
    else:
        flash("You do not have permission to cancel this event.", "error")
    return redirect(url_for('event.show', id=id))
