from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup  # เพิ่ม import
from airflow.timetables.interval import CronDataIntervalTimetable
from airflow.models.param import Param
from datetime import timedelta
from ingest_master_transaction import * #<- แก้ไข import ให้ตรงกับฟังก์ชันที่ใช้

default_args = {
    "owner": "health_data_ingest_master_data",
    "depends_on_past": False,
    "start_date": pendulum.datetime(2024, 6, 1, tz=pendulum.timezone("Asia/Bangkok")),
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
}   

def ingest_master_data_static(**context):
    (dim_ward,) = dim_table_static()
    client = get_client()
    client.table("dim_ward").upsert(dim_ward, ignore_duplicates=True).execute()
    return {"dim_ward": len(dim_ward)}

def ingest_master_data_periodic(**context):
    dim_doctor, dim_nurse = dim_table_periodic()
    client = get_client()
    client.table("dim_doctor").upsert(dim_doctor, ignore_duplicates=True).execute()
    client.table("dim_nurse").upsert(dim_nurse, ignore_duplicates=True).execute()
    return {"dim_doctor": len(dim_doctor), "dim_nurse": len(dim_nurse)}

def ingest_master_data_daily(**context):
    (dim_drug_inventory,) = dim_table_daily()
    client = get_client()
    client.table("dim_drug_inventory").upsert(dim_drug_inventory, ignore_duplicates=True).execute()
    return {"dim_drug_inventory": len(dim_drug_inventory)}

def ingest_upsert_master_data(**context):
    dim_patient, dim_allergy = dim_upsert()
    client = get_client()
    client.table("dim_patient").upsert(dim_patient, ignore_duplicates=True).execute()
    client.table("dim_allergy").upsert(dim_allergy, ignore_duplicates=True).execute()
    return {"dim_patient": len(dim_patient), "dim_allergy": len(dim_allergy)}

with DAG(
    "ingest_master_data_monthly",
    default_args=default_args,
    description="DAG for ingesting master data monthly",
    schedule=CronDataIntervalTimetable("0 0 1 * *", timezone=pendulum.timezone("Asia/Bangkok")),  # รันทุกวันที่ 1 ของเดือน
    catchup=False,  
):
    task_check_supabase_connection = PythonOperator(
        task_id="check_supabase_connection",
        python_callable=check_status,
    )

    with TaskGroup("ingest_master_data_tasks") as ingest_master_data_tasks:
        task_dim_static = PythonOperator(
            task_id="ingest_dim_static",
            python_callable=ingest_master_data_static,
        )
        task_dim_periodic = PythonOperator(
            task_id="ingest_dim_periodic",
            python_callable=ingest_master_data_periodic,
        )
        task_dim_daily = PythonOperator(
            task_id="ingest_dim_daily",
            python_callable=ingest_master_data_daily,
        )
        task_dim_upsert = PythonOperator(
            task_id="ingest_dim_upsert",
            python_callable=ingest_upsert_master_data,
        )
    
    task_check_supabase_connection >> ingest_master_data_tasks