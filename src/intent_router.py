# intent_router.py
import json
import re
import torch
from typing import Dict, List, Optional
from models import ModelManager
from config import config

class IntentRouter:
    def __init__(self, model_manager: ModelManager):
        self.manager = model_manager
        
    def extract_with_llm(self, user_query: str) -> Dict:
       
        prompt = f"""Extract all relevant information regarding train connections of the following user query. The answer must consist only of a valid JSON-object.

user query: "{user_query}"

The JSON has to contain the following fields:
- intent: "delay", "arrival", "departure", "connection", "info", "other"
- train_type: "AE", "IC", "PYO", "H", "S", "HDM", "Letter", "other"
- train_number: Number of the train (e.g. "46") or null
- station: station where to start from (e.g. "Helsinki") or null
- destination: station of destination or null
- needs_api: true if live data is needed, false if it's static information

JSON:"""
        
        inputs = self.manager.intent_tokenizer(prompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = self.manager.intent_model.generate(
                **inputs,
                max_new_tokens=200,
                temperature=0.1,
                do_sample=False
            )
        
        response = self.manager.intent_tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Antwort: {response}")
        # JSON aus Response extrahieren
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
            
     