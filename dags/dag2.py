from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

def task_in_dag2(**kwargs):
    print("Task in DAG 2")

with DAG(
    dag_id='dag2',
    default_args={'owner': 'airflow'},
    description='Second DAG',
    schedule_interval=None,  # Only triggered by DAG1
    start_date=days_ago(1),
    catchup=False,
) as dag2:

    start_dag2 = DummyOperator(
        task_id='start_dag2',
    )

    task1_dag2 = PythonOperator(
        task_id='task1_dag2',
        python_callable=task_in_dag2,
        provide_context=True,
    )

    start_dag2 >> task1_dag2