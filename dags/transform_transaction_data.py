from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.timetables.interval import CronDataIntervalTimetable
from function_master_transaction import *
from airflow.sdk import Param
from datetime import datetime
from pathlib import Path
from sql_script import * #<- เพิ่ม import สำหรับ SQL script
import psycopg2
import pendulum
import os

default_args = {
    "owner": "health_data_ingest_transaction",
    "depends_on_past": False,
    "start_date": pendulum.datetime(2024, 6, 1, tz=pendulum.timezone("Asia/Bangkok")),
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
}  

def get_pg_connect():
    return psycopg2.connect(
        host=os.environ["SUPABASE_DB_HOST"],
        port=6543,
        dbname="postgres",
        user=os.environ["SUPABASE_DB_USER"],
        password=os.environ["SUPABASE_DB_PASSWORD"],
        sslmode="require"
    )

def transform_transaction_data():
    conn = get_pg_connect()
    cursor = conn.cursor()

    sql_insert = INSERT_DIM_PATIENT

    try:
        cursor.execute(sql_insert)
        conn.commit()
        affected = cursor.rowcount
        return {"status": "success", "rows_affected": affected}
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

with DAG(
    dag_id="transform_transaction_data",
    default_args=default_args,
    schedule=CronDataIntervalTimetable("0 1 * * *", timezone="Asia/Bangkok"),
) as dag:
    task_check_status = PythonOperator(
        task_id="check_supabase_status",
        python_callable=check_status,
    )
    transform_task = PythonOperator(
        task_id="transform_transaction_data_task",
        python_callable=transform_transaction_data,
    )
    task_check_status >> transform_task