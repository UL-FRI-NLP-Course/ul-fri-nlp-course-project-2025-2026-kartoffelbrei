import torch

from .model_manager import ModelManager
from .intent_router import IntentRouter

class AssistantPipeline:
    def __init__(self):
        #load Models ( one for intent, one for answering, one embedded)
        self.model_manager = ModelManager()
        self.model_manager.load_all()
        
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
            # TODO User scraped websites -> some mock results
            result = """Train data:
                    Train IC 1
                    Route: Helsinki → Espoo → Kirkkonummi
                    Departure (Helsinki): 08:15
                    Arrival (Espoo): 08:30

                    Train AE 30
                    Route: Helsinki → Vantaa → Kerava
                    Departure (Helsinki): 09:00
                    Arrival (Espoo): not available
                    
                    Train IC 5
                    Route: Helsinki → Espoo → Kauniainen → Kirkkonummi
                    Departure (Helsinki): 10:20
                    Arrival (Espoo): 10:35
                    
                    """

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

        


