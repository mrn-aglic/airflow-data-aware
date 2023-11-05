from typing import Optional

TIMETABLE_MAPPINGS = {
    "@once": None,
    "@continuous": None,
    "@hourly": "0 * * * *",
    "@daily": "0 0 * * *",
    "@weekly": "0 0 * * 0",
    "@monthly": "0 0 1 * *",
    "@quarterly": "0 0 1 */3 *",
    "@yearly": "0 0 1 1 *",
}


def maybe_from_timetable_mapping(value: str) -> Optional[str]:
    return TIMETABLE_MAPPINGS.get(value)
