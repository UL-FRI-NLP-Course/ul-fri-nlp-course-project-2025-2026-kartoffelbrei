# models.py
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from sentence_transformers import SentenceTransformer
from config import config

class ModelManager:
    def __init__(self):
        self.intent_model = None
        self.intent_tokenizer = None
        self.answer_model = None
        self.answer_tokenizer = None
        self.embedding_model = None
        self.access_token = "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"

        
    def load_intent_model(self):
        print(f"Load Intent-model: {config.INTENT_MODEL}")
        
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True
        )
        
        self.intent_tokenizer = AutoTokenizer.from_pretrained(config.INTENT_MODEL, trust_remote_code=True)
        self.intent_tokenizer.pad_token = self.intent_tokenizer.eos_token
        self.intent_tokenizer.padding_side = "left"

        self.intent_model = AutoModelForCausalLM.from_pretrained(
            config.INTENT_MODEL,
            token=self.access_token,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code= True,
        )
        print("Intent-model loaded")


    def load_answer_model(self):
        print(f"Lade Antwort-Modell: {config.ANSWER_MODEL} auf {config.DEVICE_ANSWER}")
        
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=config.USE_4BIT,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True
        ) if config.USE_4BIT else None
        
        self.answer_tokenizer = AutoTokenizer.from_pretrained(config.ANSWER_MODEL)
        self.answer_model = AutoModelForCausalLM.from_pretrained(
            config.ANSWER_MODEL,
            quantization_config=bnb_config,
            device_map=config.DEVICE_ANSWER,
            torch_dtype=torch.float16
        )
        
    def load_embedding_model(self):
        print(f"Lade Embedding-Modell: {config.EMBEDDING_MODEL}")
        self.embedding_model = SentenceTransformer(config.EMBEDDING_MODEL)
        
    def load_all(self):
        self.load_intent_model()
        self.load_answer_model()
        self.load_embedding_model()