from flask import Blueprint, request, render_template, redirect, url_for, flash
from .models import Event, Comment, Order  # Ensure Booking is added in models
from .forms import EventForm, UpdateEventForm, CancelEvent, CommentForm, BookingForm
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
    print('Method', request.method)
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
            datetime=form.datetime.data,
            capacity=form.capacity.data,
            category=form.category.data,
            status='Open',  # Default status
            user_id=current_user.id
        )
        print('Method', request.method)
        # Add and commit the new event to the database
        db.session.add(event)
        db.session.commit()
        flash("New Event Created Successfully", 'success')
        return redirect(url_for('event.create'))  # Redirect to the homepage or event listing
    return render_template('event/create-event.html', form=form)  # Specify the correct template

# Route to show event details, including comments
@eventbp.route('/<int:id>')
def show(id):
    # Retrieve the event by ID
    event = db.session.scalar(db.Select(Event).where(Event.id == id))
    if not event:
        flash("Event not found.", "error")
        return redirect(url_for('main.index'))
    
    form = CommentForm()
    comments = Comment.query.filter_by(event_id=id).all()  # Fetch comments related to this event
    return render_template('event/event-details.html', event=event, form=form, comments=comments)  # Render event details

# Helper function to handle file upload securely
def check_file_uploaded(form):
    fp = form.image.data
    filename = fp.filename
    BASE_PATH = os.path.dirname(__file__)
    upload_path = os.path.join(BASE_PATH, 'static/img', secure_filename(filename))
    db_upload_path = '/static/img/' + secure_filename(filename)
    fp.save(upload_path)  # Save the file to the specified path
    return db_upload_path  # Return the database path to store the image

# Route to add comments to an event
@eventbp.route('/<int:id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()
    
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    
    if form.validate_on_submit():
        new_comment = Comment(
            text=form.text.data,
            event_id=event.id,
            user_id=current_user.id,
            timestamp=datetime.now()  # Store comment timestamp
        )
        if not event:
            flash("Event not found.", "error")
            return redirect(url_for('main.index'))

        # Add and commit the comment to the database
        db.session.add(new_comment)
        db.session.commit()
        flash("Comment posted successfully.", "success")
    return redirect(url_for('event.show', id=id))

#Show users events
@eventbp.route('/myevents')
@login_required
def my_events():
    events = Event.query.filter_by(user_id=current_user.id).all()
    return render_template('event/my-events.html', events=events) # Need to create html for showing user events


# Additional routes to handle booking, updating, and canceling events

# Route to book tickets for an event
@eventbp.route('/<int:id>/book', methods=['GET','POST'])
@login_required
def book(id):
    form = BookingForm()
    event = db.session.scalar(db.select(Event).where(Event.id == id))
    
      # Check if the event has capacity available
    if event.capacity <= 0:
        flash("Sorry, this event is sold out.", "danger")
        return redirect(url_for('event.show', id=id))

    if form.validate_on_submit():
        quantity = form.quantity.data

        # Check if the requested quantity exceeds available capacity
        if quantity > event.capacity:
            flash(f"Only {event.capacity} tickets are available for this event.", "danger")
            return redirect(url_for('event.book', id=id))

        total_price = event.price * quantity
        booked_date = datetime.now()

        # Create the new booking
        new_booking = Order(
            quantity=quantity,
            total_price=total_price,
            booked_date=booked_date,
            user_id=current_user.id,
            event_id=id
        )

       

        # Update the event's remaining capacity
        event.capacity -= quantity
        if event.capacity <= 0:
            event.status = 'Sold out'
    
        db.session.add(new_booking)
        db.session.commit()        
        flash("Booking Successful! Your Booking ID is here -> {new_booking.id}", "success")
        return redirect(url_for('event.show', id=id))
    return render_template('event/event-details.html', form=form, event=event)
    
    
#The codes below needs to be in the model file.    

# event = db.session.get(Event, id)
# # Check if the event is open and has capacity
# if event.status == 'Open' and event.capacity > 0:
#     # Update booking capacity and save a Booking record
#     event.capacity -= 1
#     if event.capacity == 0:
#         event.status = 'Sold Out'
#     booking = Booking(user_id=current_user.id, event_id=event.id, quantity=1)  # Adjust as needed
#     db.session.add(booking)
#     db.session.commit()
#     flash("Successfully booked the event!", "success")
# else:
#     flash("Event is not available for booking.", "error")
# return redirect(url_for('event.show', id=id))

# Route to update an existing event (accessible to event owner only)
@eventbp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    event = db.session.scalar(db.select(Event).Where(Event.id == id))
    if event.user_id != current_user.id:
        flash("You do not have permission to update this event.", "error")
        return redirect(url_for('event.show', id=id))

    form = UpdateEventForm(obj=event)
    if form.validate_on_submit():
        event.name = form.name.data
        event.description = form.description.data
        event.image = form.image.data
        event.price = form.price.data
        event.location = form.location.data
        event.datetime = form.datetime.data
        event.capacity = form.capacity.data
        event.category = form.category.data
        
        db.session.commit()
        
        flash("Event Updated Successfully!", "success")
        return redirect(url_for('event.show', id=id))
        
    return render_template('event/create-event.html', form=form)

# Route to cancel an event (accessible to event owner only)
@eventbp.route('/<int:id>/cancel', methods=['POST'])
@login_required
def cancel(id):
    event = db.session.scalar(db.Select(Event.where(Event.id == id)))
    if event.user_id == current_user.id:
        event.status = 'Cancelled'
        db.session.commit()
        flash("Event cancelled successfully.", "success")
    else:
        flash("You do not have permission to cancel this event.", "error")
    return redirect(url_for('event.show', id=id))

@eventbp.route('/booking_history')
@login_required
def booking_history():
    bookings = db.session.query(Order).filter_by(user_id=current_user.id).all()
     
    return render_template('event/booking-history.html', bookings=bookings)