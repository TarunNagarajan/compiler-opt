import os
from google import genai
from google.genai import types

def query_oracle():
    try:
        # Initializing the modern Google GenAI SDK
        client = genai.Client()
        
        prompt = """
        I am training a Reinforcement Learning agent (MAPPO) to optimize LLVM compiler graphs.
        
        The reward structure is:
        - Dense step reward: `(runtime_before - runtime_after) / runtime_before` (typically ranges from +0.02 to +0.08 per successful step).
        - Correctly stopping when optimized: `0.0` (to avoid penalizing good behavior).
        - Incorrectly stopping prematurely (the code is not fully optimized): `-0.5` terminal penalty.
        - The discount factor is `gamma = 0.99` and GAE `lambda = 0.95`.
        
        A user has raised a concern: "Does the -0.5 reward overshadow the +0.04 step rewards? I feel like the model never has the time to think about the pass choices it makes because it's afraid of the massive -0.5 penalty."
        
        Please act as a Senior RL Researcher and formally evaluate this concern. 
        1. Is a -0.5 terminal penalty mathematically too large compared to dense rewards of +0.04?
        2. With `gamma=0.99`, how many steps back does the -0.5 penalty seriously dominate the advantage calculation?
        3. Should we scale down the -0.5 penalty to something like -0.05, or is the user's fear unwarranted?
        
        Be direct and mathematically precise. Do not placate.
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=prompt,
        )
        print("=== ORACLE RESPONSE ===")
        print(response.text)
        
    except Exception as e:
        print(f"Error calling Oracle: {e}")

if __name__ == "__main__":
    query_oracle()
