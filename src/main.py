import os

from src.backend.metadata_handler import MetadataHandler
from src.llm_engine.model_pipeline import AssistantPipeline
from src.backend.api_requests import APIRequests
from src.backend.format_response import format_train_type_response

if __name__ == "__main__":
    pipeline = AssistantPipeline()

    with open(os.path.join("src", "llm_queries", "queries.txt"), "r") as file:
        for query in file:
            pipeline.run(query)
