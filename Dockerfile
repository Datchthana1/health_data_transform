FROM apache/airflow:3.1.7-python3.12

RUN pip install --no-cache-dir \
    apache-airflow==3.1.7 \
    faker==40.13.0 \
    pendulum==3.2.0 \
    python-dotenv==1.2.2 \
    supabase==2.28.0
