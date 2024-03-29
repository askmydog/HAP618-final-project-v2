from flask import render_template, request, redirect, url_for,flash
from app import app, db
import sqlalchemy as sa
from app.forms import NoteForm, RiskForm
from app.models import Notes
from functions import age_parse, gender_parse

@app.route('/', methods=['GET', 'POST'])
def NoteInput():
    form = NoteForm()
    if form.validate_on_submit():
        note_text = form.note.data
        age = age_parse(note_text)
        gender = gender_parse(note_text)
        print(gender)
        return redirect(url_for('risk_calc', 
                                age = age,
                                gender = gender
                                ))
    else:
        return render_template('note.html', form = form)

@app.route('/results')
def results():
    return render_template('results.html', results = Notes.query.all())

@app.route('/risk-calc')
def risk_calc():
    age = request.args.get("age")
    gender = request.args.get("gender")
    form = RiskForm()
    if age: form.age.default = age
    if gender: form.gender.default = gender
    form.process()
    return render_template("risk_calc.html", form = form)
    # age = Notes.query.
    # form = RiskForm()
    # form.age.default = 
    # if form.validate_on_submit():
        # pass
    # return render_template('risk_calc.html', form = form)
