from flask import Blueprint
#Need to connect database in here.

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    #Use database connection to return results which user want to see.
    #e.g., if user select rock category, then return events for rock categoty from database.
    return '<h1>Starter code for assignment 3<h1>'