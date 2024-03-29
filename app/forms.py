from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired
from app import db
from app.models import Notes

class NoteForm(FlaskForm):
    note = TextAreaField('Note', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RiskForm(FlaskForm):
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('m','Male'),('f','Female')])
    sbp = IntegerField('Systolic Blood Pressure', validators=[DataRequired()])
    tchol = IntegerField('Total Cholesterol', validators=[DataRequired()])
    hdl = IntegerField('HDL', validators=[DataRequired()])
    hrx = SelectField('Hypertension Treatment', choices=[('y', 'Yes'),('n','No')])
    dm = SelectField('Diabetes', choices=[('y', 'Yes'),('n','No')])
    race = SelectField('Race', choices=[('w', 'White'),('b','Black')])
    sm = SelectField('Smoking', choices=[('y', 'Yes'),('n','No')])
    submit = SubmitField('Submit')
