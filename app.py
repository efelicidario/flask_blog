from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Create a Flask instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "fleeceKey"

# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("Enter your name: ", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Filters: |<filter name>
#safe
#capitalizer
#lower
#upper
#title
#trim
#striptags

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
        
    return render_template("name.html",
                           name = name,
                           form = form)

#if __name__ == "__main__":
    #app.run()