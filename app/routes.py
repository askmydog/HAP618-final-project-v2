from flask import render_template, request, redirect, url_for,flash, jsonify
from app import app
from app.forms import RiskForm
from functions import *

@app.route('/', methods = ['GET','POST'])
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
        print(patient.ascvd_risk(), " ", patient.risk_rec())

        return render_template('results.html', risk = patient.ascvd_risk(), rec = patient.risk_rec())
    
    return render_template("risk_calc.html", form = form)

