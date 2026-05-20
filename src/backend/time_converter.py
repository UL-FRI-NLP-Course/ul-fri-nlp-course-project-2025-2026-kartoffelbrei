import dateparser

from typing import Tuple, Any
from datetime import datetime, timezone, time, date

class TimeConverter:

    @staticmethod
    def convert_time(time: str) -> Tuple[Any, Any]:
        if time == None:
            return None, None

        settings = {
            "TIMEZONE": "Europe/Helsinki",
            "RETURN_AS_TIMEZONE_AWARE": True
        }

        dt = dateparser.parse(time, settings=settings)
        departure_time = dt.time()
        departure_date = dt.date()
        return departure_time, departure_date

    @staticmethod
    def get_current_time() -> time:
        now = datetime.now(timezone.utc).time()
        return now

    @staticmethod
    def get_current_date() -> date:
        today_utc = datetime.now(timezone.utc).date()
        return today_utc