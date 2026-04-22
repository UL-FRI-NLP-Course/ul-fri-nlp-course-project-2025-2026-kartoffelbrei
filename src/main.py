from src.backend.metadata_handler import MetadataHandler
from src.llm_engine.model_pipeline import AssistantPipeline

from huggingface_hub import snapshot_download

if __name__ == "__main__":
    print("Hallo")

    #snapshot_download(
    #    repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    #)

    pipeline = AssistantPipeline()
    pipeline.run()
