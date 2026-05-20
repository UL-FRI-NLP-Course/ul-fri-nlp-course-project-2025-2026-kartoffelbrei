import os

from backend.website_handler import RAG_Handler
from llm_engine.model_manager import ModelManager
from llm_engine.router_i import Router
from llm_engine.intent_router import IntentRouter
from llm_engine.answer_router import AnswerRouter
from backend.api_requests import APIRequests
from llm_engine.api_request_builder import APIRequestBuilder
from llm_engine.intents import Intent


FAISS_PATH= "/d/hpc/projects/onj_fri/kartoffelbrei/faiss/"

class AssistantPipeline:
    def __init__(self):
        self.model_manager = ModelManager()
        self.model_manager.load_all()
        self.api_requests = APIRequests()
        self.api_request_builder = APIRequestBuilder(self.api_requests)
        self.faiss_store = None
        self.rag_handler = RAG_Handler()
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

    def run(self, input: str):
        print("==================")
        print(f"Query: {input}")
        # get JSON with keywords
        intents = self.intent_router.extract_answer(user_input=input)
        # decide which RAG method is necessary
        decision = ""
        if intents.get("intent") != Intent.OTHER.value and intents.get("intent") != Intent.GENERAL_INFO.value:
            decision = "Ask API for live data and got the following result"
            result = self.api_request_builder.send_api_request(intents)
        elif intents.get("intent") != Intent.OTHER.value:
            decision = "Use RAG to answer question with static websites and got the following result"
            result = self.rag_handler.search_similiar(self.faiss_store, input, 5)
        else:
            result = ""
        print(f"{decision}: {result}")
        response = self.answer_router.extract_answer(user_input=input, result=result)

        
        print(f"Answer: {response}")
        print("==================\n")
