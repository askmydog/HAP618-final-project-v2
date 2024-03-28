from flask import render_template, request, redirect, url_for,flash
from app import app, db
import sqlalchemy as sa
from app.forms import NoteForm, RiskForm
from app.models import Notes
from functions import age_parsing

@app.route('/', methods=['GET', 'POST'])
def NoteInput():
    form = NoteForm()
    if form.validate_on_submit():
        note_text = form.note.data
        n = Notes(note = note_text, age = age_parsing(note_text))
        db.session.query(Notes).delete()
        db.session.add(n)
        db.session.commit()
        return redirect(url_for('results'))
    else:
        return render_template('note.html', form = form)

@app.route('/results')
def results():
    return render_template('results.html', results = Notes.query.all())

@app.route('/risk-calc')
def risk_calc():
    form = RiskForm()
    if form.validate_on_submit():
        return f"{form.age}"
