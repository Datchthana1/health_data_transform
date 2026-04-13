from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from function.function_master_transaction import *
from datetime import datetime, timedelta
from pathlib import Path
from script.sql_script import *
from dotenv import load_dotenv
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
    load_dotenv(Path("/opt/airflow/assets/.env"))
    return psycopg2.connect(
        host=os.environ["SUPABASE_DB_HOST"],
        port=6543,
        dbname="postgres",
        user=os.environ["SUPABASE_DB_USER"],
        password=os.environ["SUPABASE_DB_PASSWORD"],
        sslmode="require"
    )

def check_pg_connection():
    conn = get_pg_connect()
    conn.close()
    print("PostgreSQL connection successful")
    return {"status": "connected"}

def transform_dimension_data():
    conn = get_pg_connect()
    cursor = conn.cursor()
    try:
        cursor.execute(INSERT_DIM_PATIENT)
        conn.commit()
        affected = cursor.rowcount
        print(f"Rows affected: {affected}")
        return {"status": "success", "rows_affected": affected}
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

with DAG(
    dag_id="PL2_transform_dimension_data",
    default_args=default_args,
    schedule=None,
    catchup=False,
    tags=["health_data", "dimension_data", "PL2", "transform"],
) as dag:
    task_pg_connection = PythonOperator(
        task_id="check_pg_connection",
        python_callable=check_pg_connection,
    )
    transform_task_dimension = PythonOperator(
        task_id="transform_dimension_data_task",
        python_callable=transform_dimension_data,
    )
    task_pg_connection >> transform_task_dimension