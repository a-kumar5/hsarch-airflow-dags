from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

def task_in_dag1(**kwargs):
    print("Task in DAG 1")

with DAG(
    dag_id='dag1',
    default_args={'owner': 'airflow'},
    description='First DAG',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
) as dag1:

    start_dag1 = DummyOperator(
        task_id='start_dag1',
    )

    task1_dag1 = PythonOperator(
        task_id='task1_dag1',
        python_callable=task_in_dag1,
        provide_context=True,
    )

    trigger_dag2 = TriggerDagRunOperator(
        task_id='trigger_dag2',
        trigger_dag_id='dag2',
    )

    start_dag1 >> task1_dag1 >> trigger_dag2
