"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.forms import NewUser
from app.models import UserProfile
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename


          




###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

def getImages():

     images = []
     for subdir, dir, files in os.walk(app.config['UPLOAD_FOLDER']):
         for file in files:
             if not file.startswith('.'):
                images.append(file)
     return images

@app.route('/profile', methods = ["GET", "POST"])
def profile():
    form = NewUser()
    if ((request.method == 'POST') and (form.validate_on_submit())):
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        gender = request.form['gender']
        email = request.form['email']
        location = request.form['location']
        biography = request.form['biography']
        date = datetime.now()
        file = request.files['photo']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      
        if gender is not None:
            newProfile = UserProfile(firstname, lastname, gender, email, location, biography, date, filename)
            
            db.session.add(newProfile)
            db.session.commit()

            flash(firstname +'`s' + ' profile is created successfully!', 'success')
            return redirect(url_for('profiles'))

    return render_template('profile.html', form = form)

@app.route('/profiles')
def profiles():
    persons = db.session.query(UserProfile).all()
    return render_template('profiles.html', persons = persons)

@app.route('/profile/<userid>')
def userPro(userid): 

      persons = db.session.query(UserProfile).all()
      for person in persons:
        if (userid == person.id):
            userid = person.id
      return render_template('IndividualProfile.html', persons = persons, userid = userid)



# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('secure_page'))
#     form = LoginForm()
#     if ((request.method == "POST") and (form.validate_on_submit())):
#         # change this to actually validate the entire form submission
#         # and not just one field
#         if form.username.data:
#             # Get the username and password values from the form.
#             username = request.form['username']
#             password = request.form['password']
#             # using your model, query database for a user based on the username
#             # and password submitted. Remember you need to compare the password hash.
#             # You will need to import the appropriate function to do so.
#             # Then store the result of that query to a `user` variable so it can be
#             # passed to the login_user() method below.
            
#             user = UserProfile.query.filter_by(username = username).first()

#             if user is not None and check_password_hash(user.password, password):
#                 # get user id, load into session
#                 login_user(user)

#                 # remember to flash a message to the user
#                 flash('You have successfully logged in!','success')
#                 return redirect(url_for('secure_page'))  # they should be redirected to a secure-page route instead
#             else:
#                 flash('User not found.')
#     return render_template("login.html", form=form)


# @app.route("/secure-page")
# @login_required
# def secure_page():
#     return render_template("secure_page.html")

# @app.route("/logout")
# def logout():
#     logout_user()
#     flash('You are now logged out.','danger')
#     return redirect(url_for('home'))


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
# @login_manager.user_loader
# def load_user(id):
#     return UserProfile.query.get(int(id))

###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
