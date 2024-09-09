from airflow.decorators import task, dag
from airflow.operators.email import EmailOperator
from pendulum import datetime
import requests
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'docs/00AKOSB3-FLSBH_3.md')
path = filename

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
        to=['ayush.kumar@transformco.com'],
        cc=['ayush.kumar@transformco.com'],
        subject=subject,
        html_content="<br/><hr/><hr/></b> <br><b>DAG Name :</b> {0}<br><b>Execution Date :</b> {1} <br><b>DAG Run Status :</b> <font color=green>SUCCESS</font> <br><b> Log File Path: {2}<br><br><hr><hr>".format(
            dag_id, execution_date, log_file_path),
        dag=context['dag'])

    send_email_on_success.execute(context)

default_args = {
    'owner': 'hsbatch',
    'wait_for_downstream': True,
    'depends_on_past': True,
    'email_on_failure': True,
    'email_on_success': True,
    'priority_weight': 5,
}


@dag(
    start_date=datetime(2022,11,1),
    schedule="@daily",
    default_args=default_args,
    tags=["Folder:HS", "Application:ARCH", "SubApplication:INFRA"],
    catchup=False,
    on_success_callback=dag_success_callback_handler,
    doc_md=path
)
def ayush_task_dag():

    @task
    def tell_me_what_to_do():
        response = requests.get("https://bored-api.appbrewery.com/random")
        print(dirname, filename, path, type(path))
        return response.json()["activity"]

    tell_me_what_to_do()

ayush_task_dag()