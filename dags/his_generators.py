"""
his_generators.py — Full HIS, 22 tables, 1 function = 1 table
"""
import random
import uuid
from datetime import datetime, timedelta
from faker import Faker
fake = Faker("th_TH")

PAYMENT_SCHEMES  = ["UCS","SSS","CSMBS","LGO","Self-pay","Private Insurance"]
PAYMENT_WEIGHTS  = [0.45, 0.22, 0.10,   0.04, 0.09,      0.10]
VISIT_TYPES   = ["OPD","IPD","ER"]
VISIT_WEIGHTS = [0.66,  0.21, 0.13]
SPECIALTIES   = ["General Practice","Internal Medicine","Pediatrics","Surgery","Orthopedics",
                  "ENT","Dermatology","Ophthalmology","OB-GYN","Psychiatry","Neurology",
                  "Cardiology","Endocrinology","Oncology","Anesthesiology","Emergency Medicine",
                  "Radiology","Pathology","ICU / Critical Care"]
DEPARTMENTS = {
    "OPD": ["General Practice","Internal Medicine","Pediatrics","Surgery","Orthopedics",
            "ENT","Dermatology","Ophthalmology","OB-GYN","Psychiatry","Neurology",
            "Cardiology","Endocrinology"],
    "IPD": ["Internal Medicine","Pediatrics","Surgery","Orthopedics","ICU / Critical Care",
            "Neurology","Cardiology","OB-GYN","Oncology"],
    "ER":  ["Emergency Medicine"],
}
DEPT_WARD_MAP = {
    "Internal Medicine":   ["Ward Med-A","Ward Med-B"],
    "Pediatrics":          ["Ward Peds"],
    "Surgery":             ["Ward Surg-A","Ward Surg-B"],
    "Orthopedics":         ["Ward Ortho"],
    "ICU / Critical Care": ["ICU"],
    "Neurology":           ["Ward Neuro"],
    "Cardiology":          ["Ward Cardio","CCU"],
    "OB-GYN":              ["Maternity Ward"],
    "Oncology":            ["Ward Onco"],
}
WARD_DEFS = [
    ("Ward Med-A","General",30),("Ward Med-B","General",30),
    ("Ward Peds","Pediatric",20),("Ward Surg-A","Surgical",25),
    ("Ward Surg-B","Surgical",25),("Ward Ortho","Orthopedic",20),
    ("ICU","Intensive Care",10),("Ward Neuro","Neurological",20),
    ("Ward Cardio","Cardiac",20),("CCU","Cardiac Intensive",8),
    ("Maternity Ward","Obstetric",15),("Ward Onco","Oncology",15),
    ("ER Hold","Emergency",8),
]
ICD10_POOL = [
    ("J06.9","Acute upper respiratory infection",     ["any"],            ["OPD","ER"]),
    ("J18.9","Pneumonia, unspecified",                ["any"],            ["OPD","IPD","ER"]),
    ("J45.9","Asthma, unspecified",                   ["any"],            ["OPD","IPD","ER"]),
    ("A09",  "Acute gastroenteritis",                 ["any"],            ["OPD","ER"]),
    ("K29.7","Gastritis, unspecified",                ["adult","elderly"],["OPD","ER"]),
    ("M54.5","Low back pain",                         ["adult","elderly"],["OPD","ER"]),
    ("I10",  "Essential hypertension",                ["adult","elderly"],["OPD","IPD"]),
    ("E11.9","Type 2 diabetes mellitus",              ["adult","elderly"],["OPD","IPD"]),
    ("E78.5","Hyperlipidaemia, unspecified",          ["adult","elderly"],["OPD"]),
    ("N39.0","Urinary tract infection",               ["any"],            ["OPD","ER","IPD"]),
    ("F32.9","Depressive episode, unspecified",       ["adult"],          ["OPD"]),
    ("S09.9","Unspecified injury of head",            ["any"],            ["ER","IPD"]),
    ("I21.9","Acute myocardial infarction",           ["elderly"],        ["ER","IPD"]),
    ("I63.9","Cerebral infarction, unspecified",      ["elderly"],        ["ER","IPD"]),
    ("Z00.0","General adult medical examination",     ["adult"],          ["OPD"]),
    ("O80",  "Single spontaneous delivery",           ["female"],         ["IPD"]),
    ("K35.9","Acute appendicitis",                    ["any"],            ["ER","IPD"]),
    ("G40.9","Epilepsy, unspecified",                 ["any"],            ["OPD","ER","IPD"]),
    ("N18.3","Chronic kidney disease stage 3",        ["elderly"],        ["OPD","IPD"]),
    ("L50.0","Allergic urticaria",                    ["any"],            ["OPD","ER"]),
    ("J96.0","Acute respiratory failure",             ["elderly"],        ["ER","IPD"]),
    ("M17.1","Primary gonarthrosis (knee OA)",        ["elderly"],        ["OPD","IPD"]),
    ("C34.9","Malignant neoplasm of bronchus/lung",   ["elderly"],        ["IPD","OPD"]),
    ("Z51.1","Chemotherapy session",                  ["adult","elderly"],["IPD","OPD"]),
    ("A15.0","Pulmonary tuberculosis",                ["adult"],          ["IPD","OPD"]),
]
LAB_POOL = [
    ("LAB001","CBC",                           150.0,["any"]),
    ("LAB002","Blood glucose (FBS)",            80.0,["E11","E10","Z00"]),
    ("LAB003","HbA1c",                         280.0,["E11","E10"]),
    ("LAB004","Lipid profile",                 350.0,["E78","I10","I21","Z00"]),
    ("LAB005","Renal function test (BUN/Cr)",  320.0,["N18","N39","I10","E11"]),
    ("LAB006","Liver function test (LFT)",     350.0,["any"]),
    ("LAB007","Cardiac enzyme (Troponin I)",   650.0,["I21","I20"]),
    ("LAB008","Urinalysis",                    100.0,["N39","N18","E11"]),
    ("LAB009","Electrolytes (Na/K/Cl)",        220.0,["J96","I21","N18"]),
    ("LAB010","Coagulation (PT/aPTT)",         280.0,["I21","I63","K35"]),
    ("LAB011","Blood culture",                 450.0,["J18","A09","N39"]),
    ("LAB012","COVID-19 Ag rapid test",         90.0,["J06","J18"]),
    ("LAB013","Thyroid function (TSH/FT4)",    420.0,["any"]),
    ("IMG001","Chest X-ray (PA)",              500.0,["J18","J45","I21","J96","any"]),
    ("IMG002","CT Brain",                     4000.0,["S09","I63","G40"]),
    ("IMG003","Ultrasound abdomen",           1200.0,["K35","K29","N39"]),
    ("IMG004","Echocardiogram",               3500.0,["I21","I10"]),
    ("IMG005","MRI Brain",                    8000.0,["I63","G40"]),
    ("PRO001","12-lead ECG",                   350.0,["I21","I10","I20","any"]),
    ("PRO002","Spirometry",                    600.0,["J45"]),
]
DRUG_POOL = [
    ("D001","Amoxicillin",     "500 mg",  "tab",    15.0,["J06","J18","N39"]),
    ("D002","Paracetamol",     "500 mg",  "tab",     3.0,["any"]),
    ("D003","Omeprazole",      "20 mg",   "cap",    20.0,["K29","any"]),
    ("D004","Metformin",       "500 mg",  "tab",    12.0,["E11","E10"]),
    ("D005","Amlodipine",      "5 mg",    "tab",    18.0,["I10"]),
    ("D006","Ibuprofen",       "400 mg",  "tab",     8.0,["M54","M17","L50"]),
    ("D007","Simvastatin",     "20 mg",   "tab",    25.0,["E78","I10"]),
    ("D008","Salbutamol",      "100 mcg", "inhaler",180.0,["J45"]),
    ("D009","Aspirin",         "81 mg",   "tab",     5.0,["I21","I10","I20"]),
    ("D010","Atorvastatin",    "20 mg",   "tab",    35.0,["E78","I21","I10"]),
    ("D011","Losartan",        "50 mg",   "tab",    28.0,["I10","N18"]),
    ("D012","Insulin glargine","100U/mL", "vial",  380.0,["E11","E10"]),
    ("D013","Clopidogrel",     "75 mg",   "tab",    45.0,["I21","I63"]),
    ("D014","Warfarin",        "5 mg",    "tab",    12.0,["I63","I21"]),
    ("D015","Prednisolone",    "5 mg",    "tab",     6.0,["J45","L50","any"]),
    ("D016","Cetirizine",      "10 mg",   "tab",    10.0,["L50","J06"]),
    ("D017","Sertraline",      "50 mg",   "tab",    55.0,["F32"]),
    ("D018","Phenytoin",       "100 mg",  "cap",    18.0,["G40"]),
    ("D019","Ciprofloxacin",   "500 mg",  "tab",    25.0,["N39","A09"]),
    ("D020","Ondansetron",     "4 mg",    "tab",    22.0,["A09","Z51"]),
    ("D021","Morphine",        "10mg/mL", "amp",   150.0,["I21","K35","any"]),
    ("D022","Vancomycin",      "500 mg",  "vial",  280.0,["J18","A09"]),
    ("D023","Enoxaparin",      "40 mg",   "syringe",320.0,["I21","I63"]),
    ("D024","Dexamethasone",   "4mg/mL",  "amp",    45.0,["J45","J96","any"]),
    ("D025","Oxytocin",        "10IU/mL", "amp",    80.0,["O80"]),
]
PROC_MINOR = [
    ("PR001","IV cannula insertion",       350.0,["any"]),
    ("PR002","Wound suture",               800.0,["S09","K35"]),
    ("PR003","Wound dressing",             200.0,["S09","K35","any"]),
    ("PR004","Nasogastric tube insertion", 450.0,["J96","I21"]),
    ("PR005","Urinary catheter insertion", 400.0,["N18","N39","any"]),
    ("PR006","Chest physiotherapy",        500.0,["J18","J45","J96"]),
    ("PR007","Blood transfusion",         2500.0,["any"]),
    ("PR008","Pleural tap",               3500.0,["J18","J96"]),
]
PROC_OR = [
    ("OR001","Appendectomy",           25000.0,["K35"]),
    ("OR002","Cesarean section",       35000.0,["O80"]),
    ("OR003","Coronary angiography",   45000.0,["I21","I20"]),
    ("OR004","Total knee replacement", 80000.0,["M17"]),
    ("OR005","Craniotomy",             90000.0,["S09","I63"]),
    ("OR006","Laparotomy",             30000.0,["K35"]),
    ("OR007","Cholecystectomy",        28000.0,["K29"]),
    ("OR008","Lobectomy (lung)",      120000.0,["C34"]),
]
BLOOD_TYPES    = ["A+","A-","B+","B-","AB+","AB-","O+","O-"]
BLOOD_WEIGHTS  = [0.28,0.05,0.26,0.05,0.08,0.01,0.26,0.01]
NATIONALITY_POOL    = ["TH","MM","LA","KH","VN","PH","CN","IN"]
NATIONALITY_WEIGHTS = [0.88,0.04,0.02,0.02,0.01,0.01,0.01,0.01]
DISCHARGE_TYPES   = ["Recovered","Improved","Transferred","AMA","Expired","Refer out"]
DISCHARGE_WEIGHTS = [0.55,0.30,0.07,0.04,0.02,0.02]
TRIAGE_LEVELS  = ["Resuscitation","Emergent","Urgent","Less-urgent","Non-urgent"]
TRIAGE_WEIGHTS = [0.03,0.12,0.35,0.35,0.15]
SCHEME_COVERAGE = {"UCS":1.00,"SSS":0.90,"CSMBS":1.00,"LGO":1.00,"Self-pay":0.00,"Private Insurance":0.80}
VISIT_FEE_BASE  = {"OPD":150.0,"ER":500.0,"IPD":800.0}

