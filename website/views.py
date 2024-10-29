from flask import Blueprint, render_template, request
from .models import Event
from . import db

# Define the main blueprint for the main pages
main_bp = Blueprint('main', __name__)

# Route for the homepage
@main_bp.route('/')
def index():
    # Get the category filter from the query string, if any
    category = request.args.get('category')
    
    # Query for events, filtering by category if provided
    if category:
        events = Event.query.filter_by(category=category).all()
    else:
        events = Event.query.all()
    
    # Render the index template, passing the list of events and selected category
    return render_template('index.html', events=events, selected_category=category)

