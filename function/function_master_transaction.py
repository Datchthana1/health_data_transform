from function.his_generators import *
from datetime import datetime
from supabase import Client, create_client
from dotenv import load_dotenv
from pathlib import Path
import os
import pendulum

env_path = Path(__file__).parent.parent / "assets/.env"
print("ENV PATH:", env_path, "EXISTS:", env_path.exists())
load_dotenv(env_path)
print("URL:", os.getenv("SUPABASE_URL"))
key = os.getenv("SUPABASE_SERVICE_ROLES")
print("KEY:", key[:20] if key else None)

default_args = {
    "owner": "health_data_transform",
    "depends_on_past": False,
    "start_date": pendulum.datetime(2024, 6, 1, tz=pendulum.timezone("Asia/Bangkok")),
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
}

def get_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLES")
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
    return create_client(url, key)

def check_status(**context):
    client = get_client()
    try:
        client.table("his_doctor").select("doctor_id").limit(1).execute()
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {e}"
        raise
    print(f"Supabase status: {db_status}")
    return db_status

def dim_table_static():
    dim_ward = ward_master()
    return (dim_ward,)

def dim_table_periodic():
    dim_doctor = doctor()
    dim_nurse = nurse()
    return dim_doctor, dim_nurse

def dim_table_daily():
    dim_drug_inventory = drug_inventory()
    return (dim_drug_inventory,)

def dim_table():
    (dim_ward,)           = dim_table_static()
    dim_doctor, dim_nurse = dim_table_periodic()
    (dim_drug_inventory,) = dim_table_daily()
    return dim_doctor, dim_nurse, dim_ward, dim_drug_inventory

def dim_upsert():
    dim_patient = patient_profile()
    dim_allergy = drug_allergy(dim_patient)
    return dim_patient, dim_allergy


def fact_table(current_date: str = datetime.now().strftime("%Y-%m-%d")):
    dim_doctor, dim_nurse, dim_ward, dim_drug_inventory = dim_table()
    dim_patient, dim_allergy = dim_upsert()
    fact_visits = patient_visit(dim_patient, dim_doctor, dim_ward, start_date=current_date, end_date=current_date)
    fact_appointment = appointment(dim_patient, dim_doctor, start_date=current_date, end_date=current_date)
    fact_queue = queue(fact_visits)
    fact_admission = patient_admission(fact_visits, dim_ward, dim_nurse)
    fact_vital_signs = vital_signs(fact_visits, dim_nurse)
    fact_doctor_note = doctor_note(fact_visits, dim_doctor)
    fact_nursing_assessment = nursing_assessment(fact_visits, dim_nurse)
    fact_referral = referral(fact_visits, dim_doctor)
    fact_procedure_order = procedure_order(fact_visits, dim_doctor, dim_nurse)
    fact_operation_record = operation_record(fact_visits, dim_doctor, dim_nurse)
    fact_icd10_diagnosis = icd10_diagnosis(fact_visits)
    fact_lab_order = lab_order(fact_visits, dim_doctor)
    fact_drug_order = drug_order(fact_visits, dim_doctor, dim_drug_inventory)
    fact_billing = billing(fact_visits, fact_lab_order, fact_drug_order, fact_procedure_order, fact_operation_record)
    fact_payment_transaction = payment_transaction(fact_billing)
    fact_insurance_claim = insurance_claim(fact_billing)
    fact_cost_center = cost_center(fact_visits, fact_billing)
    return (fact_visits , 
            fact_appointment , 
            fact_queue , 
            fact_admission , 
            fact_vital_signs , 
            fact_doctor_note , 
            fact_nursing_assessment , 
            fact_referral , 
            fact_procedure_order , 
            fact_operation_record , 
            fact_icd10_diagnosis , 
            fact_lab_order , 
            fact_drug_order , 
            fact_billing , 
            fact_payment_transaction,
            fact_insurance_claim ,
            fact_cost_center)


