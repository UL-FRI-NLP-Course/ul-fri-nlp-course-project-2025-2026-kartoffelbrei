import torch
from src.backend.website_handler import RAG_Handler
from src.llm_engine.model_manager import ModelManager
from src.llm_engine.intent_router import IntentRouter
import os

FAISS_PATH= "/d/hpc/projects/onj_fri/kartoffelbei/faiss/"

class AssistantPipeline:
    def __init__(self):
        #load Models ( one for intent, one for answering, one embedded)
        self.model_manager = ModelManager()
        self.model_manager.load_all()
        self.faiss_store = None
        self.rag_handler = RAG_Handler()
        if not os.path.exists(FAISS_PATH):
            texts = self.rag_handler.create_database()
            chunks = self.rag_handler.text_preparation(texts)
            self.faiss_store = self.rag_handler.vectorize_and_store(chunks, self.model_manager.embedding_model)
            self.rag_handler.save_faiss_local(self.faiss_store,FAISS_PATH)
        else: 
            self.faiss_store = self.rag_handler.load_faiss_local

        #load intent router
        self.router = IntentRouter(self.model_manager)

    def run(self, input: str):
        result = ""
        # get JSON with keywords
        intents = self.router.extract_intent(input)

        print(f"intents: {intents}")

        # decide which RAG method is necessary
        if intents.get("needs_api"):
            print("Ask API for livedata")
            # TODO API request -> we just mock some results now
            result = """Train data:

                    Train IC 1
                    Status: On time

                    Train AE 30
                    Status: Does not stop in Espoo, delayed 15 minutes

                    Train IC 5
                    Status: Delayed 5 minutes
                    """
        else:
            print("static knowledge from website is enough")
            result = self.rag_handler.search_similiar(self.faiss_store, input, 5)
        
            

        # construct the full prompt
        ## general information for LLM how it should behave
        system_prompt = ""
        
        full_prompt = f"""{system_prompt}
            == context for your answer ==
            {result}
            == User query ==
            {input}
            == Your answer (just based on given context)==
            """
        print("Generating an answer...")
        inputs = self.model_manager.answer_tokenizer(full_prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model_manager.answer_model.generate(
                **inputs,
                max_new_tokens=300,
                temperature=0.3,
                do_sample=True,
                top_p=0.9,
                repetition_penalty=1.1
            )
        response = self.model_manager.answer_tokenizer.decode(outputs[0], skip_special_tokens=True)

        print(f"Die Antwort des Models: {response}")

        


