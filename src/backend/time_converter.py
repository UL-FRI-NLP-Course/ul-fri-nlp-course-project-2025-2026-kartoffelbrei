import dateparser

from typing import Tuple, Any
from datetime import datetime, timezone, time, date
from zoneinfo import ZoneInfo

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

        if dt is None:
            return None, None

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("Europe/Helsinki"))

        dt_utc = dt.astimezone(ZoneInfo("UTC"))

        departure_time = dt_utc.time()
        departure_date = dt_utc.date()

        return departure_time, departure_date

    @staticmethod
    def get_current_time() -> time:
        now = datetime.now(timezone.utc).time()
        return now

    @staticmethod
    def get_current_date() -> date:
        today_utc = datetime.now(timezone.utc).date()
        return today_utc

    @staticmethod
    def get_current_datetime() -> datetime:
        date_time = datetime.now(timezone.utc)
        return date_time