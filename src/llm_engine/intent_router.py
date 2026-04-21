import json
import re
import torch
from typing import Dict

from src.llm_engine.model_manager import ModelManager
from src.llm_engine.system_prompts import query_extraction_prompt

class IntentRouter:
    def __init__(self, model_manager: ModelManager):
        self.manager = model_manager
        
    def extract_with_llm(self, user_query: str) -> Dict:
       
        prompt = query_extraction_prompt
        
        inputs = self.manager.intent_tokenizer(prompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = self.manager.intent_model.generate(
                **inputs,
                max_new_tokens=200,
                temperature=0.1,
                do_sample=False
            )
        
        response = self.manager.intent_tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"Answer: {response}")
        # JSON aus Response extrahieren
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
            
     