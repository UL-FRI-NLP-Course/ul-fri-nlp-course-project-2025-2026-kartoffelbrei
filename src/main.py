from src.backend.metadata_handler import MetadataHandler
from src.llm_engine.model_pipeline import AssistantPipeline
from src.backend.api_requests import APIRequests


if __name__ == "__main__":
    pipeline = AssistantPipeline()
    pipeline.run("Can I travel from Helsinki to Tampere today?")


