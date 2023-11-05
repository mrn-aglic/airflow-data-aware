import polars as pl
from airflow_api import AirflowApiClient
from cron_managment import construct_intervals
from login import get_session

url = "http://localhost:8080"
username = "airflow"
password = "airflow"


with AirflowApiClient(url, username, password, get_session) as airflow_client:
    ################ List DAGs
    dags = airflow_client.list_dags()
    print(dags)

    ################ Get DAG details
    def get_dag_details(dag_id: str):
        date_schema = {
            "dag_id": str,
            "schedule_interval": pl.Struct(
                [pl.Field("__type", str), pl.Field("value", str)]
            ),
            "start_date": str,
            "end_date": str,
        }

        dag_details = airflow_client.get_dag_details(dag_id=dag_id, schema=date_schema)
        print(dag_details)

        dag_details = dag_details.unnest("schedule_interval").rename(
            {"__type": "schedule_type", "value": "schedule_interval"}
        )

        return dag_details

    producer_details = get_dag_details(dag_id="simple_producer")
    print(producer_details)

    ################ Get DAG runs
    def get_dagruns(dag_id: str):
        dag_runs_schema = {
            "dag_run_id": str,
            "dag_id": str,
            "logical_date": str,
            "start_date": str,
            "end_date": str,
            "data_interval_start": str,
            "data_interval_end": str,
            "last_scheduling_decision": str,  # When a scheduler last attempted to schedule TIs for this DagRun
            "run_type": str,
            "state": str,
        }

        return airflow_client.get_all_dag_runs(dag_id=dag_id, schema=dag_runs_schema)

    dag_runs = get_dagruns(dag_id="simple_consumer")


dag_runs_basic = dag_runs.filter(pl.col("run_type") != "manual").select(
    pl.col("dag_run_id"),
    pl.col("start_date"),
    pl.col("last_scheduling_decision"),
    pl.col("data_interval_start"),
    pl.col("data_interval_end"),
    pl.col("run_type"),
)

print("\n\n#############DAG RUNS BASIC DATA")
print(dag_runs_basic)


first_last_dag_runs = dag_runs_basic.select(
    pl.min("data_interval_start").alias("min"), pl.max("data_interval_end").alias("max")
)


start_date, end_date = first_last_dag_runs.rows()[
    0
]  # the first data_interval_start and last data_interval_end of all dag runs

print(f"start_date: {start_date}")
print(f"end_date: {end_date}")

cron = producer_details.select("schedule_interval").item()

intervals = construct_intervals(cron, start_date=start_date, end_date=end_date)


anti_joined = dag_runs_basic.join(
    intervals, on=["data_interval_start", "data_interval_end"], how="anti"
)

print(anti_joined)
