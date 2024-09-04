# Airflow data-aware scheduling

The examples here are used to demonstrate the data-aware
scheduling feature of Airflow.
The examples are described in the following Medium stories:
1. [Problem with using data intervals when backfilling dataset scheduled DAGs](https://medium.com/@MarinAgli1/problem-with-using-data-intervals-when-backfilling-data-aware-dags-795594414aa2)
2. [Circumventing the problem of using data intervals when backfilling dataset scheduled DAGs](https://medium.com/@MarinAgli1/circumventing-the-problem-of-using-data-intervals-when-backfilling-dataset-scheduled-dags-b9f75d655d32)

# Running the examples
The examples can be run with
```shell
make run
```
or
```shell
docker-compose up
```

# References
1. [Airflow data-aware scheduling docs](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/datasets.html)
2. [Medium story about Airflow data-aware scheduling with dynamic task mapping](https://medium.com/@MarinAgli1/a-look-into-airflow-data-aware-scheduling-and-dynamic-task-mapping-8c548d4ad79)
