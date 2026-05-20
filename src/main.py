import os

from pathlib import Path

from llm_engine.model_pipeline import AssistantPipeline

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent
    print(BASE_DIR)

    query_path = os.path.join(BASE_DIR, "llm_queries", "queries.txt")
    pipeline = AssistantPipeline()
    with open(query_path, "r") as file:
        for query in file:
            pipeline.run(query.strip())
