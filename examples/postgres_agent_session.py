import os
import pathlib
import sys

# Add src to path
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mtp import Agent, PostgresSessionStore
from mtp.providers import OpenAI
from mtp.toolkits import CalculatorToolkit


def main() -> None:
    Agent.load_dotenv_if_available()

    db_url = os.getenv("MTP_POSTGRES_DB_URL", "postgresql://user:pass@localhost:5432/mtp")
    session_store = PostgresSessionStore(db_url=db_url, session_table="mtp_sessions")

    tools = Agent.ToolRegistry()
    tools.register_toolkit_loader("calculator", CalculatorToolkit())

    agent = Agent.MTPAgent(
        provider=OpenAI(model="gpt-4o"),
        tools=tools,
        session_store=session_store,
        debug_mode=True,
    )

    session_id = "postgres_demo_session"
    print(agent.run("Remember: my sprint ends on Friday.", session_id=session_id, user_id="demo-user"))
    print(agent.run("When does my sprint end?", session_id=session_id, user_id="demo-user"))


if __name__ == "__main__":
    main()
