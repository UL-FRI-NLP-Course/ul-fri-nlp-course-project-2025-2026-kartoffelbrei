import os
import dateparser

from pathlib import Path
from backend.metadata_handler import MetadataHandler
from llm_engine.model_pipeline import AssistantPipeline
from backend.api_requests import APIRequests
from backend.format_response import ResponseFormatter
from backend.route_params import RouteParams
from backend.time_converter import TimeConverter

if __name__ == "__main__":
    requests = APIRequests()

    # show correct times
    departure_time, departure_date = TimeConverter.convert_time("today at 8am")
    route_params: RouteParams = {'departure_date': departure_date.isoformat()}
    result = requests.get_journey_information(departure_station="HKI", destination_station="TPE", params=route_params)
    print(ResponseFormatter.format_journey_response(train_data=result, departure_station="HKI", destination_station="TPE", current_time=departure_time))

    #BASE_DIR = Path(__file__).resolve().parent
    #print(BASE_DIR)

    #query_path = os.path.join(BASE_DIR, "llm_queries", "queries.txt")
    #pipeline = AssistantPipeline()
    #with open(query_path, "r") as file:
    #    for query in file:
    #        pipeline.run(query.strip())
        

