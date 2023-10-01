import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator

from dags.include.datasets.datasets import SIMPLE_DATASET


def _trigger():
    return 42


with DAG(
    dag_id="simple_producer",
    start_date=pendulum.datetime(2023, 10, 15),
    schedule="@hourly",
):
    first_task = PythonOperator(
        task_id="first_task", python_callable=_trigger, outlets=[SIMPLE_DATASET]
    )
