# IAB207_A3
This is IAB207 A3 Group 28

## Make sure to install before start 
```
flask
werkzeug
bootstrap-flask
email-validator
flask-login
flask-sqlalchemy
flask-wtf
flask-bcrypt
```

### You could make a separate branch and request to push the code but not necessarily :)





-- Tasks to do
### Part 1: Project Requirements
Landing Page:
Create a clear landing page that promotes events and allows users to browse by categories.
Optionally include text-based search functionality for users to filter events.

Event Listing & Details Page:
Events listed on the landing page should include an overview of the event’s status.
The details page should display event information (image, description, date, and other relevant details).

Booking Functionality:
Users need to log in to book tickets.
Users should specify the quantity of tickets they want to purchase, and an order is generated with a reference ID.
Show the user’s booking history on their account.

Comments Section:
Logged-in users can post comments on events.
Comments should display the commenter's name, comment text, and the date posted.

Event Creation & Management:
Logged-in users can create events and update event details (excluding status).
The event status should include options like Open, Inactive, Sold Out, or Cancelled.
Users can cancel their own events.

User Registration & Login/Logout:
Allow users to register with details like name, email, password, contact number, and address.
Implement login and logout functionality.

Error Handling:
Ensure proper handling for 404 (Page Not Found) and 500 (Server Error) errors.

Navigation & Database Integration:
All pages should include a navigation menu.
Use dynamic content from the database (using SQLAlchemy).

### Part 2: Project Management
Use a GitHub repository for version control and task management. Assign tasks equitably among the team members and track progress.
Maintain a list of tasks and submit a peer review feedback form for each team member.
Include clear contributions of each member in the final submission report.

### Part 3: Development Guidelines
Code should be well-documented with comments.
Stick to the prescribed languages and frameworks: HTML, CSS, Bootstrap, Python, Flask (including all relevant Flask libraries), and WTForms.

Database:
Design at least 4 tables:
Event Table
Booking Table (with relationships to events and users)
User Table (for login credentials)
Comments Table

Submission Instructions:
Package your submission in a ZIP file named according to your group number

Include:
Submission report (with GitHub link, team declaration, task table, and git shortlog).
Application code with a working sqlite database file containing dummy data.
Make sure your code can be run by executing main.py.

Individual Components:
Each member needs to submit a peer review form.
Everyone's contribution will be evaluated individually, so ensure active participation from all team members.
