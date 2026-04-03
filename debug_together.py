import os
from dotenv import load_dotenv
from together import Together

load_dotenv()
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

try:
    print("--- TOGETHER AI TEST ---")
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=[{"role": "user", "content": "What is 1+1?"}],
        tools=[{
            "type": "function", 
            "function": {
                "name": "calculator__add", 
                "description": "Add numbers",
                "parameters": {
                    "type": "object", 
                    "properties": {
                        "a": {"type": "number"},
                        "b": {"type": "number"}
                    },
                    "required": ["a", "b"]
                }
            }
        }],
        tool_choice="auto"
    )
    print("Success!")
    print(response.choices[0].message)
except Exception as e:
    print(f"FULL ERROR: {e}")
    if hasattr(e, "response"):
        print(f"RESPONSE JSON: {e.response.json()}")
