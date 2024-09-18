from airflow.decorators import dag, task
from airflow.models.baseoperator import chain
from airflow.exceptions import AirflowException
from airflow.providers.apprise.notifications.apprise import send_apprise_notification
from apprise import NotifyType
@dag(schedule=None, catchup=False, on_failure_callback=send_apprise_notification(
    title='Airflow Task Failed',
    body='Task Failed',
    notify_type=NotifyType.FAILURE,
    apprise_conn_id='notifier',
    tag='alerts'
))
def dag_apprise():

    @task
    def a():
        print("good")

    @task
    def b():
        print("bad")
        raise AirflowException()


    chain(a(), b())

dag_apprise()


#{"path": "https://searshc.webhook.office.com/webhookb2/34f6d740-a240-4d8e-a030-1b8c5a1ccc03@27e4c168-0323-4463-acad-7e124b566726/IncomingWebhook/3fa80d8d58814d22ad996f9a017737b6/727d96fa-3dd1-4da0-ad93-9b4f153c66fd", "tag": "alerts"}
