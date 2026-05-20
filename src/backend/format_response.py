import json

from typing import List, Any, Tuple, Union
from datetime import datetime, timedelta

from backend.metadata_handler import MetadataHandler
from backend.time_converter import TimeConverter


class ResponseFormatter:

    @staticmethod
    def _build_train_string(train_type: str, train_number: str) -> str:
        return train_type + " " + train_number

    @staticmethod
    def _get_arrival_and_departure_time_journey(timetable, departure_station: str, destination_station: str) -> List[Any]:
        response_list = []
        rows = sorted(timetable, key=lambda x: x['scheduledTime'])

        seen = set()
        for r in rows:
            station = r.get('stationShortCode')
            time = r.get('scheduledTime')

            if not station or station in seen:
                continue

            if str(station) == departure_station:
                response_list.append(time)
            elif str(station) == destination_station:
                response_list.append(time)
                break

        return response_list

    @staticmethod
    def _filter_connections(response_list: List[Any], current_time: Any) -> List[Any]:
        filtered_list = []
        for connection in response_list:
            if connection['departure'].time() >= current_time:
                filtered_list.append(connection)


        sorted_list = sorted(filtered_list, key=lambda x: x['duration'])
        return sorted_list[:5]

    @staticmethod
    def _turn_connections_into_json_string(
            departure_station: str,
            destination_station: str,
            response_list: List[Any]
    ) -> str:
        station_dict = MetadataHandler.load_station_dict()
        data = {
            "departure_station": station_dict.get(departure_station),
            "destination_station": station_dict.get(destination_station),
            "connections_found": True,
            "top_five_connections": []
        }

        if len(response_list) == 0:
            data['connections_found'] = False

        for connection in response_list:
            data['top_five_connections'].append(
                {
                    "train": ResponseFormatter._build_train_string(connection['train_type'], connection['train_number']),
                    "departure": TimeConverter.convert_datetime_to_string(connection['departure']),
                    "arrival": TimeConverter.convert_datetime_to_string(connection['arrival']),
                    "duration_minutes": connection['duration']
                }
            )

        json_string = json.dumps(data, ensure_ascii=False, indent=2)
        return json_string

    @staticmethod
    def format_journey_response(
            train_data,
            departure_station: str,
            destination_station: str,
            current_time: Any
    ) -> str:
        response_list = []

        for train in train_data:
            times = ResponseFormatter._get_arrival_and_departure_time_journey(train['timeTableRows'], departure_station, destination_station)

            departure_time = TimeConverter.convert_time_to_utc(times[0])
            arrival_time = TimeConverter.convert_time_to_utc(times[1])
            difference = arrival_time - departure_time

            response_list.append(
                {
                    "train_type": f"{train['trainType']}",
                    "train_number": f"{train['trainNumber']}",
                    "departure": departure_time,
                    "arrival": arrival_time,
                    "duration": float(difference.total_seconds() / 60)
                }
            )

        response_list = ResponseFormatter._filter_connections(response_list, current_time)

        return ResponseFormatter._turn_connections_into_json_string(
            departure_station,
            destination_station,
            response_list
        )

    @staticmethod
    def _get_arrival_and_departure_time_station(entry, station_shortcode: str) -> Tuple[Union[datetime, None], Union[datetime, None]]:
        arrival_time = None
        departure_time = None
        for row in entry['timeTableRows']:
            if row['type'] == "ARRIVAL" and row['stationShortCode'] == station_shortcode:
                arrival_time = TimeConverter.convert_time_to_utc(row['scheduledTime'])
            elif row['type'] == "DEPARTURE" and row['stationShortCode'] == station_shortcode:
                departure_time = TimeConverter.convert_time_to_utc(row['scheduledTime'])

        return arrival_time, departure_time

    @staticmethod
    def _turn_station_timetable_into_json_string(response_list: List[Any], station_shortcode: str) -> str:
        station_dict = MetadataHandler.load_station_dict()
        station = station_dict.get(station_shortcode)

        data = {
            "station": station,
            "timetable_found": True,
            "timetable": []
        }

        if len(response_list) == 0:
            data['timetable_found'] = False

        for train in response_list:
            arrival_time = "" if train['scheduled_arrival'] is None \
                else TimeConverter.convert_datetime_to_string(train['scheduled_arrival'])
            departure_time = "" if train['scheduled_departure'] is None \
                else TimeConverter.convert_datetime_to_string(train['scheduled_departure'])

            if arrival_time == "":
                station_role = "origin"
            elif departure_time == "":
                station_role = "destination"
            else:
                station_role = "intermediate"

            data['timetable'].append(
                {
                    "train": ResponseFormatter._build_train_string(train['train_type'], train['train_number']),
                    "station_role": station_role,
                    "scheduled_arrival": arrival_time,
                    "scheduled_departure": departure_time,
                }
            )

        json_string = json.dumps(data, ensure_ascii=False, indent=2)
        return json_string

    @staticmethod
    def format_station_timetable_response(station_data, departure_station: str):
        response_list = []
        for entry in station_data:
            arrival_time, departure_time = ResponseFormatter._get_arrival_and_departure_time_station(entry, departure_station)
            response_list.append(
                {
                    "train_type": f"{entry['trainType']}",
                    "train_number": f"{entry['trainNumber']}",
                    "scheduled_arrival": arrival_time,
                    "scheduled_departure": departure_time
                }
            )

        return ResponseFormatter._turn_station_timetable_into_json_string(response_list, departure_station)

    @staticmethod
    def _get_current_next_final_stop(time_table_rows):
        current_location = None
        next_stop = None
        delay = 0

        commercial_rows = [
            row for row in time_table_rows
            if row.get('commercialStop')
               and row.get('type') == "ARRIVAL"
        ]

        if not commercial_rows:
            return None, None, None

        destination = commercial_rows[-1]

        now = TimeConverter.get_current_datetime_in_utc()
        for row in commercial_rows:

            timestamp = (
                    row.get('liveEstimateTime')
                    or row.get('scheduledTime')
            )

            row_time = TimeConverter.convert_time_to_utc(timestamp)

            if row_time <= now:
                current_location = row

            elif row_time > now and next_stop is None:
                next_stop = row
                break

        station_dict = MetadataHandler.load_station_dict()

        if current_location is not None:
            delay = current_location['differenceInMinutes']
            dt = TimeConverter.convert_time_to_utc(current_location['actualTime'])
            current_location = {
                "station": station_dict.get(current_location['stationShortCode']),
                "event": current_location['type'],
                "time": TimeConverter.convert_datetime_to_string(dt),
                "delay_minutes": delay
            }

        if next_stop is not None:
            scheduled = TimeConverter.convert_time_to_utc(next_stop['scheduledTime'])
            estimated = scheduled + timedelta(minutes=delay)
            next_stop = {
                "station": station_dict[next_stop['stationShortCode']],
                "scheduled_arrival": TimeConverter.convert_datetime_to_string(scheduled),
                "estimated_arrival": TimeConverter.convert_datetime_to_string(estimated),
            }

        if destination is not None:
            scheduled = TimeConverter.convert_time_to_utc(destination['scheduledTime'])
            estimated = scheduled + timedelta(minutes=delay)
            destination = {
                "station": station_dict[destination['stationShortCode']],
                "scheduled_arrival": TimeConverter.convert_datetime_to_string(scheduled),
                "estimated_arrival": TimeConverter.convert_datetime_to_string(estimated),
            }

        return current_location, next_stop, destination

    @staticmethod
    def _turn_train_status_into_json_string(train_status) -> str:
        json_string = json.dumps(train_status, ensure_ascii=False, indent=2)
        return json_string

    @staticmethod
    def format_train_status_response(train_data) -> str:
        train_data = train_data[0]
        current_location, next_stop, destination = ResponseFormatter._get_current_next_final_stop(
            train_data['timeTableRows']
        )

        train_status = {
            "train": ResponseFormatter._build_train_string(f"{train_data['trainType']}", f"{train_data['trainNumber']}"),
            "running": train_data['runningCurrently'],
            "cancelled": train_data['cancelled'],
            "current_location": current_location,
            "next_stop": next_stop,
            "destination": destination,
        }

        return ResponseFormatter._turn_train_status_into_json_string(train_status)
