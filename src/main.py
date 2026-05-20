import os

from pathlib import Path

from llm_engine.model_pipeline import AssistantPipeline
from llm_queries.queries import dataset
from llm_engine.intent_extractor import IntentExtractor
from analysis.intent_data import IntentData

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent
    print(BASE_DIR)

    query_path = os.path.join(BASE_DIR, "llm_queries", "queries.txt")
    pipeline = AssistantPipeline()
    pred_intents = []
    for query in dataset:
        intent = pipeline.run(query.get('text'))
        pred_intents.append(IntentExtractor.get_intent(intent))


    intent_data = IntentData(y_pred=pred_intents, dataset=dataset)
    intent_data.compute_intent_accuracy()
    intent_data.compute_confusion_matrix()