import torch
from src.backend.website_handler import RAG_Handler
from src.llm_engine.model_manager import ModelManager
from src.llm_engine.intent_router import IntentRouter
from src.backend.api_requests import APIRequests
from src.llm_engine.api_request_builder import APIRequestBuilder
from src.llm_engine.intents import Intent
import os

FAISS_PATH= "/d/hpc/projects/onj_fri/kartoffelbei/faiss/"

class AssistantPipeline:
    def __init__(self):
        #load Models ( one for intent, one for answering, one embedded)
        self.model_manager = ModelManager()
        self.model_manager.load_all()
        self.api_requests = APIRequests()
        self.api_request_builder = APIRequestBuilder(self.api_requests)
        self.faiss_store = None
        self.rag_handler = RAG_Handler()
        #if not os.path.exists(FAISS_PATH):
        #    texts = self.rag_handler.create_database()
        #    chunks = self.rag_handler.text_preparation(texts)
        #    self.faiss_store = self.rag_handler.vectorize_and_store(chunks, self.model_manager.embedding_model)
        #    self.rag_handler.save_faiss_local(self.faiss_store,FAISS_PATH)
        #else:
        #    self.faiss_store = self.rag_handler.load_faiss_local

        #load intent router
        self.router = IntentRouter(self.model_manager)

    def run(self, input: str):
        # get JSON with keywords
        intents = self.router.extract_intent(input)

        # decide which RAG method is necessary
        if intents.get("intent") != Intent.OTHER.value:
            print("Ask API for livedata")
            result = self.api_request_builder.send_api_request(intents)
        else:
            print("static knowledge from website is enough")
            result = self.rag_handler.search_similiar(self.faiss_store, input, 5)

        SYSTEM_PROMPT = """
        You are RailBot, a helpful assistant for Finnish railway travel.

        Use ONLY the provided context data.
        Never invent train times, delays, routes, or prices.

        Rules:
        - If context is incomplete, say so clearly.
        - Keep answers concise (max 4 sentences unless asked for more).
        - Stay within railway topics only.
        - If no relevant data exists, say you cannot find the information.
        """

        USER_PROMPT = f"""
        User question:
        {input}

        Retrieved context:
        {result}

        Generate the best possible answer for the user.
        """

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT}
        ]

        inputs = self.model_manager.answer_tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(self.model_manager.answer_model.device)

        outputs = self.model_manager.answer_model.generate(
            **inputs,
            max_new_tokens=180,
            temperature=0.3,
            do_sample=True,
            eos_token_id=self.model_manager.answer_tokenizer.eos_token_id,
            pad_token_id=self.model_manager.answer_tokenizer.eos_token_id
        )

        input_length = inputs["input_ids"].shape[1]
        generated = outputs[0][input_length:]

        response = self.model_manager.answer_tokenizer.decode(generated, skip_special_tokens=True)

        print(f"Query: {input}")
        print(f"Answer: {response}")

        


