from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import InputRequired, Length
from flask_wtf.file import FileField, FileAllowed
from flask_uploads import IMAGES

class RegistrationForm(FlaskForm):
    name = StringField('Full name', validators=[InputRequired('A full name required.'), Length(max=100, message='yorur name cant be more than 100 characters')])
    username = StringField('Username', validators=[InputRequired('A username required.'), Length(max=30, message='yorur username is too many character ')])
    password = PasswordField('Password',  validators=[InputRequired('A password is required.')])
    image = FileField( validators=[FileAllowed(IMAGES, 'only images are accepted')])    

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired('A username required.'), Length(max=30, message='yorur username is too many character ')])
    password = PasswordField('Password',  validators=[InputRequired('A password is required.')])
    remember = BooleanField('Remember me')   

class TweetForm(FlaskForm):
    text =  TextAreaField('Message', validators=[InputRequired('Message is required.')])
