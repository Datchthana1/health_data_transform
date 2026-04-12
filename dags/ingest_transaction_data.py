from airflow.providers.standard.operators.python import PythonOperator
from airflow.timetables.interval import CronDataIntervalTimetable
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from function.function_master_transaction import *
from dotenv import load_dotenv
from datetime import timedelta
from airflow.sdk import Param
from datetime import datetime
from pathlib import Path
from airflow import DAG
import pendulum
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

def ingest_transaction_data():
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
    client.table("his_visits").upsert(fact_visits).execute()
    client.table("his_appointment").upsert(fact_appointment).execute()
    client.table("his_queue").upsert(fact_queue).execute()
    client.table("his_admission").upsert(fact_admission).execute()
    client.table("his_vital_signs").upsert(fact_vital_signs).execute()
    client.table("his_doctor_note").upsert(fact_doctor_note).execute()
    client.table("his_nursing_assessment").upsert(fact_nursing_assessment).execute()
    client.table("his_referral").upsert(fact_referral).execute()
    client.table("his_procedure_order").upsert(fact_procedure_order).execute()
    client.table("his_operation_record").upsert(fact_operation_record).execute()
    client.table("his_icd10_diagnosis").upsert(fact_icd10_diagnosis).execute()
    client.table("his_lab_order").upsert(fact_lab_order).execute()
    client.table("his_drug_order").upsert(fact_drug_order).execute()
    client.table("his_billing").upsert(fact_billing).execute()
    client.table("his_payment_transaction").upsert(fact_payment_transaction).execute()
    client.table("his_insurance_claim").upsert(fact_insurance_claim).execute()
    client.table("his_cost_center").upsert(fact_cost_center).execute()
    return {
        "his_visits": len(fact_visits),
        "his_appointment": len(fact_appointment),
        "his_queue": len(fact_queue),
        "his_admission": len(fact_admission),
        "his_vital_signs": len(fact_vital_signs),
        "his_doctor_note": len(fact_doctor_note),
        "his_nursing_assessment": len(fact_nursing_assessment),
        "his_referral": len(fact_referral),
        "his_procedure_order": len(fact_procedure_order),
        "his_operation_record": len(fact_operation_record),
        "his_icd10_diagnosis": len(fact_icd10_diagnosis),
        "his_lab_order": len(fact_lab_order),
        "his_drug_order": len(fact_drug_order),
        "his_billing": len(fact_billing),
        "his_payment_transaction": len(fact_payment_transaction),
        "his_insurance_claim": len(fact_insurance_claim),
        "his_cost_center": len(fact_cost_center)
    }

with DAG(
    dag_id="ingest_transaction_data",
    default_args=default_args,
    schedule= CronDataIntervalTimetable("@daily", timezone="Asia/Bangkok"),
    description="DAG for ingesting transaction data into the health data warehouse",
    catchup=False,
    tags=["health_data", "transaction_data"],
):
    check_db = PythonOperator(
        task_id="check_db_connection",
        python_callable=check_status,
    )

    task_ingest_transaction = PythonOperator(
        task_id="ingest_transaction_data",
        python_callable=ingest_transaction_data,
    )
    trigger_transform = TriggerDagRunOperator(
        task_id="trigger_transform_transaction_data",
        trigger_dag_id="transform_transaction_data",
        wait_for_completion=False,
    )

    check_db >> task_ingest_transaction >> trigger_transform