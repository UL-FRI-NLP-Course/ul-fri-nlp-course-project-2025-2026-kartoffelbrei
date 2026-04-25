from backend.metadata_handler import MetadataHandler
from llm_engine.model_pipeline import AssistantPipeline
from backend.api_requests import APIRequests


if __name__ == "__main__":
    print("Hallo")

    pipeline = AssistantPipeline()

    pipeline.run("hello")


