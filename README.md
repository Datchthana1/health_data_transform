# health_data_transform
Health Data Processing — A synthetic HIS (Hospital Information System) data pipeline built with Apache Airflow. Generates realistic hospital transaction data (visits, admissions, labs, drugs, billing, etc.) and transforms it into a Star Schema (fact/dim tables) stored in Supabase, following a Medallion Architecture (Bronze → Silver → Gold).
