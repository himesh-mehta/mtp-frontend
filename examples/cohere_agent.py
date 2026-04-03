import pathlib
import sys
import os

# Add src to path
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mtp import Agent, ToolRegistry, load_dotenv_if_available
from mtp.providers import Cohere
from mtp.toolkits import CalculatorToolkit

def main():
    load_dotenv_if_available()
    tools = ToolRegistry()
    tools.register_toolkit_loader("calculator", CalculatorToolkit())
    
    # Cohere is unique because of its native RAG and reasoning strengths.
    provider = Cohere(
        model="command-a-03-2025",
        temperature=0.3
    )
    
    agent = Agent(provider=provider, tools=tools, debug_mode=True)
    
    print("--- Starting Cohere Agent ---")
    response = agent.run("What is 12345 / 5?")
    print(f"\nFinal Response: {response}")

if __name__ == "__main__":
    main()
