import pathlib
import sys

# Add src to path
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mtp import Agent
from mtp.providers import OpenAI
from mtp.toolkits import CalculatorToolkit


def main() -> None:
    Agent.load_dotenv_if_available()

    tools = Agent.ToolRegistry()
    tools.register_toolkit_loader("calculator", CalculatorToolkit())

    provider = OpenAI(model="gpt-4o")
    agent = Agent(provider=provider, tools=tools, debug_mode=True)

    image = Agent.Image(url="https://upload.wikimedia.org/wikipedia/commons/0/0c/GoldenGateBridge-001.jpg")
    note = Agent.File(content="Quarterly growth: Q1 12%, Q2 15%, Q3 19%", filename="note.txt", mime_type="text/plain")
    # Small dummy audio payload for request-shape testing.
    audio = Agent.Audio(content=b"RIFF....WAVEfmt ", format="wav")

    response = agent.run(
        "Describe the image briefly, summarize the note, then compute (12 * 19).",
        images=[image],
        files=[note],
        audios=[audio],
    )
    print(response)


if __name__ == "__main__":
    main()
