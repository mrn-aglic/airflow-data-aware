import math
import typing

import polars as pl
from login import AirflowLogin


class AirflowApiClient(AirflowLogin):
    _headers = {"Accept": "application/json"}

    def __init__(
        self, url: str, username: str, password: str, get_session: typing.Callable
    ) -> None:
        super().__init__(url, username, password, get_session)

        self._api = f"{self._url}/api/v1"

    def list_dags(self) -> pl.DataFrame:
        endpoint = f"{self._api}/dags"

        r = self._session.get(url=endpoint, headers=AirflowApiClient._headers)
        data = r.json()

        return pl.from_records(data["dags"])

    def get_dag_details(
        self, dag_id: str, schema: typing.Optional[dict] = None
    ) -> pl.DataFrame:
        endpoint = f"{self._api}/dags/{dag_id}/details"

        details = self._session.get(
            url=endpoint, headers=AirflowApiClient._headers
        ).json()

        return pl.from_dicts([details], schema=schema)

    def get_num_dag_runs(self, dag_id: str) -> int:
        return self.get_dag_runs(dag_id=dag_id)["total_entries"]

    def get_dag_runs(self, dag_id: str, offset: int = 0, limit: int = 100) -> dict:
        dag_runs_api_endpoint = f"{self._api}/dags/{dag_id}/dagRuns"

        return self._session.get(
            url=dag_runs_api_endpoint,
            headers=AirflowApiClient._headers,
            params={"offset": offset, "limit": limit},
        ).json()

    def get_all_dag_runs(self, dag_id: str, schema=None) -> pl.DataFrame:
        total_entries = self.get_num_dag_runs(dag_id=dag_id)

        batch_size = 100
        num_batches = math.ceil(total_entries / batch_size)

        result = pl.DataFrame()

        for num in range(num_batches):
            dag_runs = self.get_dag_runs(
                dag_id=dag_id, offset=(batch_size * num), limit=batch_size
            )
            dag_runs = dag_runs["dag_runs"]

            response = pl.from_dicts(dag_runs, schema=schema)
            result = pl.concat([result, response])

        return result
