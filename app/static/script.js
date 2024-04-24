note = document.getElementById('note');
age = document.getElementById('age');
gen = document.getElementById('gender');
race = document.getElementById('race');
dm = document.getElementById('dm');
sbp = document.getElementById('sbp');
hrx = document.getElementById('hrx');
sm = document.getElementById('sm');
tchol = document.getElementById('tchol');
hdl = document.getElementById('hdl');
sbmt = document.getElementById('submit');
clrbtn = document.getElementById("clear_btn")

function age_parser(text){
    const re = /\d+(?=\s?(yo|year old))/i;
    let match = re.exec(text);
    if (match != null) {
        return Number(match[0])
    } else {
        return null;
    }
}

function gen_parser(text) {
    const re = /\b(man|woman|male|female|((?<=\d\d)|(?<=\d\dyo )|(?<=\d\dyo, ))(m|w|f|aam|aaf))\b/i;
    let match = re.exec(text);
    if (match != null) {
        match = match[0];
        gen_array = ['m', 'male', 'man', 'aam'];
        if (gen_array.indexOf(match) > -1) {
            return 'm';
        } else {
            return 'f';
        }
    }
}

function race_parser(text) {
    const re_b = /\b(black|african american|aaf|aam|aa)\b/i;
    let match_b = re_b.exec(text);
    const re_w = /\b(white|hispanic|latin(o|a|x)|asian)\b/i;
    match_w = re_w.exec(text);
    if (match_b != null) {
        return 'b';
    } else if (match_w != null ){
        return 'w';
    } else {
        return null
    }
}

function sbp_parser(text) {
    const re_bp = /(?<!\d\d\/)(?<!\d\/)(\d{2,3})\/(\d{2,3}(?!\/\d+))/i;
    let match_bp = re_bp.exec(text);
    const re_sbp = /(sbp|systolic blood pressure|systolic bp)\D+(\d{2,3})/i;
    let match_sbp = re_sbp.exec(text);
    // const re_hist = /(?!no )(?!=history of )(?!h\/o)htn/i;
    // let match_hist = re_hist.exec(text);
    if (match_bp != null) {
        return Number(match_bp[1])
    } else if (match_sbp != null) {
        return Number(match_sbp[2]);
    } else {
        return null
    }
}

function sm_parser(text) {
    re_a = /(?<!never )(?<!never-)(?<!does not )(?<!no )smok/i;
    match_a = re_a.exec(text);
    re_b = /(does not |never( |-)|no )smok/i;
    match_b = re_b.exec(text)
    if (match_b != null) {
        return 0;
    } else if (match_a != null) {
        return 1;
    } else {
        return null;
    }
}

function dm_parser(text) {
    re_lab = /a1c\D+(\d{1,2}\.?\d{1,2}?)/i;
    match_lab = re_lab.exec(text);
    re_hist = /(?<!no )(?<!without )(?<!no history of )(?<!no h\/o )(?<!no e\/o )(\bdm\b|\bt2dm\b|\bdiabetes\b|\biddm\b|\bniddm\b)/i;
    match_hist = re_hist.exec(text);
    re_nohist = /((no )|(without )|(no history of )|(no h\/o )|(no e\/o ))(\bdm\b|\bt2dm\b|\bdiabetes\b|\biddm\b|\bniddm\b)/i;
    match_nohist = re_nohist.exec(text);
    if (match_lab != null) {
        if (Number(match_lab[1]) >= 6.5) {
            return 1;
        } else {
            return 0;
        }
    } else if (match_hist != null) {
        return 1;
    } else if (match_nohist != null){
        return 0;
    } else {
        return null;
    }
}

function hrx_parser(text) {
    re_hist = /(?<!no )(?<!without )(?<!no history of )(?<!no h\/o )(?<!no e\/o )(htn|hypertension)/i;
    match_hist = re_hist.exec(text);
    med_arr = ['hctz', 'lisinopril', 'benazepril', 'losartan', 'valsartan', 'amlodipine','chlorthalidone',];
    re_meds = RegExp('(' + med_arr.join('|') + ')','i');
    match_meds = re_meds.exec(text);
    re_norx = /(htn|hypertension) (not (treated|on therapy|on treatment)|untreated)/i;
    match_norx = re_norx.exec(text);
    re_nohist = /((no )|(without )|(no history of )|(no h\/o )|(no e\/o ))(htn|hypertension)/i;
    match_nohist = re_nohist.exec(text)
    if (match_hist != null | match_meds != null) {
        return 1;
    } else if (match_norx != null | match_nohist != null) {
        return 0;
    } else {
        return null;
    }
}

function tchol_parser(text) {
    re = /(t chol|total chol|total cholesterol|tchol)\D+(\d{2,3})/i;
    match = re.exec(text);
    if (match != null) {
        return Number(match[2]);
    } else {
        return null;
    }
}   

function hdl_parser(text) {
    re = /(hdl|high density lipoprotein)\D+(\d{2,3})/i;
    match = re.exec(text);
    if (match != null) {
        return Number(match[2]);
    } else {
        return null;
    }
}  


note.addEventListener('input', () => {
    age_match = age_parser(note.value);
    if (age_match != null) {
        age.value = age_match;
    }
    gen_match = gen_parser(note.value);
    if (gen_match != null) {
        gen.value = gen_match;
    }
    race_match = race_parser(note.value);
    if (race_match != null) {
        race.value = race_match;
    }
    dm_match = dm_parser(note.value);
    if (dm_match != null) {
        dm.value = dm_match
    }
    sbp_match = sbp_parser(note.value);
    if (sbp_match != null) {
        sbp.value = sbp_match
    }
    hrx_match = hrx_parser(note.value);
    if (hrx_match != null) {
        hrx.value = hrx_match
    }
    sm_match = sm_parser(note.value);
    if (sm_match != null) {
        sm.value = sm_match;
    }
    tchol_match = tchol_parser(note.value);
    if (tchol_match != null) {
        tchol.value = tchol_match;
    }
    hdl_match = hdl_parser(note.value);
    if (hdl_match != null) {
        hdl.value = hdl_match;
    }
});

clrbtn.addEventListener("click", ()=>{
    location.replace(location.href)
})