from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, PasswordField, BooleanField

from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from models import User




def email_exists(form, field):
    print ("in Email exist")
    email = User.query.filter_by(user_email = field.data).first()
    print (email)
    if email:
        print ("inside")
        raise ValidationError('Email Already Exists')

class RegistrationForm(FlaskForm):

    name = StringField ('Name', validators=[DataRequired(), Length(3,15, message= 'Must be between 3 to 15 characters')])
    email = StringField ('Email', validators=[DataRequired(), Email(), email_exists])
    password = PasswordField ('Password',validators=[DataRequired(), Length(5), EqualTo('confirm', message='Password must match')])
    confirm = PasswordField ('Confirm', validators=[DataRequired()])
    submit = SubmitField ('Register')


class LoginForm(FlaskForm):
    email = StringField('Email ID:', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    stay_logged_in = BooleanField('stay logged-in')
    submit = SubmitField('Log In')



