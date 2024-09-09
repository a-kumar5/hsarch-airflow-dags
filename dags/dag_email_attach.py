from __future__ import annotations
from airflow.operators.python import PythonOperator

import datetime
import sys

from airflow import DAG
from airflow.models import Variable
from airflow.operators.email import EmailOperator


def dag_failure_callback_handler(context):
    dag_id = context['task_instance'].dag_id
    task_id = context['task_instance'].task_id
    run_id = context['task_instance'].run_id
    execution_date = context['logical_date']
    attempt_number = context['task_instance'].try_number
    attempt_number -= 1
    subject = "FAILURE: Airflow Non-PROD: NEW-STAGE Run No: {0} - Dag ID: {1}".format(run_id, dag_id)
    log_file_path = "/opt/airflow/logs/dag_id={0}/run_id={1}/task_id={2}/attempt={3}.log".format(dag_id, run_id, task_id, attempt_number)


    send_email_on_failure = EmailOperator(
        task_id='send_email_on_failure',
        to=['SHI_HS_AIRFLOW@tranformco.com'],
        cc=['ayush.kumar@transformco.com'],
        files=[log_file_path],
        subject=subject,
        html_content="<br/><hr/><hr/></b> <br><b>DAG Name :</b> {0}<br><b>Execution Date :</b> {1} <br><b>DAG Run Status :</b> <font color=red>FAILURE <br/><b> Log File Path: {2}</font><br><br><hr><hr>".format(
            dag_id, execution_date, log_file_path),
        dag=context['dag'])

    send_email_on_failure.execute(context)


def dag_success_callback_handler(context):
    dag_id = context['task_instance'].dag_id
    run_id = context['task_instance'].run_id
    task_id = context['task_instance'].task_id
    attempt_number = context['task_instance'].try_number
    attempt_number -= 1
    execution_date = context['logical_date']
    subject = "SUCCESS: Airflow Non-PROD: NEW-STAGE  Run No: {0} - Dag ID: {1}".format(run_id, dag_id)
    log_file_path = "/opt/airflow/logs/dag_id={0}/run_id={1}/task_id={2}/attempt={3}.log".format(dag_id, run_id, task_id, attempt_number)


    send_email_on_success = EmailOperator(
        task_id='send_email_on_success',
        to=['SHI_HS_AIRFLOW@tranformco.com'],
        cc=['ayush.kumar@transformco.com'],
        subject=subject,
        html_content="<br/><hr/><hr/></b> <br><b>DAG Name :</b> {0}<br><b>Execution Date :</b> {1} <br><b>DAG Run Status :</b> <font color=green>SUCCESS</font> <br><b> Log File Path: {2}<br><br><hr><hr>".format(
            dag_id, execution_date, log_file_path),
        dag=context['dag'])

    send_email_on_success.execute(context)


def python_task():
    print('hello')


default_args = {
    'owner': 'akumar5',
    'depends_on_past': True,
    'wait_for_downstream': True,
    'email_on_failure': True,
    'email_on_success': True,
    'priority_weight': 5,
    'job_doc': ""
}

dag = DAG(
    dag_id='dag_email_attachment',
    schedule="*/25 * * * *",
    default_args=default_args,
    tags=["Folder:test", "Application:test", "SubApplication:test"],
    start_date=datetime.datetime.now(),
    catchup=False,
    on_success_callback=dag_success_callback_handler
)


python_callable_task = PythonOperator(
    task_id='python_callable_task',
    python_callable=python_task,
    op_args=[],
    dag=dag
)


python_callable_task