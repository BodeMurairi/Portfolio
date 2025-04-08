from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email

# Form for user tasks
class TaskForm(FlaskForm):
    '''Task Form'''
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    
    # Add a select field for task completion emoji choice
    completed = SelectField('Completed', choices=[('✅', 'Success'), ('❌', 'Fail')], default='✅')
    
    submit = SubmitField('Submit')

# Form for user registration
class RegistrationForm(FlaskForm):
    '''Registration Form'''
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

# Form for user login
class LoginForm(FlaskForm):
    '''Login Form'''
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
