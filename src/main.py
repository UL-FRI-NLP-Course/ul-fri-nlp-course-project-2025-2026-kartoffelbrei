import os
from pathlib import Path
from backend.metadata_handler import MetadataHandler
from llm_engine.model_pipeline import AssistantPipeline
from backend.api_requests import APIRequests
from backend.format_response import ResponseFormatter

if __name__ == "__main__":
    # requests = APIRequests()
    # result = requests.get_route_information(departure_station="HKI", destination_station="TPE")
    # print(format_route_response(train_data=result, departure_station="HKI", destination_station="TPE"))
    BASE_DIR = Path(__file__).resolve().parent
    print(BASE_DIR)

    query_path = BASE_DIR / "llm_queries" / "queries.txt"
    pipeline = AssistantPipeline()
    with open(query_path, "r") as file:
        for query in file:
            pipeline.run(query.strip())
