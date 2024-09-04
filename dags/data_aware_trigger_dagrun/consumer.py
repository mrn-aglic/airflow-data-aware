import pendulum
from airflow import DAG
from airflow.models.dataset import DatasetEvent
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from dags.include.datasets.datasets import ENRICHED_DATASET_TRIGGER


def _resolve_event(event: DatasetEvent) -> dict:
    return {
        "ds_interval_start": pendulum.DateTime.fromisoformat(
            event.extra["data_interval_start"]
        ),
        "ds_interval_end": pendulum.DateTime.fromisoformat(
            event.extra["data_interval_end"]
        ),
    }


def _resolve_dataset_events(triggering_dataset_events, **context) -> list[dict]:

    return [_resolve_event(event) for event in triggering_dataset_events[ENRICHED_DATASET_TRIGGER.uri]]


def _print(ds_interval_start, ds_interval_end, **context):
    print(f"data_interval_start: {ds_interval_start}")
    print(f"data_interval_end: {ds_interval_end}")


with DAG(
    dag_id="simple_consumer_metadata_trigger",
    start_date=pendulum.datetime(2023, 10, 15),
    schedule=[ENRICHED_DATASET_TRIGGER],
):
    dummy = EmptyOperator(
        task_id="dummy",
    )

    resolve_dataset_events = PythonOperator(
        task_id="resolve_dataset_events",
        python_callable=_resolve_dataset_events,
        inlets=[ENRICHED_DATASET_TRIGGER],
    )

    print_data = PythonOperator.partial(
        task_id="print_data",
        python_callable=_print,
        map_index_template="""resolved_with_start_{{ task.op_kwargs['ds_interval_start'] | ds }}""",
    ).expand(op_kwargs=resolve_dataset_events.output)

    def _extract_logical_date(event_extra):
        return event_extra["ds_interval_start"]

    trigger_runs = TriggerDagRunOperator.partial(
        task_id="trigger_runs",
        trigger_dag_id="printer",
        # reset_dag_run=True,
    ).expand(logical_date=resolve_dataset_events.output.map(_extract_logical_date))

    dummy >> resolve_dataset_events
