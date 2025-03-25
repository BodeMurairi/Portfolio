from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


class AddCafeForm(FlaskForm):
    name = StringField('Coffee Name', validators=[DataRequired()])
    Location = StringField('Location', validators=[DataRequired()])
    Availability = StringField('Availability', validators=[DataRequired()])