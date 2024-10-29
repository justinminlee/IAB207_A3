from flask import Blueprint, request, render_template, redirect, url_for, flash
from .models import Event, Comment 
from .forms import LoginForm, RegisterForm, EventForm, UpdateEventForm, CancelEvent, CommentForm
from . import db
import os 
from werkzeug.utis import secure_filenameec
from flask_login import login_required, current_user
from datetime import datetime

eventbp = Blueprint('event', __name__, url_prefix='/event')

#Create new events
@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    print('Method type  :', request.method)
    form = EventForm()
    if form.validate_on_submit():
        db_file_path = check_upload_file(form)
        event = Event(
            name = form.name.data,
            description = form.description.data,
            image = form.image.data,
            price = form.price.data,
            location = form.location.data,
            datetime = datetime.strptime(form.datetime.data, '%d/%m/%Y %I:%M %p'),
            capacity = form.capacity.data,
            category = form.category.data,
            status = 'Open',
            user_id = current_user.id
        )
        db.session.add(event)
        db.session.commit()
        flash("New Event Created Successfully", 'success')
        return redirect(url_for('event.create'))
    #return render_template('This need to be the path for the html', form=form)

@eventbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).Where(Event.id == id))
    form = CommentForm()
    #return render_template('This need to be the path for the html', event=event, form=form)

#Save uploaded file
def check_file_uploaded(form):
    file_path = form.image.data
    filename = file_path.filename
    BASE_PATH = os.path.dirname(__file__)
    upload_path = os.path.join(BASE_PATH, 'static/images', secure_filename(filename))
    db_uplaod_path = '/static/img/' + secure_filenameec(filename)
    return db_uplaod_path

@eventbp.route('/<id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()
    event = db.session.scalar(db.select(Event).Where(Event.id == id))
    if form.validate_on_submit():
        comment = Comment(
            text = form.text.data,
            event = event,
            user = current_user
        )
    ruturn redirect(url_for('event.show', id=id))