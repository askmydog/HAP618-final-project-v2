from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError


class NoteForm(FlaskForm):
    note = TextAreaField('Note', validators=[DataRequired()])
    submit = SubmitField('Submit')

class RiskForm(FlaskForm):
    def validate_select(form, field):
        if field.data == '':
            raise ValidationError('Please select a choice')

    note = TextAreaField('Note', render_kw={'class':'form-control'})
    age = IntegerField('Age', validators=[DataRequired()], render_kw={'class':'form-control'})
    gender = SelectField('Gender', choices=[('',''),('m','Male'),('f','Female')], validators=[validate_select], render_kw={'class':'form-control'})
    sbp = IntegerField('Systolic Blood Pressure', validators=[DataRequired()], render_kw={'class':'form-control'})
    tchol = IntegerField('Total Cholesterol', validators=[DataRequired()], render_kw={'class':'form-control'})
    hdl = IntegerField('HDL', validators=[DataRequired()], render_kw={'class':'form-control'})
    hrx = SelectField('Hypertension Treatment', choices=[('',''),(1, 'Yes'),(0,'No')], validators=[validate_select], render_kw={'class':'form-control'})
    dm = SelectField('Diabetes', choices=[('', ''),(1, 'Yes'),(0,'No')], validators=[validate_select], render_kw={'class':'form-control'})
    race = SelectField('Race', choices=[('',''),('w', 'White'),('b','Black')], validators=[validate_select], render_kw={'class':'form-control'})
    sm = SelectField('Smoking', choices=[('',''),(1, 'Yes'),(0,'No')], validators=[validate_select], render_kw={'class':'form-control'})
    submit = SubmitField('Submit', render_kw={'class':'btn btn-primary'})


