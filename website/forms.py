from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, PasswordField, IntegerField, DateTimeField, FileField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

# Login form
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

# Registration form
class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()]) 
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")]) 
    password = PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    contact_num = StringField("Contact Number", validators=[InputRequired()])
    address = StringField("Address", validators=[InputRequired()])
    submit = SubmitField("Register")

# Create Event form
class EventForm(FlaskForm):
    name = StringField('Title of the Event', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired(), Length(max=500)])
    image = FileField('Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, JPEG')])
    price = IntegerField('Price($)', validators=[InputRequired(), NumberRange(min=1, message="Price must be greater than 0")])
    location = StringField('Location', validators=[InputRequired()])
    datetime = DateTimeField('Event Date (DD/MM/YYYY hh:mm AM/PM)', validators=[InputRequired()], format='%d/%m/%Y %I:%M %p')
    capacity = IntegerField("Capacity", validators=[InputRequired(), NumberRange(min=1, message="Capacity must be greater than 0")])
    category = SelectField('Category', choices=
                            [('soccer', 'Soccer'),
                             ('basketball', 'Basketball'),
                             ('tennis', 'Tennis'),
                             ('cricket', 'Cricket'),
                             ('swimming', 'Swimming'),
                             ('athletics', 'Athletics'),
                             ('rugby', 'Rugby'),
                             ('golf', 'Golf'),
                             ('cycling', 'Cycling'),
                             ('boxing', 'Boxing'),
                             ('martial_arts', 'Martial Arts'),
                             ('esports', 'Esports'),
                             ('badminton', 'Badminton'),
                             ('volleyball', 'Volleyball'),
                             ('baseball', 'Baseball'),
                             ('hockey', 'Hockey'),
                             ('gymnastics', 'Gymnastics'),
                             ('motorsport', 'Motorsport'),
                             ('squash', 'Squash'),
                             ('table_tennis', 'Table Tennis'),
                             ('other', 'Other'),],
                           validators=[InputRequired()])
    submit = SubmitField("Create")

# Update Event form
class UpdateEventForm(FlaskForm):
    name = StringField('Title of the Event', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired(), Length(max=500)])
    image = FileField('Image', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, JPEG')])
    price = IntegerField('Price($)', validators=[InputRequired(), NumberRange(min=1, message="Price must be greater than 0")])
    location = StringField('Location', validators=[InputRequired()])
    datetime = DateTimeField('Event Date (DD/MM/YYYY hh:mm AM/PM)', validators=[InputRequired()], format='%d/%m/%Y %I:%M %p')
    capacity = IntegerField("Capacity", validators=[InputRequired(), NumberRange(min=1, message="Capacity must be greater than 0")])
    category = SelectField('Category', choices=
                            [('soccer', 'Soccer'),
                             ('basketball', 'Basketball'),
                             ('tennis', 'Tennis'),
                             ('cricket', 'Cricket'),
                             ('swimming', 'Swimming'),
                             ('athletics', 'Athletics'),
                             ('rugby', 'Rugby'),
                             ('golf', 'Golf'),
                             ('cycling', 'Cycling'),
                             ('boxing', 'Boxing'),
                             ('martial_arts', 'Martial Arts'),
                             ('esports', 'Esports'),
                             ('badminton', 'Badminton'),
                             ('volleyball', 'Volleyball'),
                             ('baseball', 'Baseball'),
                             ('hockey', 'Hockey'),
                             ('gymnastics', 'Gymnastics'),
                             ('motorsport', 'Motorsport'),
                             ('squash', 'Squash'),
                             ('table_tennis', 'Table Tennis'),
                             ('other', 'Other'),],
                           validators=[InputRequired()])
    submit = SubmitField("Update Event")

# Cancel Event form
class CancelEvent(FlaskForm):
    submit = SubmitField('Cancel Event')

# Comment form
class CommentForm(FlaskForm):
    text = TextAreaField('Leave Comment', validators=[InputRequired(), Length(max=300)])
    submit = SubmitField('Post Comment')

# Booking form to handle ticket quantity
class BookingForm(FlaskForm):
    quantity = IntegerField('Ticket Quantity', validators=[InputRequired(), NumberRange(min=1, message="Quantity must be at least 1")])
    submit = SubmitField('Book Now')
