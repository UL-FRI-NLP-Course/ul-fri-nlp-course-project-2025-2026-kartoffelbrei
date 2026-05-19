import dateparser

from typing import Tuple, Any

class TimeConverter:

    @staticmethod
    def convert_time(time: str) -> Tuple[Any, Any]:
        settings = {
            "TIMEZONE": "Europe/Helsinki",
            "RETURN_AS_TIMEZONE_AWARE": True
        }

        dt = dateparser.parse(time, settings=settings)
        departure_time = dt.time()
        departure_date = dt.date()
        return departure_time, departure_date