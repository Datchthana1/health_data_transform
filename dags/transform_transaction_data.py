from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.timetables.interval import CronDataIntervalTimetable
from function_master_transaction import *
from airflow.sdk import Param
from datetime import datetime
from pathlib import Path
import pendulum
import os

default_args = {
    "owner": "health_data_ingest_transaction",
    "depends_on_past": False,
    "start_date": pendulum.datetime(2024, 6, 1, tz=pendulum.timezone("Asia/Bangkok")),
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
}  

# def transform_transaction_data():
#     client = get_client()
#     if client.table("")
#     client.rpc(
#         "sql", {
#             "query":"""
            
#             """
#         }
#     )
    