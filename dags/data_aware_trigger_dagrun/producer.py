import pendulum
from airflow import DAG
from airflow.datasets.metadata import Metadata
from airflow.operators.python import PythonOperator
from pendulum import DateTime

from dags.include.datasets.datasets import ENRICHED_DATASET_TRIGGER


def _trigger(data_interval_start: DateTime, data_interval_end: DateTime):
    yield Metadata(
        ENRICHED_DATASET_TRIGGER,
        extra={
            "data_interval_start": data_interval_start.isoformat(),
            "data_interval_end": data_interval_end.isoformat(),
        },
    )

    return 42


with DAG(
    dag_id="simple_producer_metadata_trigger",
    start_date=pendulum.datetime(2024, 8, 1),
    end_date=pendulum.datetime(2024, 8, 31),
    schedule="@daily",
):
    first_task = PythonOperator(
        task_id="first_task",
        python_callable=_trigger,
        outlets=[ENRICHED_DATASET_TRIGGER],
    )
