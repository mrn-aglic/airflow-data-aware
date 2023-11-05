from datetime import datetime, timezone
from typing import List, Optional, Tuple

import polars as pl
from croniter import croniter

DataInterval = Tuple[datetime, datetime]


def construct_intervals(
    cron_expr: str, start_date: str, end_date: Optional[str] = None
) -> List[DataInterval]:
    dt = datetime.fromisoformat(start_date)

    has_end_date = end_date is not None

    if has_end_date:
        end_date = datetime.fromisoformat(end_date)
    else:
        end_date = datetime.now(timezone.utc)

    citer = croniter(cron_expr, dt)

    current_date = dt

    dates = [dt.isoformat()]

    while current_date < end_date:
        val = citer.get_next(datetime)

        dates.append(val.isoformat())

        current_date = val

    # Add another entry if the end_date was provided
    if has_end_date:
        val = citer.get_next(datetime)
        dates.append(val.isoformat())

    intervals = [dates[:-1], dates[1:]]

    start_column = "data_interval_start"
    end_column = "data_interval_end"

    df = pl.from_records(intervals, schema=[start_column, end_column])

    return df
