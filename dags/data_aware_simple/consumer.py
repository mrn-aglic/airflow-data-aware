import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from dags.include.datasets.datasets import SIMPLE_DATASET


def _print(data_interval_start, data_interval_end):
    print(f"data_interval_start: {data_interval_start}")
    print(f"data_interval_end: {data_interval_end}")


with DAG(
    dag_id="simple_consumer",
    start_date=pendulum.datetime(2023, 10, 15),
    schedule=[SIMPLE_DATASET],
):
    dummy = EmptyOperator(
        task_id="dummy",
    )

    print_data = PythonOperator(task_id="print_data", python_callable=_print)

    dummy >> print_data
