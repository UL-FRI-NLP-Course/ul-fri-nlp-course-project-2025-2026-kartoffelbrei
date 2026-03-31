from llama_cpp import Llama

def run_llm():
   llm = Llama(
       model_path="llm_engine/models/llama-2-7b-chat.Q4_K_M.gguf",
       n_ctx=512,
       n_threads=4
   )

   # Provide a prompt
   prompt = """
   You are an environmental monitoring assistant.

   Based on the provided weather data, decide whether the user should carry an umbrella tomorrow.

   Respond in natural, clear, and concise language.

   Your answer should:
   - Directly address whether an umbrella is recommended
   - Briefly explain the reasoning using the weather conditions
   - Be easy to understand (like giving advice to a person)

   Do not use bullet points or JSON.

   ---

   WEATHER DATA (Tomorrow):

   Location: Ljubljana

   - Temperature: 12°C to 17°C
   - Humidity: 85%
   - Pressure: 1004 hPa (falling)
   - Chance of rain: 70%
   - Weather condition: Cloudy with periods of rain
   - Wind: 10 km/h

   ---

   Respond naturally.
   """

   # Generate the response
   output = llm(prompt, max_tokens=250)

   # Print the response
   print(output["choices"][0]["text"].strip())
