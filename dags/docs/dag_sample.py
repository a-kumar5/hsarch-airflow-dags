from __future__ import annotations
from airflow import DAG
import datetime
from airflow.operators.bash import BashOperator
from airflow.operators.email import EmailOperator
from airflow.operators.python import PythonOperator
import warnings
from typing import Any, Dict, List, NamedTuple, Optional, Sized
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.exceptions import AirflowException
from airflow.utils.weight_rule import WeightRule
from airflow.utils.dates import days_ago
from airflow.timetables.events import EventsTimetable
import pendulum
import pytz
import sys
from airflow.models import Variable
util_path = Variable.get("util_functions_path")
sys.path.insert(1,util_path)
from dependencies_handling.dependencies_handling import pre_execution, post_execution, check_predecessor_dag_status,check_successor_status_and_trigger
from on_failure_actions.dag_failure_actions import select_failure_action
from conf.properties.PROD_searshs_helix_airflow_properties import \
    APP_HS_PARTS__FOLDER_HS_ANAPLAN__SUBAPP_HS_SCF__DAG_FIRST_EXEC_START_YEAR, \
    APP_HS_PARTS__FOLDER_HS_ANAPLAN__SUBAPP_HS_SCF__DAG_FIRST_EXEC_START_MONTH, \
    APP_HS_PARTS__FOLDER_HS_ANAPLAN__SUBAPP_HS_SCF__DAG_FIRST_EXEC_START_DAY

def send_email_on_failure(context):
    dag_id = context['task_instance'].dag_id
    task_id = context['task_instance'].task_id
    run_id = context['task_instance'].run_id
    execution_date = context['logical_date']
    subject = "FAILURE: Airflow PROD: Run No: {0} - Dag ID: {1}".format(run_id, dag_id),
    select_failure_action(dag_id, run_id, 'HS-ANAPLAN', 'HS-PARTS', 'HS-SCF', 'BMC Helix Control-M','post_execution_task_SSH_AIM-INV-ConvertSupplierInventory_AWS_160',execution_date)

    send_email_on_failure = EmailOperator(
        task_id='send_email_on_failure',
        to=["SHI_HS_PSOM_HIGH@transformco.com"],
        cc=["SHI_HS_AIRFLOW@transformco.com","airflow-notifications@transformco.com"],
        subject=subject,
        html_content="<br/><hr/><hr/></b> <br><b>DAG Name :</b> {0}<br><b>Execution Date :</b> {1} <br><b>DAG Run Status :</b> <font color=red>FAILURE</font><br><br><hr><hr>".format(dag_id, execution_date),

        dag=context['dag'])

    send_email_on_failure.execute(context)

def send_email_on_success(context):
    dag_id = context['task_instance'].dag_id
    run_id = context['task_instance'].run_id
    task_id = context['task_instance'].task_id
    execution_date = context['logical_date']
    subject = "SUCCESS: Airflow PROD: Run No: {0} - Dag ID: {1}".format(run_id, dag_id),

    send_email_on_success = EmailOperator(
        task_id='send_email_on_success',
        to=["SHI_HS_PSOM_HIGH@transformco.com"],
        cc=["SHI_HS_AIRFLOW@transformco.com"],
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
    'job_doc': "\\kih.kmart.com\DataStore\corp\it\CTM_JobDoc_Prod\AIM-INV-ConvertSupplierInventory_AWS.txt"
}

dag = DAG(
    dag_id='dag_Non-Cyclic_Mon-Sat_AIM-INV-ConvertSupplierInventory_AWS_160',
    schedule="5 8 * * 1-6",
    default_args=default_args,
    tags=["Folder:HS-ANAPLAN", "Application:HS-PARTS", "SubApplication:HS-SCF"],
    start_date=datetime.datetime(APP_HS_PARTS__FOLDER_HS_ANAPLAN__SUBAPP_HS_SCF__DAG_FIRST_EXEC_START_YEAR,
                                 APP_HS_PARTS__FOLDER_HS_ANAPLAN__SUBAPP_HS_SCF__DAG_FIRST_EXEC_START_MONTH,
                                 APP_HS_PARTS__FOLDER_HS_ANAPLAN__SUBAPP_HS_SCF__DAG_FIRST_EXEC_START_DAY,
                                 tzinfo=pytz.timezone('US/Eastern')),
    catchup=False,
    max_active_runs=1,
    on_failure_callback=send_email_on_failure,
    on_success_callback=send_email_on_success
)

pre_execution_task = PythonOperator(
    task_id='Pre_execution_task_SSH_AIM-INV-ConvertSupplierInventory_AWS_160',
    python_callable=pre_execution,
    op_args=['AIM-INV-ConvertSupplierInventory_AWS','HS-ANAPLAN','HS-PARTS','HS-SCF','BMC Helix Control-M'],
    dag=dag
)

ssh_cmd_task = SSHOperator(
    task_id='task_SSH_Non-Cyclic_Mon-Sat_Command_HS-ANAPLAN_HS-SCF_AIM-INV-ConvertSupplierInventory_AWS',
    ssh_conn_id='conn-SSH-hspscbat1pr-hsbatch',
    command="sh /appl/anaplan/prod/others/bin/supplier-inventory_conversion.sh ",
    cmd_timeout=None,
    dag=dag
)

predecessor_status_check_task = PythonOperator(
    task_id='predecessor_status_check_task_SSH_AIM-INV-ConvertSupplierInventory_AWS_160',
    python_callable=check_predecessor_dag_status,
    op_args=['dag_Non-Cyclic_Mon-Sat_AIM-INV-ConvertSupplierInventory_AWS_160','AIM-INV-ConvertSupplierInventory_AWS','HS-ANAPLAN','HS-PARTS','HS-SCF','BMC Helix Control-M'],
    dag=dag
)

post_execution_task = PythonOperator(
    task_id='post_execution_task_SSH_AIM-INV-ConvertSupplierInventory_AWS_160',
    python_callable=post_execution,
    op_args=['dag_Non-Cyclic_Mon-Sat_AIM-INV-ConvertSupplierInventory_AWS_160', 'AIM-INV-ConvertSupplierInventory_AWS',
             'HS-ANAPLAN', '0 8 * * 1-6', 'post_execution_task_SSH_AIM-INV-ConvertSupplierInventory_AWS_160','hsbatch','HS-PARTS','HS-SCF','BMC Helix Control-M'],
    dag=dag
)

post_execution_task_B = PythonOperator(
    task_id='Post_execution_task_B_SSH_AIM-INV-ConvertSupplierInventory_AWS_160',
    python_callable=check_successor_status_and_trigger,
    op_args=['dag_Non-Cyclic_Mon-Sat_AIM-INV-ConvertSupplierInventory_AWS_160','AIM-INV-ConvertSupplierInventory_AWS','HS-ANAPLAN','HS-PARTS','HS-SCF','BMC Helix Control-M'],
    dag=dag
)

pre_execution_task >> predecessor_status_check_task >> ssh_cmd_task >> post_execution_task >> post_execution_task_B