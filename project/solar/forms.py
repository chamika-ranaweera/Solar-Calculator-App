from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

class Location_Form(FlaskForm):
    submit = SubmitField(label='Get the Solar Insolation Data')