import math, re
from datetime import datetime

class PatientClass:
    def __init__(self, mrn = None, age = None, sbp = None, tchol = None, hdl = None, dm = None, sm = None, race = None, gen = None, hrx = None) -> None:

        age_eq = lambda dob: math.floor(((datetime.today() - datetime.strptime(dob, '%m/%d/%Y')).days/365))

        self.mrn = mrn
        # if not self.dob is None: self.dob = datetime.strptime(dob, '%m/%d/%Y')
        # if self.dob is None:
        #     self.age = age_eq(dob)
        # else:
        self.age = int(age)
        self.sbp = int(sbp)
        self.tchol = int(tchol)
        self.hdl = int(hdl)
        self.dm = int(dm)
        self.sm = int(sm)
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

#         print(f"""age {self.age} gender {self.gen} race {self.race} 
# dm {self.dm}{type(self.dm)} tchol {self.tchol} hdl {self.hdl} sbp {self.sbp} 
# hrx {self.hrx} sm {self.sm}""")
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

        # try:
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
        # except:
        #     return "please enter all values"

def age_parse(text):
    pattern = "\\d+(?=\\s?(yo|year old|YO))"
    try:
        return int(re.search(pattern, text).group(0))
    except:
        return None
    
def gender_parse(text):
    pattern = "(man|woman|male|female|(?<=\\d\\d)(m|w|f))"
    match = re.search(pattern, text.lower())
    print(match)
    if match:
        match = match.group(0)
        if match in ('m', 'male', 'man'):
            gender = 'm'
        else:
            gender = 'f'
    else:
        gender = None
    return gender

def race_parse(text):
    """Return 'b' if words black, african american, aaf or aam are detected, otherwise returns 'w'.
    Assumes patient is white unless otherwise specified"""
    pattern = "\\b(black|african american|aaf|aam|aa)\\b"
    match = re.search(pattern, text.lower())
    if match: race = "b"
    else: race = 'w'
    return race

def smoker_parse(text):
    '''Retun 1 if patient is smoker by looking for the words smoker or smoking.  
    If "never smoker" detected, return 0, other return None'''
    pattern_A = "never( |-)smoke(r|d)"
    pattern_B = "smok(er|ing|ed)"
    text = text.lower()
    match = re.search(pattern_A, text)
    if match:
        sm = 0
    elif re.search(pattern_B, text):
        sm = 1
    else:
        sm = None
    return sm

def dm_parse(text):
    '''Return 1 if words DM, T2DM, diabetes, IDDM, NIDDM decteted, or if an A1C >6.5 
    is found, if listed.  Otherwise, return None.'''
    pattern_hist = '\\b(dm|t2dm|diabetes|iddm|niddm)\\b'
    pattern_lab = 'a1c\\D+(\\d{1,2}\\.?\\d{1,2}?)'
    text = text.lower()
    match_hist = re.search(pattern_hist,text)
    match_lab = re.search(pattern_lab,text)
    if match_lab: match_lab = float(re.search(pattern_lab,text).group(1))
    if match_hist or match_lab >= 6.5:
        dm = 1
    else:
        dm = 0
    return dm

def hrx_parse(text):
    '''Return 1 if words HTN or hypertension detected, or if BP is >140/90. Assumes if patient has diagnosis of HTN, is on treatment.
    If not detected, return None.'''
    text = text.lower()
    pattern_hist = '(htn|hypertension)' #( (.+?controlled|treated|(on (therapy|treatment))))?
    pattern_bp = '(\\d{2,3})\\/(\\d{2,3})'
    pattern_sbp = '(sbp|systolic blood pressure|systolic bp)\\D+(\\d{2,3})'
    match_hist = re.search(pattern_hist, text)
    match_bp = re.search(pattern_bp, text)
    match_sbp = re.search(pattern_sbp, text)
    htn = None
    if match_bp:
        if int(match_bp.group(1))>=140 or int(match_bp.group(2))>=90: #assumes that patient on treatment if BP >140/90
            htn = 1
    if match_sbp:
        if int(match_sbp.group(2))>140: htn = 1
    if match_hist or htn:
        htnrx = 1
    else:
        htnrx = 0
    return htnrx

def sbp_parse(text):
    '''Extract systolic blood pressure, if listed, otherwise return None'''
    text = text.lower()
    pattern_bp = '(\\d{2,3})\\/(\\d{2,3})'
    pattern_sbp = '(sbp|systolic blood pressure|systolic bp)\\D+(\\d{2,3})'
    match_bp = re.search(pattern_bp, text)
    match_sbp = re.search(pattern_sbp, text)
    if match_bp: return int(match_bp.group(1))
    if match_sbp: return int(match_sbp.group(2))
    else: return None

def tchol_parse(text):
    '''Extract total cholesterol, if listed.  Otherwise return None'''
    text = text.lower()
    pattern_chol = '(t chol|total chol|total cholesterol|tchol)\\D+(\\d{2,3})'
    match_chol = re.search(pattern_chol, text)
    if match_chol: match_chol = int(match_chol.group(2))
    return match_chol

def hdl_parse(text):
    '''Extract total cholesterol, if listed.  Otherwise return None'''
    text = text.lower()
    pattern_hdl = '(hdl|high density lipoprotein)\\D+(\\d+\\b)'
    match_hdl = re.search(pattern_hdl, text)
    if match_hdl: match_hdl = int(match_hdl.group(2))
    return match_hdl

def risk_rec(risk):
    if risk >= 0.2: return 'High intensity statin recommended'
    elif risk >=0.075: return 'High intensity statin recommended'
    else: return 'No statin recommended'
        