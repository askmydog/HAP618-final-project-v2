import math, re
from datetime import datetime

class PatientClass:
    def __init__(self, mrn = None, dob = None, age = None, sbp = None, tchol = None, hdl = None, dm = None, sm = None, race = None, gen = None, hrx = None) -> None:

        age_eq = lambda dob: math.floor(((datetime.today() - datetime.strptime(dob, '%m/%d/%Y')).days/365))

        self.mrn = mrn
        self.dob = datetime.strptime(dob, '%m/%d/%Y')
        if not self.dob is None:
            self.age = age
        else:
            self.age = age_eq(dob)
        self.sbp = sbp
        self.tchol = tchol
        self.hdl = hdl
        self.dm = dm
        self.sm = sm
        self.race = race
        self.gen = gen
        self.hrx = hrx

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

        # if race != "w" or race != "b":
        #     return "Please enter the patient's race"
        # if gen != "m" or gen != "f":
        #     return "Please enter the patient's gender"

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
                sm_coef = -7.837
                sm_age_coef = -1.795
                if self.hrx == True:
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
                if self.hrx == True:
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
                if self.hrx == True:
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
                if self.hrx == True:
                    sbp_coef = 29.291
                    sbp_age_coef = -6.432
                else:
                    sbp_coef = 27.820
                    sbp_age_coef = -6.087

        #calculate coefficients * values for each variable 

        try:
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

            return 1 - baseline_surv ** math.e ** (coef_val - mean_coef_val)
        except:
            return "please enter all values"

def age_parse(text):
    pattern = "\\d+(?=\\s?(yo|year old|YO))"
    try:
        return int(re.search(pattern, text).group(0))
    except:
        return None
    
def gender_parse(text):
    pattern = "(man|woman|male|female|(?<=\\d\\d)(m|w|f))"
    match = re.search(pattern, text).group(0).lower()
    if match in ['m', 'male', 'man']:
        gender = 'm'
    else:
        gender = 'f'
    return gender
