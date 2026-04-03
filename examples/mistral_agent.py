import pathlib
import sys
import os

# Add src to path
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mtp import Agent, ToolRegistry, load_dotenv_if_available
from mtp.providers import Mistral
from mtp.toolkits import CalculatorToolkit

def main():
    load_dotenv_if_available()
    tools = ToolRegistry()
    tools.register_toolkit_loader("calculator", CalculatorToolkit())
    
    # Mistral Large is their frontier model with native tool-calling support.
    provider = Mistral(
        model="mistral-large-latest",
        temperature=0.0
    )
    
    agent = Agent(provider=provider, tools=tools, debug_mode=True)
    
    print("--- Starting Mistral Agent ---")
    response = agent.run("Can you add 1357 and 2468?")
    print(f"\nFinal Response: {response}")

if __name__ == "__main__":
    main()
