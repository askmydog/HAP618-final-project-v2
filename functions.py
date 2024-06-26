import math, re
from datetime import datetime

class PatientClass:
    def __init__(self, age = None, sbp = None, tchol = None, hdl = None, dm = None, sm = None, race = None, gen = None, hrx = None) -> None:

        self.age = int(age)
        self.sbp = int(sbp)
        self.tchol = int(tchol)
        self.hdl = int(hdl)
        self.dm = int(dm)
        self.sm = int(sm)
        self.race = race
        self.gen = gen
        self.hrx = hrx
        self.risk = None

    def ascvd_risk(self) -> float:
        """Calculate 10 year cardiovascular risk based on (variable name, options):
        - Age (age)
        - Race (race, "w" or "b")
        - Gender(gen, "m" or "f")
        - Systolic blood pressure (sbp)
        - Hyptertension treatment (hrx)
        - Total cholesterol (tchol)
        - HDL-C (hdl)
        - Diabetes (dm)
        - Smoking (sm)"""

        # zero coefficients
        baseline_surv = 0
        mean_coef_val = 0
        age_coef = 0
        age_sq_coef = 0
        tchol_coef = 0
        tchol_age_coef = 0
        hdl_coef = 0
        hdl_age_coef = 0
        sbp_coef = 0
        sbp_age_coef = 0
        dm_coef = 0
        sm_coef = 0
        sm_age_coef = 0
        
        # Assign coefficients
        if self.race == 'w':
            if self.gen == "m":
                baseline_surv = 0.9144
                mean_coef_val = 61.18
                age_coef = 12.344
                tchol_coef = 11.853
                tchol_age_coef = -2.664
                hdl_coef = -7.990
                hdl_age_coef = 1.769
                dm_coef = 0.658
                sm_coef = 7.837
                sm_age_coef = -1.795
                if self.hrx == 1:
                    sbp_coef = 1.797
                else:
                    sbp_coef = 1.764
                    
            elif self.gen == "f":
                baseline_surv = 0.9665
                mean_coef_val = -29.18
                age_coef = -29.799
                age_sq_coef = 4.884
                tchol_coef = 13.540
                tchol_age_coef = -3.114
                hdl_coef = -13.578
                hdl_age_coef = 3.149
                dm_coef = 0.661
                sm_coef = 7.574
                sm_age_coef = -1.665
                if self.hrx == 1:
                    sbp_coef = 2.019
                else:
                    sbp_coef = 1.957

        elif self.race == "b":
            if self.gen == "m":
                baseline_surv = 0.8954
                mean_coef_val = 19.54
                age_coef = 2.469
                tchol_coef = 0.302
                hdl_coef = -0.307
                dm_coef = 0.645
                sm_coef = 0.549
                if self.hrx == 1:
                    sbp_coef = 1.916 
                else:
                    sbp_coef = 1.809
                
            elif self.gen == "f":
                baseline_surv = 0.9533
                mean_coef_val = 86.61
                age_coef = 17.114
                tchol_coef = 0.940
                hdl_coef = -18.920
                hdl_age_coef = 4.475
                dm_coef = 0.874
                sm_coef = 0.691
                if self.hrx == 1:
                    sbp_coef = 29.291
                    sbp_age_coef = -6.432
                else:
                    sbp_coef = 27.820
                    sbp_age_coef = -6.087

        #calculate coefficients * values for each variable 

        coef_val =  age_coef * math.log(self.age) + \
                    age_sq_coef * math.log(self.age)**2 + \
                    tchol_coef * math.log(self.tchol) + \
                    tchol_age_coef * math.log(self.age) * math.log(self.tchol) + \
                    hdl_coef * math.log(self.hdl) + \
                    hdl_age_coef * math.log(self.hdl) * math.log(self.age) + \
                    sbp_coef * math.log(self.sbp) + \
                    sbp_age_coef * math.log(self.sbp) * math.log(self.age) + \
                    dm_coef * self.dm + \
                    sm_coef * self.sm + \
                    sm_age_coef * self.sm * math.log(self.age)

        # calculate risk for each demographic: subtract mean coefficient * values for demographic
        # from individual coefficients * values and raise 1 - baseline survival to this number


        self.risk =  1 - baseline_surv ** math.e ** (coef_val - mean_coef_val)
        return self.risk
    
    def risk_rec(self):
        rec_list = []
        if not self.risk: self.risk = self.ascvd_risk()
        if self.risk >= 0.2:
            rec_list.append("A high intensity statin is recommended.")
            rec_list.append(f"A high intensity statin will reduce the patient's risk by 50% to {(self.risk*.7):.1%}.")
            return rec_list
        elif self.risk >=0.075: 
            rec_list.append("A moderate intensity statin is recommended.")
            rec_list.append(f"A moderate intensity statin will reduce the patient's risk by 30% to {(self.risk*.7):.1%}.")
            return rec_list
        else: 
            rec_list.append("No statin is recommended")
            rec_list.append(f"The patient's risk is low enough that a statin medication will not substantially lower their risk.")
            return rec_list
