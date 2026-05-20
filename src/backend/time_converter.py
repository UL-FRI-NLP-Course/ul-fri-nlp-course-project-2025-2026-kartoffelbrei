import dateparser

from typing import Tuple, Any, Union
from datetime import datetime, timezone, time, date
from zoneinfo import ZoneInfo

class TimeConverter:

    @staticmethod
    def convert_time(time: Any) -> Tuple[Union[time, None], Union[date, None]]:
        if time is None:
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
    def convert_datetime_to_string(dt: datetime) -> str:
        helsinki_dt = dt.astimezone(ZoneInfo("Europe/Helsinki"))
        date_str = helsinki_dt.strftime("%Y-%m-%d %H:%M:%S %Z%z")
        return date_str

    @staticmethod
    def convert_time_to_utc(dt: str) -> datetime:
        return datetime.fromisoformat(dt.replace("Z", "+00:00"))

    @staticmethod
    def get_current_time() -> time:
        now = datetime.now(timezone.utc).time()
        return now

    @staticmethod
    def get_current_date() -> date:
        today_utc = datetime.now(timezone.utc).date()
        return today_utc

    @staticmethod
    def get_current_datetime_in_utc() -> datetime:
        date_time = datetime.now(timezone.utc)
        return date_time