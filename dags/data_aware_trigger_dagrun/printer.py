import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator

def _print(data_interval_start, data_interval_end):
    print(f"data_interval_start: {data_interval_start}")
    print(f"data_interval_end: {data_interval_end}")

with DAG(
    dag_id="printer",
    start_date=pendulum.datetime(2024, 8, 1),
    end_date=pendulum.datetime(2024, 8, 31),
    schedule=None,
    # catchup=False, # use if you assign a schedule
):
    print_data = PythonOperator(task_id="print_data", python_callable=_print)
