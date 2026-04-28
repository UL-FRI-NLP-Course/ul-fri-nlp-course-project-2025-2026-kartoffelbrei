from src.backend.metadata_handler import MetadataHandler
from src.llm_engine.model_pipeline import AssistantPipeline
from src.backend.api_requests import APIRequests
from src.backend.format_response import format_train_type_response


if __name__ == "__main__":
    api_requests = APIRequests()
    route_info = api_requests.get_route_information("HKI", "TPE")
    print(format_train_type_response(route_info))

    pipeline = AssistantPipeline()
    pipeline.run("Can I travel from Helsinki asema to Tampere asema today?")


