import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from dags.include.datasets.datasets import SIMPLE_DATASET


def _print(data_interval_end, data_interval_start):
    print(data_interval_end)
    print(data_interval_start)


with DAG(
    dag_id="simple_consumer",
    start_date=pendulum.datetime(2023, 9, 3),
    schedule=[SIMPLE_DATASET],
):
    dummy = EmptyOperator(
        task_id="dummy",
    )

    print_data = PythonOperator(task_id="print_data", python_callable=_print)

    dummy >> print_data