# ── helpers ──────────────────────────────────────────────────────────────────
def _uid(p,n): return f"{p}{n:08d}"
def _fuid(p): return f"{p}{uuid.uuid4().hex[:12].upper()}"
def _rand_dt(s,e):
    delta=max(1,int((e-s).total_seconds()))
    return s+timedelta(seconds=random.randint(0,delta))
def _age(dob):
    d=datetime.fromisoformat(dob); t=datetime.today()
    return t.year-d.year-((t.month,t.day)<(d.month,d.day))
def _agegrp(age):
    return "child" if age<18 else ("adult" if age<65 else "elderly")
def _icd(agegrp,gender,vtype):
    e=[(c,d) for c,d,ags,vts in ICD10_POOL
       if ("any" in ags or agegrp in ags or ("female" in ags and gender=="F")) and vtype in vts]
    return random.choice(e or [("Z00.0","General adult medical examination")])
def _labs(icd,nrange):
    pfx=icd[:3]
    pri=[x for x in LAB_POOL if pfx in x[3] or "any" in x[3]]
    oth=[x for x in LAB_POOL if x not in pri]
    pool=pri+random.sample(oth,min(3,len(oth)))
    lo,hi=nrange
    chosen=random.sample(pool,random.randint(lo,min(hi,len(pool))))
    return [{"item_code":c,"item_name":n,"quantity":1,"unit_price":p,"total_price":round(p,2)} for c,n,p,_ in chosen]
