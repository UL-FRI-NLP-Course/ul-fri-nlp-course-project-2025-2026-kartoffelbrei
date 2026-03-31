from llama_cpp import Llama
from huggingface_hub import hf_hub_download
import os

MODEL_PATH = "llm_engine/models/llama-2-7b-chat.Q4_K_M.gguf"

def run_llm(trains):
    if not os.path.exists(MODEL_PATH):
        hf_hub_download(
            repo_id="TheBloke/Llama-2-7B-Chat-GGUF",
            filename="llama-2-7b-chat.Q4_K_M.gguf",
            local_dir="ul-fri-nlp-course-project-2025-2026-kartoffelbrei/src/llm_engine")

    llm = Llama(
        model_path="llm_engine/llama-2-7b-chat.Q4_K_M.gguf",
        n_ctx=512,
        n_threads=4
    )

    # Provide a prompt
    prompt = """
    Is there a train in the following data that goes from Helsinki to Espoo?
    
    Train data:

    Train 101
    Route: Helsinki → Espoo → Kirkkonummi
    Departure (Helsinki): 08:15
    Arrival (Espoo): 08:30
    Status: On time

    Train 205
    Route: Helsinki → Vantaa → Kerava
    Departure (Helsinki): 09:00
    Arrival (Espoo): not available
    Status: Does not stop in Espoo

    Train 312
    Route: Helsinki → Espoo → Kauniainen → Kirkkonummi
    Departure (Helsinki): 10:20
    Arrival (Espoo): 10:35
    Status: Delayed 5 minutes
    """

    # Generate the response
    output = llm(prompt, max_tokens=250)

    # Print the response
    print(output["choices"][0]["text"].strip())
