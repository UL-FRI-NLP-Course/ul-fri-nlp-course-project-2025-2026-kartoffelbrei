from models import ModelManager
from intent_router import IntentRouter
import torch
from dataclasses import dataclass

@dataclass
class SystemPrompt:
    persona: str
    domain_boundaries: str
    output_format: str
    guardrails: str
    examples: str
    
    def to_prompt(self) -> str:
        return f"""{self.persona}

                {self.domain_boundaries}

                {self.output_format}

                {self.guardrails}

                {self.examples}"""
    
    
class AssistantPipeline:
    def __init__(self):
        #load Models ( one for intent, one for answering, one embedded)
        self.model_manager = ModelManager()
        self.model_manager.load_all()
        
        #load intent router
        self.router = IntentRouter(self.model_manager)

    def pipeline(self, input: str):
        result = ""
        # get JSON with keywords
        intents = self.router.extract_with_llm(input)

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
        system_prompt= SystemPrompt(
        persona="You are a helpful and precise assistant for finnish  railway system. Your name is 'RailBot'. You always speak in a friendly and professional manner.",
    
        domain_boundaries="""YOUR AREA OF RESPONSIBILITY (EXCLUSIVELY):
        - Train connections, delays, and arrival times
        - Ticket prices
        - Luggage regulations and bicycle transport
        - Station information and services

        TOPICS OUTSIDE YOUR DOMAIN:
        - Air, bus, or other means of transportation (except in connection with train travel)
        - Politics, sports, weather, or other general topics
        - Technical support for devices or software""",
            
            output_format="""RESPONSE FORMAT:
        1. Answer the question precisely using the available data
        2. If data is missing, state this honestly
        3. Keep responses to a maximum of 3-4 sentences, unless the user explicitly requests details""",
            
            guardrails="""IMPORTANT SAFETY RULES:
        - NEVER invent train numbers, times, or delays
        - If the API provides no data, say: "I am currently unable to retrieve real-time data for this connection."
        - For questions outside the railway context, respond: "As a railway assistant, I can only provide information about train travel and railway-related topics."
        - Always remain polite, even with unfriendly requests
        - Do not provide legal advice (e.g., regarding compensation claims)""",
            
            examples="""EXAMPLES:

        User: "Is IC 1 delayed?"
        Assistant: "According to real-time data, IC 1 is currently delayed by 15 minutes. The reason is a signal malfunction in Turku area. The scheduled departure from Helsinki Central Station is therefore postponed to 14:45."

        User: "Who will win the World Cup?"
        Assistant: "As a railway assistant, I can only provide information about train travel and railway-related topics. May I help you with a train connection or timetable inquiry instead?" """
        ).to_prompt()
        
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

        


