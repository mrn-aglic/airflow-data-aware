import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from dags.include.datasets.datasets import ALIAS_DATASET


def _print(data_interval_start, data_interval_end, **context):
    print(f"data_interval_start: {data_interval_start}")
    print(f"data_interval_end: {data_interval_end}")

    inlets_events = context["inlets_events"]
    print(f"inlets_events: {inlets_events}")


with DAG(
    dag_id="simple_consumer_alias",
    start_date=pendulum.datetime(2023, 10, 15),
    schedule=[ALIAS_DATASET],
):
    dummy = EmptyOperator(
        task_id="dummy",
    )

    print_data = PythonOperator(
        task_id="print_data",
        python_callable=_print,
        inlets=[ALIAS_DATASET],
    )

    dummy >> print_data
