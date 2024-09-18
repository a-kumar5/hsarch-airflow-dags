import requests
from airflow.operators.email import EmailOperator
from airflow.decorators import task, dag
from datetime import datetime

def send_email_on_success(context):
    dag_id = context['task_instance'].dag_id
    run_id = context['task_instance'].run_id
    task_id = context['task_instance'].task_id
    execution_date = context['logical_date']
    subject = "TES: Run No: {0} - Dag ID: {1}".format(run_id, dag_id),

    send_email_on_success = EmailOperator(
        task_id='send_email_on_success',
        to=["ayush.kumar@transformco.com"],
        cc=["ayush.kumar@transformco.com"],
        subject=subject,
        html_content="<br/><hr/><hr/></b> <br><b>DAG Name :</b> {0}<br><b>Execution Date :</b> {1} <br><b>DAG Run Status :</b> <font color=green>SUCCESS</font><br><br><hr><hr>".format(dag_id, execution_date),

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
    catchup=False,
    tags=["Folder:HS-ANAPLAN", "Application:HS-PARTS", "SubApplication:HS-SCF"],
    default_args=default_args,
    on_success_callback=send_email_on_success
)
def docs_example_dag():

    @task
    def tell_me_what_to_do():
        response = requests.get("https://bored-api.appbrewery.com/random")
        return response.json()["activity"]

    tell_me_what_to_do()

docs_example_dag()