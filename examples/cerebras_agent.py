import pathlib
import sys
import os

# Add src to path
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mtp import Agent
from mtp.providers import Cerebras
from mtp.toolkits import CalculatorToolkit

def main():
    Agent.load_dotenv_if_available()
    tools = Agent.ToolRegistry()
    tools.register_toolkit_loader("calculator", CalculatorToolkit())
    
    # Cerebras is the world's fastest inference (wafer-scale chips)
    provider = Cerebras(
        model="qwen-3-235b-a22b-instruct-2507",
        temperature=0.0
    )
    
    agent = Agent(provider=provider, tools=tools, debug_mode=True)
    
    print("--- Starting Cerebras Agent ---")
    print("Task: Multiply 123 by 456")
    response = agent.run("What is 123 * 456?")
    print(f"\nFinal Response: {response}")

if __name__ == "__main__":
    main()
