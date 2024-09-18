from airflow.decorators import dag, task
from airflow import Dataset
from datetime import datetime, timedelta

data_a = Dataset("s3://bucket_a/data_a")
data_b = Dataset("s3://bucket_b/data_b")

@dag(start_date=datetime(2023,1,1), schedule='@daily', catchup=False, dagrun_timeout=timedelta(minutes=1))
def producer():

    @task
    def task_a(outlets=[data_a]):
        print("A")


    @task
    def task_b(outlets=[data_b]):
        print("B")


    task_a() >> task_b()

producer()

