from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup  # เพิ่ม import
from airflow.timetables.interval import CronDataIntervalTimetable
from airflow.models.param import Param
from datetime import timedelta
from function_master_transaction import * #<- แก้ไข import ให้ตรงกับฟังก์ชันที่ใช้

default_args = {
    "owner": "health_data_ingest_master_data",
    "depends_on_past": False,
    "start_date": pendulum.datetime(2024, 6, 1, tz=pendulum.timezone("Asia/Bangkok")),
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
}   

def ingest_master_data(**context):
    dim_doctor, dim_nurse, dim_ward, dim_drug_inventory = dim_table()
    dim_patient, dim_allergy = dim_upsert()
    client = get_client()
    client.table("his_doctor").upsert(dim_doctor).execute()
    client.table("his_nurse").upsert(dim_nurse).execute()
    client.table("his_ward").upsert(dim_ward).execute()
    client.table("his_drug_inventory").upsert(dim_drug_inventory).execute()
    client.table("his_patient").upsert(dim_patient).execute()
    client.table("his_patient_allergy").upsert(dim_allergy).execute()
    return {
        "his_doctor": len(dim_doctor),
        "his_nurse": len(dim_nurse),
        "his_ward": len(dim_ward),
        "his_drug_inventory": len(dim_drug_inventory),
        "his_patient": len(dim_patient),
        "his_patient_allergy": len(dim_allergy),
    }

with DAG(
    dag_id="ingest_master_data",
    default_args=default_args,
    schedule=CronDataIntervalTimetable("@monthly", timezone="Asia/Bangkok"),
    description="DAG for ingesting master data into the health data warehouse",
    catchup=False,
    tags=["health_data", "master_data"],
):
    check_db = PythonOperator(
        task_id="check_db_connection",
        python_callable=check_status,
    )

    task_ingest_data = PythonOperator(
        task_id="ingest_master_data",
        python_callable=ingest_master_data,
    )

    check_db >> task_ingest_data