def _drugs(icd,vtype,nrange):
    pfx=icd[:3]
    pri=[x for x in DRUG_POOL if pfx in x[5] or "any" in x[5]]
    oth=[x for x in DRUG_POOL if x not in pri]
    pool=pri+random.sample(oth,min(2,len(oth)))
    lo,hi=nrange
    chosen=random.sample(pool,random.randint(lo,min(hi,len(pool))))
    rows=[]
    for code,name,strength,unit,price,_ in chosen:
        qty=random.randint(7,30) if vtype in("OPD","ER") else random.randint(1,5)
        rows.append({"drug_code":code,"drug_name":name,"strength":strength,"unit":unit,
                     "quantity":qty,"unit_price":price,"total_price":round(qty*price,2)})
    return rows

# ════════════════════════════════════════════════════════════════════════
# MASTER DATA
# ════════════════════════════════════════════════════════════════════════

def doctor(n: int = 250) -> list[dict]:
    """Doctor master. PK: doctor_id"""
    records=[]
    for i in range(1,n+1):
        g=random.choice(["M","F"]); spec=random.choice(SPECIALTIES)
        name=("นพ. "+fake.name_male()) if g=="M" else ("พญ. "+fake.name_female())
        records.append({"doctor_id":_uid("DR",i),"name":name,"gender":g,"specialty":spec,
            "license_no":fake.numerify("ว#####"),"phone":fake.phone_number(),
            "email":fake.email(),"department":spec,
            "employment_type":random.choices(["Full-time","Part-time","Visiting"],weights=[0.70,0.20,0.10])[0],
            "active":random.choices([True,False],weights=[0.95,0.05])[0]})
    return records


def nurse(n: int = 350) -> list[dict]:
    """Nurse master. PK: nurse_id"""
    wards_all=[w for w,_,_ in WARD_DEFS]+["OPD Clinic","ER","OR"]
    records=[]
    for i in range(1,n+1):
        g=random.choices(["M","F"],weights=[0.10,0.90])[0]
        records.append({"nurse_id":_uid("NS",i),
            "name":fake.name_male() if g=="M" else fake.name_female(),
            "gender":g,"license_no":fake.numerify("พ#######"),
            "phone":fake.phone_number(),"ward":random.choice(wards_all),
            "shift":random.choice(["Morning","Afternoon","Night"]),
            "active":random.choices([True,False],weights=[0.97,0.03])[0]})
    return records


def ward_master() -> list[dict]:
    """Ward/unit master. PK: ward_id"""
    records=[]
    for i,(name,wtype,total) in enumerate(WARD_DEFS,1):
        avail=random.randint(max(0,total-5),total)
        records.append({"ward_id":_uid("WD",i),"ward_name":name,"ward_type":wtype,
            "total_beds":total,"available_beds":avail,
            "floor":random.choice(["1F","2F","3F","4F","5F","6F", "7F","8F","9F","10F"]),
            "building":random.choice(["Main","Tower A","Tower B", "Tower C","Tower D"]),"active":True})
    return records


def drug_inventory() -> list[dict]:
    """Drug/supply inventory master. PK: drug_id (= drug_code in drug_order)"""
    records=[]
    for code,name,strength,unit,price,_ in DRUG_POOL:
        qty=random.randint(100,5000)
        records.append({"drug_id":code,"drug_name":name,"strength":strength,"unit":unit,
            "unit_price":price,"qty_onhand":qty,"reorder_level":random.randint(20,100),
            "storage_condition":random.choice(["Room temp","Refrigerated","Frozen","Cool & dry"]),
            "expiry_date":str((datetime.today()+timedelta(days=random.randint(180,730))).date()),
            "supplier":random.choice(["Great Eastern Drug","Siam Pharma","Medicross",
                                      "Bangkok Drug","Thai Pharma","Mega Lifesciences"]),
            "active":True})
    return records


# ════════════════════════════════════════════════════════════════════════
# PATIENT CORE
# ════════════════════════════════════════════════════════════════════════

