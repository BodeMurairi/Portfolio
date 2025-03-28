from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AddCafeForm(FlaskForm):
    name = StringField('Coffee Name', validators=[DataRequired()])
    Location = StringField('Location', validators=[DataRequired()])
    Availability = StringField('Availability', validators=[DataRequired()])
    submit = SubmitField('➕ Add Cafe')
