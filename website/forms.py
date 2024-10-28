from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, IntegerField, DateTimeField, FileField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

# creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    first_name=StringField("First Name", validators=[InputRequired()])
    last_name=StringField("Last Name", validators=[InputRequired()]) 
    email = StringField("Email Address", validators=[Email("Please enter a valid email")]) 
    # linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    # submit button
    submit = SubmitField("Register")
    
#Create new event
class EventForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    description = TextAreaField('Description', 
                validators=[InputRequired()])
    image = FileField('Image', validators=[
                FileRequired(message = 'Image cannot be empty'),
                FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, JPEG, png, jpg, jpeg')])
    price = IntegerField('Price($)', validators=[InputRequired()])
    location = StringField( 'Location', validators=[InputRequired()])
    datetime = DateTimeField("Date", format= '%Y-%m-%d', validators=[InputRequired()])
    capacity = IntegerField("Capacity", validators=[InputRequired(), NumberRange(min=50, max=1000)])
    category = StringField('Category', validators=[InputRequired()])
    submit = SubmitField("Create")
    
#User cancel event
class CancelEvent(FlaskForm):
    submit = SubmitField('Cancel Event')

#User comment
class CommentForm(FlaskForm):
    text = TextAreaField('Leave Comment', [InputRequired()])
    submit = SubmitField('Create')