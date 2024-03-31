from flask import render_template, request, redirect, url_for,flash
from app import app
import sqlalchemy as sa
from app.forms import NoteForm, RiskForm
from functions import * #age_parse, gender_parse, dm_parse, smoker_parse, race_parse, hrx_parse, sbp_parse, tchol_parse, hdl_parse, PatientClass, risk_rec

@app.route('/', methods=['GET', 'POST'])
def NoteInput():
    form = NoteForm()
    if form.validate_on_submit():
        note_text = form.note.data
        age = age_parse(note_text)
        gender = gender_parse(note_text)
        dm = dm_parse(note_text)
        sm = smoker_parse(note_text)
        race = race_parse(note_text)
        hrx = hrx_parse(note_text)
        hdl = hdl_parse(note_text)
        tchol = tchol_parse(note_text)
        sbp = sbp_parse(note_text)
        print(gender)
        return redirect(url_for('risk_calc', 
                                age = age,
                                gender = gender,
                                dm = dm,
                                sm = sm, 
                                race = race,
                                hrx = hrx,
                                hdl = hdl,
                                tchol = tchol, 
                                sbp = sbp
                                ))
    else:
        return render_template('note.html', form = form)

@app.route('/results')
def results():
    return render_template('results.html', results = Notes.query.all())

@app.route('/risk-calc', methods = ['GET','POST'])
def risk_calc():
    form = RiskForm()
    if form.validate_on_submit():
        patient = PatientClass(age=form.age.data, 
                               gen= form.gender.data, 
                               race=form.race.data, 
                               dm=form.dm.data, 
                               sm=form.sm.data, 
                               tchol=form.tchol.data,
                               hdl=form.hdl.data,
                               sbp = form.sbp.data,
                               hrx=form.hrx.data)
        risk = patient.ascvd_risk()
        rec = risk_rec(risk)
        return render_template('results.html', risk = risk, rec = rec)
    age = request.args.get("age")
    gender = request.args.get("gender")
    dm = request.args.get("dm")
    sm = request.args.get("sm")
    race = request.args.get("race")
    tchol = request.args.get("tchol")
    hdl = request.args.get("hdl")
    sbp = request.args.get("sbp")
    hrx = request.args.get("hrx")
    if age: form.age.default = age
    if gender: form.gender.default = gender
    if dm: form.dm.default = dm
    if sm: form.sm.default = sm
    if race: form.race.default = race
    if tchol: form.tchol.default = tchol
    if hdl: form.hdl.default = hdl
    if sbp: form.sbp.default = sbp
    if hrx: form.hrx.default = hrx
    form.process()
    return render_template("risk_calc.html", form = form)

    
    
    # age = Notes.query.
    # form = RiskForm()
    # form.age.default = 
    # if form.validate_on_submit():
        # pass
    # return render_template('risk_calc.html', form = form)
