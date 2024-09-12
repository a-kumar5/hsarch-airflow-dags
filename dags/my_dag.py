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


apprise -t "Test Title" -b "Test Message" "https://prod-95.westus.logic.azure.com:443/workflows/9c5adffea70d4120adb1222907b4944d/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=nHfcx6_6Xde5scH29DGwj7tC_nzPf6PzyKbhCPWOGmg"

https://prod-site.logic.azure.com:443/workflows/{workflow}/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig={signature}
workflows://prod-95.westus.logic.azure.com:443/9c5adffea70d4120adb1222907b4944d/nHfcx6_6Xde5scH29DGwj7tC_nzPf6PzyKbhCPWOGmg

apprise -vv -t "Test Message Title" -b "Test Message Body" workflows://prod-95.westus.logic.azure.com:443/9c5adffea70d4120adb1222907b4944d/nHfcx6_6Xde5scH29DGwj7tC_nzPf6PzyKbhCPWOGmg/
