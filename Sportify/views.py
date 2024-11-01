from flask import Blueprint, render_template, request
from .models import Event
from . import db
from datetime import datetime

# Define the main blueprint for the main pages
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # List of categories for the dropdown
    categories = [
        'soccer', 'basketball', 'tennis', 'cricket', 'swimming', 'athletics',
        'rugby', 'golf', 'cycling', 'boxing', 'martial_arts', 'esports',
        'badminton', 'volleyball', 'baseball', 'hockey', 'gymnastics',
        'motorsport', 'squash', 'table_tennis', 'other'
    ]

    # Get the selected category from the query parameters, default to 'all'
    category = request.args.get('category', 'all')

    # Filter events by category if a specific category is selected
    if category != 'all':
        events = Event.query.filter_by(category=category).all()
    else:
        events = Event.query.all()

     # Update event status based on the date
    for event in events:
        if event.datetime < datetime.now() and event.status == 'Open':
            event.status = 'Inactive'
            db.session.commit()

    # Render the index template, passing the list of events, categories, and selected category
    return render_template(
        'index.html',
        events=events,
        categories=categories,
        selected_category=category
    )
