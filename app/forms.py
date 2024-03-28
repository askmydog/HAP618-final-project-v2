from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from app import db
from app.models import Notes

class NoteForm(FlaskForm):
    note = TextAreaField('Note', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RiskForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired()])
    submit = SubmitField('Submit')
