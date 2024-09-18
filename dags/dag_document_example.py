from datetime import datetime

import requests
import os
from airflow.decorators import dag, task

doc = """
## HELLO THIS IS DAG DOC EXAMPLE
"""

dirname = os.path.dirname(__file__)
doc_path = os.path.join(dirname, 'docs/dag_doc_sample.md')

@dag(
    start_date=datetime(2023,1,1),
    schedule='@daily',
    catchup=False,
    doc_md=doc_path
)
def dag_doc_example_ui():

    @task
    def tel_me_what_to_do():
        response = requests.get("https://bored-api.appbrewery.com/random")
        return response.json()

    tel_me_what_to_do()

dag_doc_example_ui()
