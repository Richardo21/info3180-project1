from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SelectField, TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import validators
from wtforms.fields.html5 import EmailField 
from wtforms.validators import InputRequired


class NewUser(FlaskForm):
    firstname = TextField('First Name', validators=[InputRequired()])
    lastname = TextField('Last Name', validators=[InputRequired()])
    gender = SelectField(u'Gender', choices = [('M','Male'),('F','Female')])
    email = EmailField('Email Address', [validators.DataRequired(), validators.Email()])
    location = TextField('Location', validators= [InputRequired()])
    biography = TextAreaField('Biography', validators = [InputRequired()])
    photo = FileField('Profile Picture', validators = [FileRequired(), FileAllowed(['jpg', 'png'], 'Images Only!')])
