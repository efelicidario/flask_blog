from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a Flask instance
app = Flask(__name__)

# Add Database
# Old SQLite db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# New MySQL db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:TeeWhy661!@localhost/users'

# Secret Key
app.config['SECRET_KEY'] = "fleeceKey"

# Initialize Database
db = SQLAlchemy(app)

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Create a string
    def __repr__(self):
        return '<Name %r>' % self.name
    
with app.app_context():
    db.create_all()

# Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Filters: |<filter name>
#safe
#capitalizer
#lower
#upper
#title
#trim
#striptags

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        email = form.email.data
        form.name.data = ''
        form.email.data = ''
        flash("User added successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", 
                           form=form, 
                           name=name, 
                           our_users=our_users)

# Create a route decorator
@app.route('/')
def index():
    first_name = "Tyler"
    stuff = "This is bold Text"
    
    favorite_pizza = ["Pineapple", "Bellpepper", "Onion", 69]
    return render_template("index.html", 
                           first_name=first_name,
                           stuff=stuff,
                           favorite_pizza=favorite_pizza)

# localhost:5000/user/Tyler
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name=name)

# Create Custom Error Pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
        return render_template("404.html"), 404
    
# Invalid Server Error
@app.errorhandler(500)
def page_not_found(e):
        return render_template("500.html"), 500

# Create Name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form submitted successfully!")
        
    return render_template("name.html",
                           name = name,
                           form = form)

#if __name__ == "__main__":
    #app.run()