def patient_profile(n: int = 2000) -> list[dict]:
    """Master patient registry. PK: hn — seed by i เพื่อให้ข้อมูลคงที่ทุกรอบ"""
    records=[]; today=datetime.today()
    for i in range(1,n+1):
        rng=random.Random(i)          # seed ด้วย i → HN เดิม = ข้อมูลเดิมทุกครั้ง
        fake_seeded=Faker("th_TH"); Faker.seed(i)
        g=rng.choice(["M","F"])
        agegrp=rng.choices(["child","adult","elderly"],weights=[0.20,0.60,0.20])[0]
        age_days={"child":rng.randint(0,17*365),"adult":rng.randint(18*365,64*365),
                  "elderly":rng.randint(65*365,90*365)}[agegrp]
        dob=str((today-timedelta(days=age_days)).date())
        records.append({"hn":_uid("HN",i),
            "name":fake_seeded.name_male() if g=="M" else fake_seeded.name_female(),
            "dob":dob,"gender":g,"id_card":fake_seeded.numerify("###############"),
            "phone":fake_seeded.phone_number(),"address":fake_seeded.address().replace("\n"," "),
            "blood_type":rng.choices(BLOOD_TYPES,weights=BLOOD_WEIGHTS)[0],
            "nationality":rng.choices(NATIONALITY_POOL,weights=NATIONALITY_WEIGHTS)[0],
            "payment_scheme":rng.choices(PAYMENT_SCHEMES,weights=PAYMENT_WEIGHTS)[0],
            "allergy_flag":rng.choices(["Y","N"],weights=[0.15,0.85])[0],
            "emergency_contact_name":fake_seeded.name(),
            "emergency_contact_phone":fake_seeded.phone_number(),
            "registered_date":str((today-timedelta(days=rng.randint(180,3650))).date())})
    return records


def appointment(profiles: list[dict], doctors: list[dict],
                n: int = 800, start_date: str = "2024-01-01",
                end_date: str = "2024-12-31") -> list[dict]:
    """OPD appointment scheduling. PK: appt_id  FK: hn, doctor_id"""
    start=datetime.fromisoformat(start_date); end=datetime.fromisoformat(end_date)
    records=[]
    for i in range(1,n+1):
        pt=random.choice(profiles); doc=random.choice(doctors)
        dt=_rand_dt(start,end).replace(hour=random.choice([9,10,11,13,14,15,16]),
                                        minute=random.choice([0,15,30,45]),second=0)
        status=random.choices(["Scheduled","Completed","Cancelled","No-show"],
                               weights=[0.20,0.65,0.10,0.05])[0]
        records.append({"appt_id":_fuid("AP"),
            "hn":pt["hn"],                              # FK → patient_profile
            "doctor_id":doc["doctor_id"],               # FK → doctor
            "department":doc["specialty"],
            "appt_date":str(dt),
            "appt_type":random.choice(["Follow-up","New case","Lab result review","Procedure"]),
            "chief_complaint":random.choice(["ปวดศีรษะ","ไข้","ไอ","เจ็บหน้าอก","ปวดท้อง",
                                              "ปวดหลัง","ตรวจสุขภาพ","ติดตามผล","ปวดข้อ","นอนไม่หลับ"]),
            "duration_min":random.choice([15,20,30,45,60]),"status":status,
            "cancel_reason":random.choice(["Patient request","Doctor unavailable",None])
                           if status in("Cancelled","No-show") else None,
            "created_at":str((dt-timedelta(days=random.randint(1,30))).date())})
    return records


def patient_visit(profiles: list[dict], doctors: list[dict], wards: list[dict],
                  n: int = 900, start_date: str = "2024-01-01",
                  end_date: str = "2024-12-31") -> list[dict]:
    """OPD/IPD/ER encounters. PK: visit_id  FK: hn, doctor_id, ward_id"""
    start=datetime.fromisoformat(start_date); end=datetime.fromisoformat(end_date)
    ward_map={w["ward_name"]:w["ward_id"] for w in wards}
    records=[]
    for i in range(1,n+1):
        pt=random.choice(profiles)
        vtype=random.choices(VISIT_TYPES,weights=VISIT_WEIGHTS)[0]
        vdt=_rand_dt(start,end)
        age=_age(pt["dob"]); agegrp=_agegrp(age)
        icd_code,icd_desc=_icd(agegrp,pt["gender"],vtype)
        dept=random.choice(DEPARTMENTS[vtype])
        spec_docs=[d for d in doctors if d["specialty"]==dept and d["active"]]
        doc=random.choice(spec_docs if spec_docs else doctors)
        los=0; ward_id=None
        if vtype=="IPD":
            los=max(1,int(random.gauss(5.5 if agegrp=="elderly" else 4.0,2)))
            wname=random.choice(DEPT_WARD_MAP.get(dept,["Ward Med-A"]))
            ward_id=ward_map.get(wname)
        elif vtype=="ER":
            los=random.choices([0,1],weights=[0.78,0.22])[0]
            ward_id=ward_map.get("ER Hold")
        triage=random.choices(TRIAGE_LEVELS,weights=TRIAGE_WEIGHTS)[0] if vtype=="ER" else None
        records.append({"visit_id":_fuid("VN"),
            "hn":pt["hn"],                              # FK → patient_profile
            "doctor_id":doc["doctor_id"],               # FK → doctor
            "ward_id":ward_id,                          # FK → ward_master
            "visit_type":vtype,"department":dept,
            "visit_date":str(vdt),"discharge_date":str(vdt+timedelta(days=los)),
            "los_days":los,"triage_level":triage,"payment_scheme":pt["payment_scheme"],
            "primary_icd10":icd_code,"primary_icd_desc":icd_desc,
            "age_at_visit":age,"gender":pt["gender"],"status":"Discharged"})
    return records


