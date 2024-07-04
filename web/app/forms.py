from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class EnterEquation(FlaskForm):
    equation = StringField('equation', validators=[DataRequired()])
    lower_limit = StringField('lower limit', validators=[DataRequired()])
    upper_limit = StringField('upper limit', validators=[DataRequired()])
    submit = SubmitField('Enter equation')