import pathlib
import sys
import os

# Add src to path
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[0] / "src"))

from mtp import Agent, ToolRegistry, load_dotenv_if_available
from mtp.providers import Groq
from mtp.toolkits import CalculatorToolkit

def main():
    load_dotenv_if_available()
    
    tools = ToolRegistry()
    tools.register_toolkit_loader("calculator", CalculatorToolkit())
    
    # Use standard model
    provider = Groq(
        model="llama-3.3-70b-versatile"
    )
    
    agent = Agent(provider=provider, tools=tools, debug_mode=True)
    
    print("--- Running Simple Groq Test ---")
    try:
        # This usually triggers a plan with a dependency
        response = agent.run("Calculate (123 + 456) * 789")
        print(f"\nFinal Response: {response}")
    except Exception as e:
        print(f"\nCaught Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
