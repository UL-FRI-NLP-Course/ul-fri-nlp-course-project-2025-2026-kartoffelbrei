import os

from typing import Any

from backend.website_handler import RAG_Handler
from llm_engine.model_manager import ModelManager
from llm_engine.router_i import Router
from llm_engine.intent_router import IntentRouter
from llm_engine.answer_router import AnswerRouter
from backend.api_requests import APIRequests
from llm_engine.api_request_builder import APIRequestBuilder
from llm_engine.intents import Intent
from llm_engine.intent_extractor import IntentExtractor
from util.file_creation import FileCreation


FAISS_PATH= "/d/hpc/projects/onj_fri/kartoffelbrei/faiss/"

class AssistantPipeline:
    def __init__(self, file_creation: FileCreation):
        self.model_manager = ModelManager()
        self.model_manager.load_all()
        self.api_requests = APIRequests()
        self.api_request_builder = APIRequestBuilder(self.api_requests)
        self.faiss_store = None
        self.rag_handler = RAG_Handler()
        self.file_creation = file_creation
        if not os.path.exists(FAISS_PATH):
            print("Create FAISS index.")
            texts = self.rag_handler.create_database()
            chunks = self.rag_handler.text_preparation(texts)
            self.faiss_store = self.rag_handler.vectorize_and_store(chunks, self.model_manager.embedding_model)
            self.rag_handler.save_faiss_local(self.faiss_store,FAISS_PATH)
        else:
           self.faiss_store = self.rag_handler.load_faiss_local(self.model_manager.embedding_model, FAISS_PATH)

        self.intent_router: Router = IntentRouter(self.model_manager)
        self.answer_router: Router = AnswerRouter(self.model_manager)
        print("\n")

    def run(self, input: str) -> Any:
        self.file_creation.write_pipeline_log("==================")
        self.file_creation.write_pipeline_log(f"Query: {input}")
        # get JSON with keywords
        intents = self.intent_router.extract_answer(user_input=input)
        # decide which RAG method is necessary
        if (
                IntentExtractor.get_intent(intents) != Intent.OTHER.value
                and IntentExtractor.get_intent(intents) != Intent.GENERAL_INFO.value
        ):
            decision = "Ask API for live data and got the following result"
            result = self.api_request_builder.send_api_request(intents)
        elif IntentExtractor.get_intent(intents) != Intent.OTHER.value:
            decision = "Use RAG to answer question with static websites and got the following result"
            result = self.rag_handler.search_similiar(self.faiss_store, input, 5)
        else:
            decision = "Use neither API nor RAG to answer the question"
            result = ""
        self.file_creation.write_pipeline_log(f"{decision}: {result}")
        response = self.answer_router.extract_answer(user_input=input, result=result)

        
        self.file_creation.write_pipeline_log(f"Answer of the model: {response}")
        self.file_creation.write_pipeline_log("==================\n")

        return intents