def queue(visits: list[dict]) -> list[dict]:
    """OPD/ER daily queue. PK: queue_id  FK: visit_id, hn"""
    records=[]
    for i,v in enumerate([v for v in visits if v["visit_type"] in("OPD","ER")],1):
        arrive=datetime.fromisoformat(v["visit_date"])
        call=arrive+timedelta(minutes=random.randint(5,90))
        seen=call+timedelta(minutes=random.randint(0,20))
        records.append({"queue_id":_fuid("QU"),
            "visit_id":v["visit_id"],                   # FK → patient_visit
            "hn":v["hn"],                               # FK → patient_profile
            "queue_number":f"{v['department'][:3].upper()}-{random.randint(1,300):03d}",
            "queue_type":"Walk-in" if v["visit_type"]=="OPD" else "Emergency",
            "arrived_at":str(arrive),"called_at":str(call),"seen_at":str(seen),
            "wait_min":int((call-arrive).total_seconds()//60),
            "department":v["department"],
            "status":random.choices(["Completed","Waiting","Called","No-show"],
                                     weights=[0.85,0.05,0.05,0.05])[0]})
    return records


def patient_admission(visits: list[dict], wards: list[dict],
                       nurses: list[dict]) -> list[dict]:
    """IPD ward/bed assignment. PK: admission_id  FK: visit_id, hn, ward_id, nurse_id"""
    ward_map={w["ward_name"]:w["ward_id"] for w in wards}
    records=[]
    for i,v in enumerate([v for v in visits if v["visit_type"]=="IPD"],1):
        dept=v["department"]
        wname=random.choice(DEPT_WARD_MAP.get(dept,["Ward Med-A"]))
        ns=random.choice(nurses)
        records.append({"admission_id":_fuid("AD"),
            "visit_id":v["visit_id"],                   # FK → patient_visit
            "hn":v["hn"],                               # FK → patient_profile
            "ward_id":ward_map.get(wname),              # FK → ward_master
            "nurse_id":ns["nurse_id"],                  # FK → nurse
            "ward_name":wname,"bed_no":f"{wname.split()[-1][:3]}-{random.randint(1,40):02d}",
            "admit_date":v["visit_date"],"discharge_date":v["discharge_date"],
            "los_days":v["los_days"],"attending_dr":v["doctor_id"],
            "discharge_type":random.choices(DISCHARGE_TYPES,weights=DISCHARGE_WEIGHTS)[0],
            "diet_order":random.choice(["Regular","Soft","Low-salt","Diabetic","NPO"]),
            "nursing_note":random.choice(["Stable condition throughout admission.",
                "Required oxygen support; improved.","Pain controlled. Ambulated on day 3.",
                "Post-operative recovery uneventful.","Transferred from ICU on day 2."])})
    return records


# ════════════════════════════════════════════════════════════════════════
# CLINICAL
# ════════════════════════════════════════════════════════════════════════

def vital_signs(visits: list[dict], nurses: list[dict]) -> list[dict]:
    """Vital signs (1-4 sets/visit). PK: vs_id  FK: visit_id, hn, nurse_id"""
    n_sets={"OPD":1,"ER":2,"IPD":4}
    records=[]; counter=1
    for v in visits:
        vdt=datetime.fromisoformat(v["visit_date"]); age=v.get("age_at_visit",35)
        for j in range(n_sets[v["visit_type"]]):
            ns=random.choice(nurses)
            sbp=max(70,min(int(random.gauss(125 if age<65 else 140,15)),220))
            dbp=max(40,min(int(random.gauss(80 if age<65 else 88,10)),140))
            records.append({"vs_id":_fuid("VS"),
                "visit_id":v["visit_id"],               # FK → patient_visit
                "hn":v["hn"],                           # FK → patient_profile
                "nurse_id":ns["nurse_id"],              # FK → nurse
                "recorded_at":str(vdt+timedelta(hours=j*6)),
                "sbp":sbp,"dbp":dbp,
                "hr":max(40,min(int(random.gauss(78,12)),160)),
                "temperature":max(35.0,min(round(random.gauss(36.8,0.4),1),41.0)),
                "rr":max(10,min(int(random.gauss(18,3)),40)),
                "spo2":max(80.0,min(round(random.gauss(98.0,1.2),1),100.0)),
                "weight_kg":round(random.gauss(62,12),1) if j==0 else None,
                "height_cm":random.randint(145,185) if j==0 else None,
                "pain_score":random.randint(0,10),
                "consciousness":random.choices(["Alert","Drowsy","Stupor","Coma"],
                                                weights=[0.90,0.07,0.02,0.01])[0]})
            counter+=1
    return records


def drug_allergy(profiles: list[dict]) -> list[dict]:
    """Drug allergy records (allergy_flag=Y patients). PK: allergy_id  FK: hn"""
    allergens=[("Penicillin","Urticaria, angioedema"),("Amoxicillin","Rash, pruritus"),
               ("Aspirin","Bronchospasm, urticaria"),("NSAIDs","GI bleeding, bronchospasm"),
               ("Sulfonamide","Stevens-Johnson syndrome"),("Codeine","Nausea, vomiting"),
               ("Contrast media","Anaphylaxis"),("Metformin","GI intolerance"),("Latex","Contact dermatitis")]
    records=[]; counter=1
    for p in profiles:
        if p.get("allergy_flag")!="Y": continue
        for drug_name,reaction in random.sample(allergens,random.choices([1,2,3],weights=[0.70,0.20,0.10])[0]):
            records.append({"allergy_id":_uid("AL",counter),
                "hn":p["hn"],                           # FK → patient_profile
                "allergen":drug_name,"reaction":reaction,
                "severity":random.choices(["Mild","Moderate","Severe","Life-threatening"],
                                           weights=[0.40,0.35,0.20,0.05])[0],
                "onset_date":str((datetime.today()-timedelta(days=random.randint(30,3000))).date()),
                "verified_by":_uid("DR",random.randint(1,80)),"active":True})
            counter+=1
    return records


def doctor_note(visits: list[dict], doctors: list[dict]) -> list[dict]:
    """SOAP/progress notes (1/visit, daily for IPD). PK: note_id  FK: visit_id, hn, doctor_id"""
    subj=["ผู้ป่วยมาด้วยไข้ ไอ มีเสมหะ 3 วัน","เจ็บหน้าอกซ้าย แน่น เหนื่อยง่าย",
          "ปวดท้องส่วนล่างขวา คลื่นไส้","ปวดหลังเรื้อรัง ร้าวลงขา","ควบคุมน้ำตาลไม่ได้",
          "ความดันสูง มาตรวจตามนัด","ผื่นคัน ลมพิษ หลังรับประทานยา"]
    plan=["Stable. Continue regimen.","Responded to treatment. Labs ordered.",
          "Condition improving. Plan discharge tomorrow.","High-risk. Consult ordered.",
          "Requires further investigation."]
    records=[]; counter=1
    for v in visits:
        n_notes=max(1,min(v["los_days"] if v["visit_type"]=="IPD" else 1,7))
        vdt=datetime.fromisoformat(v["visit_date"])
        for day in range(n_notes):
            records.append({"note_id":_fuid("DN"),
                "visit_id":v["visit_id"],               # FK → patient_visit
                "hn":v["hn"],                           # FK → patient_profile
                "doctor_id":v["doctor_id"],             # FK → doctor
                "note_date":str(vdt+timedelta(days=day)),
                "note_type":"Admission note" if day==0 else "Progress note",
                "subjective":random.choice(subj),
                "objective":f"BP {random.randint(100,160)}/{random.randint(60,100)}, HR {random.randint(60,100)}, Temp {round(random.uniform(36.5,38.5),1)}°C",
                "assessment":f"{v['primary_icd10']} — {v['primary_icd_desc']}",
                "plan":random.choice(plan),"created_at":str(vdt+timedelta(days=day))})
            counter+=1
    return records


def nursing_assessment(visits: list[dict], nurses: list[dict]) -> list[dict]:
    """Nursing assessments (1/visit, daily for IPD). PK: assess_id  FK: visit_id, hn, nurse_id"""
    records=[]; counter=1
    for v in visits:
        n=max(1,min(v["los_days"] if v["visit_type"]=="IPD" else 1,7))
        vdt=datetime.fromisoformat(v["visit_date"])
        for day in range(n):
            ns=random.choice(nurses)
            records.append({"assess_id":_fuid("NA"),
                "visit_id":v["visit_id"],               # FK → patient_visit
                "hn":v["hn"],                           # FK → patient_profile
                "nurse_id":ns["nurse_id"],              # FK → nurse
                "assess_date":str(vdt+timedelta(days=day)),
                "fall_risk":random.choices(["Low","Medium","High"],weights=[0.65,0.25,0.10])[0],
                "pressure_ulcer_risk":random.choices(["Low","Medium","High"],weights=[0.70,0.20,0.10])[0],
                "nutrition_status":random.choices(["Normal","At risk","Malnourished"],weights=[0.70,0.20,0.10])[0],
                "pain_score":random.randint(0,10),
                "mobility":random.choices(["Independent","Assisted","Bed rest"],weights=[0.60,0.30,0.10])[0],
                "note":random.choice(["Patient cooperative and orientated.","Requires assistance with ADL.",
                    "Sleeping well. Appetite good.","Complains of pain at wound site.","IV site clean."])})
            counter+=1
    return records


def referral(visits: list[dict], doctors: list[dict]) -> list[dict]:
    """Inter-department/hospital referrals (~15% of visits). PK: ref_id  FK: visit_id, hn, doctor_id×2"""
    hospitals=["Ramathibodi Hospital","Siriraj Hospital","BNH Hospital","Bumrungrad Hospital"]
    records=[]; counter=1
    for v in [v for v in visits if random.random()<0.15]:
        rtype=random.choices(["Internal","External"],weights=[0.70,0.30])[0]
        recv=random.choice(doctors)
        records.append({"ref_id":_fuid("RF"),
            "visit_id":v["visit_id"],                   # FK → patient_visit
            "hn":v["hn"],                               # FK → patient_profile
            "referring_dr":v["doctor_id"],              # FK → doctor
            "receiving_dr":recv["doctor_id"],           # FK → doctor
            "ref_type":rtype,
            "ref_to":recv["specialty"] if rtype=="Internal" else random.choice(hospitals),
            "reason":random.choice(["Specialist consultation","Advanced imaging needed",
                "Surgical intervention required","Second opinion","Closer to patient"]),
            "urgency":random.choice(["Routine","Urgent","Emergency"]),
            "ref_date":v["visit_date"],
            "status":random.choices(["Pending","Accepted","Completed","Declined"],
                                     weights=[0.10,0.30,0.55,0.05])[0]})
        counter+=1
    return records


def procedure_order(visits: list[dict], doctors: list[dict],
                     nurses: list[dict]) -> list[dict]:
    """Minor bedside procedures (~40% of visits). PK: proc_id  FK: visit_id, hn, doctor_id, nurse_id"""
    records=[]; counter=1
    for v in [v for v in visits if random.random()<0.40]:
        icd_pfx=v["primary_icd10"][:3]
        pool=[x for x in PROC_MINOR if icd_pfx in str(x) or "any" in x[3]] or PROC_MINOR
        for code,name,price,_ in random.sample(pool,min(random.randint(1,2),len(pool))):
            ns=random.choice(nurses)
            records.append({"proc_id":_fuid("PC"),
                "visit_id":v["visit_id"],               # FK → patient_visit
                "hn":v["hn"],                           # FK → patient_profile
                "doctor_id":v["doctor_id"],             # FK → doctor
                "nurse_id":ns["nurse_id"],              # FK → nurse
                "proc_code":code,"proc_name":name,"unit_price":price,"total_price":round(price,2),
                "performed_at":v["visit_date"],"duration_min":random.randint(5,60),
                "outcome":random.choices(["Successful","Complicated","Aborted"],weights=[0.92,0.06,0.02])[0],
                "note":random.choice(["Procedure without complication.","Patient tolerated well.",
                                      "Sterile technique maintained.","Bleeding controlled."])})
            counter+=1
    return records


def operation_record(visits: list[dict], doctors: list[dict],
                      nurses: list[dict]) -> list[dict]:
    """Surgical/OR cases (~30% of IPD). PK: op_id  FK: visit_id, hn, surgeon_id, anesthetist_id, scrub_nurse_id"""
    anesth_docs=[d for d in doctors if d["specialty"]=="Anesthesiology"] or doctors
    records=[]; counter=1
    for v in [v for v in visits if v["visit_type"]=="IPD" and random.random()<0.30]:
        pfx=v["primary_icd10"][:3]
        pool=[x for x in PROC_OR if pfx in str(x)] or PROC_OR
        code,name,price,_=random.choice(pool)
        anesth=random.choice(anesth_docs); scrub=random.choice(nurses)
        opstart=datetime.fromisoformat(v["visit_date"])+timedelta(hours=random.randint(2,12))
        opmin=random.randint(45,300)
        records.append({"op_id":_fuid("OP"),
            "visit_id":v["visit_id"],                   # FK → patient_visit
            "hn":v["hn"],                               # FK → patient_profile
            "surgeon_id":v["doctor_id"],                # FK → doctor
            "anesthetist_id":anesth["doctor_id"],       # FK → doctor
            "scrub_nurse_id":scrub["nurse_id"],         # FK → nurse
            "op_code":code,"op_name":name,
            "op_start":str(opstart),"op_end":str(opstart+timedelta(minutes=opmin)),
            "duration_min":opmin,
            "anesthesia_type":random.choice(["General","Spinal","Epidural","Local","Sedation"]),
            "op_room":f"OR-{random.randint(1,8):02d}",
            "blood_loss_ml":random.randint(50,1500),
            "op_fee":round(price,2),"anesthesia_fee":round(price*0.20,2),
            "outcome":random.choices(["Successful","Complicated","Converted","Abandoned"],
                                      weights=[0.88,0.08,0.03,0.01])[0],
            "post_op_note":random.choice(["Completed without complication.",
                "Intraoperative bleeding controlled.","Patient transferred to recovery room stable.",
                "Converted to open due to adhesions."])})
        counter+=1
    return records


# ════════════════════════════════════════════════════════════════════════
# DIAGNOSIS & ORDERS
# ════════════════════════════════════════════════════════════════════════

def icd10_diagnosis(visits: list[dict]) -> list[dict]:
    """ICD-10 diagnoses (primary + 0-2 secondary). PK: diag_id  FK: visit_id, hn"""
    records=[]; counter=1
    for v in visits:
        agegrp=_agegrp(v.get("age_at_visit",35))
        records.append({"diag_id":_fuid("DG"),"visit_id":v["visit_id"],"hn":v["hn"],
            "icd10_code":v["primary_icd10"],"icd10_desc":v["primary_icd_desc"],
            "diag_type":"Primary","created_at":v["visit_date"]})
        for _ in range(random.choices([0,1,2],weights=[0.55,0.30,0.15])[0]):
            code,desc=_icd(agegrp,v.get("gender","M"),v["visit_type"])
            records.append({"diag_id":_fuid("DG"),"visit_id":v["visit_id"],"hn":v["hn"],
                "icd10_code":code,"icd10_desc":desc,"diag_type":"Secondary","created_at":v["visit_date"]})
    return records


def lab_order(visits: list[dict], doctors: list[dict]) -> list[dict]:
    """Lab/imaging orders (clinically paired). PK: order_id  FK: visit_id, hn, doctor_id"""
    n_map={"OPD":(0,3),"IPD":(2,6),"ER":(1,5)}
    records=[]; counter=1
    for v in visits:
        for item in _labs(v["primary_icd10"],n_map[v["visit_type"]]):
            status=random.choices(["Completed","Pending","Cancelled"],weights=[0.90,0.07,0.03])[0]
            records.append({"order_id":_fuid("OR"),
                "visit_id":v["visit_id"],               # FK → patient_visit
                "hn":v["hn"],                           # FK → patient_profile
                "doctor_id":v["doctor_id"],             # FK → doctor
                **item,"ordered_at":v["visit_date"],
                "reported_at":str(datetime.fromisoformat(v["visit_date"])+timedelta(hours=random.randint(1,6)))
                             if status=="Completed" else None,
                "status":status}); counter+=1
    return records


def drug_order(visits: list[dict], doctors: list[dict],
               drug_inv: list[dict]) -> list[dict]:
    """Prescription/dispensing (clinically paired). PK: rx_id  FK: visit_id, hn, doctor_id, drug_id"""
    inv_ids={d["drug_id"] for d in drug_inv}
    n_map={"OPD":(1,4),"IPD":(2,6),"ER":(1,4)}
    records=[]; counter=1
    for v in visits:
        for item in _drugs(v["primary_icd10"],v["visit_type"],n_map[v["visit_type"]]):
            records.append({"rx_id":_fuid("RX"),
                "visit_id":v["visit_id"],               # FK → patient_visit
                "hn":v["hn"],                           # FK → patient_profile
                "doctor_id":v["doctor_id"],             # FK → doctor
                "drug_id":item["drug_code"] if item["drug_code"] in inv_ids else None,  # FK → drug_inventory
                **item,"dispensed_at":v["discharge_date"],
                "dispensed_by":_uid("PH",random.randint(1,20)),
                "route":random.choice(["oral","IV","topical","inhalation","SC"]),
                "frequency":random.choice(["OD","BD","TID","QID","PRN","stat"]),
                "duration_days":random.choice([3,5,7,14,30,90])}); counter+=1
    return records


# ════════════════════════════════════════════════════════════════════════
# FINANCE
# ════════════════════════════════════════════════════════════════════════

def billing(visits: list[dict], lab_orders: list[dict], drug_orders: list[dict],
            proc_orders: list[dict], op_records: list[dict]) -> list[dict]:
    """Financial settlement per visit. PK: bill_id  FK: visit_id, hn"""
    def _agg(rows,key="visit_id",val="total_price"):
        d={}
        for r in rows: d[r[key]]=d.get(r[key],0.0)+r[val]
        return d
    lab_c  = _agg([o for o in lab_orders if o.get("status")!="Cancelled"])
    drug_c = _agg(drug_orders)
    proc_c = _agg(proc_orders)
    op_c   = {}
    for op in op_records:
        op_c[op["visit_id"]]=op_c.get(op["visit_id"],0.0)+op["op_fee"]+op["anesthesia_fee"]
    records=[]
    for i,v in enumerate(visits,1):
        vfee=VISIT_FEE_BASE[v["visit_type"]]*(max(1,v["los_days"]) if v["visit_type"]=="IPD" else 1)
        labs=round(lab_c.get(v["visit_id"],0.0),2); drugs=round(drug_c.get(v["visit_id"],0.0),2)
        procs=round(proc_c.get(v["visit_id"],0.0),2); ops=round(op_c.get(v["visit_id"],0.0),2)
        sub=round(vfee+labs+drugs+procs+ops,2)
        rate=SCHEME_COVERAGE.get(v["payment_scheme"],0.0)
        covered=round(sub*rate,2); copay=round(sub-covered,2)
        records.append({"bill_id":_fuid("BL"),
            "visit_id":v["visit_id"],                   # FK → patient_visit
            "hn":v["hn"],                               # FK → patient_profile
            "payment_scheme":v["payment_scheme"],
            "visit_fee":round(vfee,2),"lab_cost":labs,"drug_cost":drugs,
            "procedure_cost":procs,"operation_cost":ops,"subtotal":sub,
            "scheme_coverage_pct":rate*100,"covered_amount":covered,"patient_copay":copay,
            "billed_at":v["discharge_date"],
            "due_date":str(datetime.fromisoformat(v["discharge_date"])+timedelta(days=30)),
            "paid":random.choices([True,False],weights=[0.92,0.08])[0]})
    return records


def payment_transaction(bills: list[dict]) -> list[dict]:
    """Split payment receipts (insurance + OOP). PK: txn_id  FK: bill_id, visit_id, hn"""
    records=[]; counter=1
    for b in [b for b in bills if b["paid"]]:
        if b["covered_amount"]>0:
            records.append({"txn_id":_fuid("PT"),
                "bill_id":b["bill_id"],                 # FK → billing
                "visit_id":b["visit_id"],               # FK → patient_visit
                "hn":b["hn"],                           # FK → patient_profile
                "txn_type":"Insurance Claim","amount":b["covered_amount"],
                "method":b["payment_scheme"],"reference":f"CLM{random.randint(1000000,9999999)}",
                "txn_at":b["billed_at"],"cashier_id":_uid("CS",random.randint(1,15)),"status":"Settled"})
        if b["patient_copay"]>0:
            records.append({"txn_id":_fuid("PT"),
                "bill_id":b["bill_id"],                 # FK → billing
                "visit_id":b["visit_id"],               # FK → patient_visit
                "hn":b["hn"],                           # FK → patient_profile
                "txn_type":"Co-payment","amount":b["patient_copay"],
                "method":random.choices(["Cash","Credit Card","Debit Card","PromptPay","Mobile Banking"],
                                         weights=[0.30,0.25,0.15,0.20,0.10])[0],
                "reference":f"RCP{random.randint(1000000,9999999)}",
                "txn_at":b["billed_at"],"cashier_id":_uid("CS",random.randint(1,15)),"status":"Settled"})
            counter+=1
    return records


def insurance_claim(bills: list[dict]) -> list[dict]:
    """Scheme/insurance claim submissions. PK: claim_id  FK: bill_id, visit_id, hn"""
    insurer_map={"UCS":"สปสช.","SSS":"สำนักงานประกันสังคม","CSMBS":"กรมบัญชีกลาง",
                 "LGO":"อปท.","Private Insurance":"AIA/Muang Thai/FWD","Self-pay":None}
    records=[]; counter=1
    for b in bills:
        ins=insurer_map.get(b["payment_scheme"])
        if not ins or b["covered_amount"]<=0: continue
        sub_dt=datetime.fromisoformat(b["billed_at"])+timedelta(days=random.randint(1,3))
        status=random.choices(["Submitted","Under Review","Approved","Rejected","Partially Approved"],
                               weights=[0.05,0.10,0.70,0.05,0.10])[0]
        approved=b["covered_amount"] if status=="Approved" else (
                  0.0 if status=="Rejected" else round(b["covered_amount"]*random.uniform(0.5,0.9),2))
        records.append({"claim_id":_fuid("IC"),
            "bill_id":b["bill_id"],                     # FK → billing
            "visit_id":b["visit_id"],                   # FK → patient_visit
            "hn":b["hn"],                               # FK → patient_profile
            "payment_scheme":b["payment_scheme"],"insurer":ins,
            "claimed_amount":b["covered_amount"],"approved_amount":approved,
            "rejection_reason":random.choice(["Diagnosis not covered","Incomplete documentation",
                "Exceeded annual limit","Pre-existing condition",None])
                if status in("Rejected","Partially Approved") else None,
            "submitted_at":str(sub_dt),
            "updated_at":str(sub_dt+timedelta(days=random.randint(3,30))),
            "status":status,"claim_ref":f"CLM{random.randint(10000000,99999999)}"})
        counter+=1
    return records


def cost_center(visits: list[dict], bills: list[dict]) -> list[dict]:
    """Cost-center revenue allocation per visit. PK: cc_id  FK: visit_id, bill_id"""
    cc_map={"OPD":"CC-OPD","IPD":"CC-IPD","ER":"CC-ER"}
    bill_map={b["visit_id"]:b for b in bills}
    records=[]; counter=1
    for v in visits:
        b=bill_map.get(v["visit_id"])
        if not b: continue
        sub=b["subtotal"]
        records.append({"cc_id":_fuid("CC"),
            "visit_id":v["visit_id"],                   # FK → patient_visit
            "bill_id":b["bill_id"],                     # FK → billing
            "cost_center_code":cc_map.get(v["visit_type"],"CC-OPD"),
            "department":v["department"],"visit_type":v["visit_type"],
            "revenue":sub,"doctor_fee":round(sub*0.40,2),
            "nursing_facility":round(sub*0.30,2),"consumables":round(sub*0.30,2),
            "period_month":datetime.fromisoformat(v["visit_date"]).strftime("%Y-%m"),
            "recorded_at":v["discharge_date"]})
        counter+=1
    return records