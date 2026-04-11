from dotenv import load_dotenv
from pathlib import Path
from supabase import Client, create_client
from airflow.providers.standard.operators.python import PythonOperator
from airflow import DAG
from airflow.sdk import Param
from datetime import timedelta
import pendulum
from airflow.timetables.interval import CronDataIntervalTimetable
from ingest_master_transaction import *
from datetime import datetime
import os

default_args = {
    "owner": "health_data_ingest_transaction",
    "depends_on_past": False,
    "start_date": pendulum.datetime(2024, 6, 1, tz=pendulum.timezone("Asia/Bangkok")),
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
}   

env_path = Path(__file__).parent.parent / "assets/.env"
print("ENV PATH:", env_path, "EXISTS:", env_path.exists())
load_dotenv(env_path)
print("URL:", os.getenv("SUPABASE_URL"))
key = os.getenv("SUPABASE_SERVICE_ROLES")
print("KEY:", key[:20] if key else None)

def get_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLES")
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
    return create_client(url, key)

def transform_transaction_data():
    client = get_client()
    (fact_visits , 
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
    fact_cost_center) = fact_table(current_date=datetime.now().strftime("%Y-%m-%d"))
    client.table("fact_visits").upsert(fact_visits).execute()
    client.table("fact_appointment").upsert(fact_appointment).execute()
    client.table("fact_queue").upsert(fact_queue).execute()
    client.table("fact_admission").upsert(fact_admission).execute()
    client.table("fact_vital_signs").upsert(fact_vital_signs).execute()
    client.table("fact_doctor_note").upsert(fact_doctor_note).execute()
    client.table("fact_nursing_assessment").upsert(fact_nursing_assessment).execute()
    client.table("fact_referral").upsert(fact_referral).execute()
    client.table("fact_procedure_order").upsert(fact_procedure_order).execute()
    client.table("fact_operation_record").upsert(fact_operation_record).execute()
    client.table("fact_icd10_diagnosis").upsert(fact_icd10_diagnosis).execute()
    client.table("fact_lab_order").upsert(fact_lab_order).execute()
    client.table("fact_drug_order").upsert(fact_drug_order).execute()
    client.table("fact_billing").upsert(fact_billing).execute()
    client.table("fact_payment_transaction").upsert(fact_payment_transaction).execute()
    client.table("fact_insurance_claim").upsert(fact_insurance_claim).execute()
    client.table("fact_cost_center").upsert(fact_cost_center).execute()
    return {
        "fact_visits": len(fact_visits),
        "fact_appointment": len(fact_appointment),
        "fact_queue": len(fact_queue),
        "fact_admission": len(fact_admission),
        "fact_vital_signs": len(fact_vital_signs),
        "fact_doctor_note": len(fact_doctor_note),
        "fact_nursing_assessment": len(fact_nursing_assessment),
        "fact_referral": len(fact_referral),
        "fact_procedure_order": len(fact_procedure_order),
        "fact_operation_record": len(fact_operation_record),
        "fact_icd10_diagnosis": len(fact_icd10_diagnosis),
        "fact_lab_order": len(fact_lab_order),
        "fact_drug_order": len(fact_drug_order),
        "fact_billing": len(fact_billing),
        "fact_payment_transaction": len(fact_payment_transaction),
        "fact_insurance_claim": len(fact_insurance_claim),
        "fact_cost_center": len(fact_cost_center)
    }


with DAG(
    "transform_transaction_daily",
    default_args=default_args,
    description="DAG for transforming transaction data daily",
    schedule=CronDataIntervalTimetable("0 1 * * *", timezone=pendulum.timezone("Asia/Bangkok")),
    params={  # type: ignore[arg-type]
        "current_date": Param(
            default=pendulum.now("Asia/Bangkok").strftime("%Y-%m-%d"),
            type="string",
            description="วันที่ต้องการ ingest (YYYY-MM-DD)",
        ),
    },
    catchup=False,
):
    
    task_check_supabase_connection = PythonOperator(
        task_id="check_supabase_connection",
        python_callable=check_status,
    )

    task_transform_transaction_data = PythonOperator(
        task_id="transform_transaction_data",
        python_callable=transform_transaction_data,
    )

    task_check_supabase_connection >> task_transform_transaction_data
