from airflow.decorators import task, dag
from pendulum import datetime
import requests
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'docs/00AKOSB3-FLSBH_3.md')
path = filename

@dag(
    start_date=datetime(2022,11,1),
    schedule="@daily",
    catchup=False,
    doc_md=path
)
def docs_example_dag():

    @task
    def tell_me_what_to_do():
        response = requests.get("https://bored-api.appbrewery.com/random")
        print(dirname, filename, path, type(path))
        return response.json()["activity"]

    tell_me_what_to_do()

docs_example_dag()