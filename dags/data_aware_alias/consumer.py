import pendulum
from airflow import DAG
from airflow.models.dataset import DatasetEvent
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from dags.include.datasets.datasets import ENRICHED_DATASET


def _resolve_event(event: DatasetEvent) -> dict:
    return {
        "ds_interval_start": pendulum.DateTime.fromisoformat(
            event.extra["data_interval_start"]
        ),
        "ds_interval_end": pendulum.DateTime.fromisoformat(
            event.extra["data_interval_end"]
        ),
    }


def _resolve_dataset_events(inlet_events: list[DatasetEvent], **context) -> list[dict]:

    return [_resolve_event(event) for event in inlet_events[ENRICHED_DATASET]]


def _print(ds_interval_start, ds_interval_end, **context):
    print(f"data_interval_start: {ds_interval_start}")
    print(f"data_interval_end: {ds_interval_end}")


with DAG(
    dag_id="simple_consumer_metadata",
    start_date=pendulum.datetime(2023, 10, 15),
    schedule=[ENRICHED_DATASET],
):
    dummy = EmptyOperator(
        task_id="dummy",
    )

    resolve_dataset_events = PythonOperator(
        task_id="resolve_dataset_events",
        python_callable=_resolve_dataset_events,
        inlets=[ENRICHED_DATASET],
    )

    print_data = PythonOperator.partial(
        task_id="print_data",
        python_callable=_print,
        map_index_template="""resolved_with_start_{{ task.op_kwargs['ds_interval_start'] | ds }}""",
    ).expand(op_kwargs=resolve_dataset_events.output)

    dummy >> resolve_dataset_events
