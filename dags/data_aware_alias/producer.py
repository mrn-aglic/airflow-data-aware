import pendulum
from airflow import DAG
from airflow.datasets.metadata import Metadata
from airflow.operators.python import PythonOperator
from pendulum import DateTime

from dags.include.datasets.datasets import ALIAS_DATASET


def _trigger(data_interval_start: DateTime, data_interval_end: DateTime):
    yield Metadata(
        ALIAS_DATASET,
        extra={
            "data_interval_start": data_interval_start,
            "data_interval_end": data_interval_end,
        },
    )

    return 42


with DAG(
    dag_id="simple_producer_alias",
    start_date=pendulum.datetime(2023, 10, 15),
    end_date=pendulum.datetime(2023, 10, 20),
    schedule="@hourly",
):
    first_task = PythonOperator(
        task_id="first_task",
        python_callable=_trigger,
        outlets=[ALIAS_DATASET],
    )
