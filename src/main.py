from src.backend.metadata_handler import MetadataHandler
from src.llm_engine.model_pipeline import AssistantPipeline
from src.backend.api_requests import APIRequests


if __name__ == "__main__":
    print("Hallo")

    pipeline = AssistantPipeline()

    pipeline.run("hello")


