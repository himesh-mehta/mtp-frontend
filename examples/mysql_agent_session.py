import os
import pathlib
import sys

# Add src to path
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from mtp import Agent, MySQLSessionStore
from mtp.providers import OpenAI
from mtp.toolkits import CalculatorToolkit


def main() -> None:
    Agent.load_dotenv_if_available()

    session_store = MySQLSessionStore(
        host=os.getenv("MTP_MYSQL_HOST", "localhost"),
        user=os.getenv("MTP_MYSQL_USER", "root"),
        password=os.getenv("MTP_MYSQL_PASSWORD", "secret"),
        database=os.getenv("MTP_MYSQL_DATABASE", "mtp"),
        port=int(os.getenv("MTP_MYSQL_PORT", "3306")),
        session_table="mtp_sessions",
    )

    tools = Agent.ToolRegistry()
    tools.register_toolkit_loader("calculator", CalculatorToolkit())

    agent = Agent.MTPAgent(
        provider=OpenAI(model="gpt-4o"),
        tools=tools,
        session_store=session_store,
        debug_mode=True,
    )

    session_id = "mysql_demo_session"
    print(agent.run("Remember: release date is April 15.", session_id=session_id, user_id="demo-user"))
    print(agent.run("What is the release date?", session_id=session_id, user_id="demo-user"))


if __name__ == "__main__":
    main()
