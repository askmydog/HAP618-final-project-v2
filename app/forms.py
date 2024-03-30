from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app import db
from app.models import Notes

class NoteForm(FlaskForm):
    note = TextAreaField('Note', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RiskForm(FlaskForm):
    def validate_select(form, field):
        if field.data == '':
            raise ValidationError('Please select a choice')

    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('',''),('m','Male'),('f','Female')], validators=[validate_select])
    # sbp = IntegerField('Systolic Blood Pressure', validators=[DataRequired()])
    # tchol = IntegerField('Total Cholesterol', validators=[DataRequired()])
    # hdl = IntegerField('HDL', validators=[DataRequired()])
    # hrx = SelectField('Hypertension Treatment', choices=[('',''),('y', 'Yes'),('n','No')], validators=[validate_select()])
    dm = SelectField('Diabetes', choices=[('', ''),(1, 'Yes'),(0,'No')], validators=[validate_select])
    race = SelectField('Race', choices=[('',''),('w', 'White'),('b','Black')], validators=[validate_select])
    sm = SelectField('Smoking', choices=[('',''),(1, 'Yes'),(0,'No')], validators=[validate_select])
    submit = SubmitField('Submit')


