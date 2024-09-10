from datetime import datetime, timedelta
from airflow.decorators import dag, task

import time

default_args = {
    'owner': 'hsbatch',
    'wait_for_downstream': True,
    'depends_on_past': True,
    'email_on_failure': True,
    'email_on_success': True,
    'priority_weight': 5,
}

@dag(
    start_date=datetime(2024,9,9),
    default_args=default_args,
    tags=["Folder:HS", "Application:ARCH", "SubApplication:INFRA"],
    catchup=False
)
def dag_cron():

    @task
    def task_a():
        print("Task A")
        time.sleep(150)
        return 1

    @task
    def task_b():
        print("Task B")
        time.sleep(150)
        return 1

    task_a() >> task_b()

dag_cron()