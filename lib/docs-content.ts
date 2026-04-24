export type DocContentBlock = {
  type: "heading" | "text" | "code" | "list" | "callout" | "table";
  value: string;
  language?: string;
  label?: string;
  output?: string;
  outputLabel?: string;
  items?: string[];
  calloutType?: "note" | "tip" | "warning";
  headers?: string[];
  rows?: string[][];
};

export type DocItem = {
  slug: string;
  title: string;
  description: string;
};

export type DocSection = {
  title: string;
  items: DocItem[];
};

export const docSidebar: DocSection[] = [
  {
    title: "Getting Started",
    items: [
      { slug: "introduction", title: "Introduction", description: "What is MTPX and why use it" },
      { slug: "installation", title: "Installation", description: "Install via pip or from source" },
      { slug: "quickstart", title: "Quickstart", description: "Build your first agent in 5 minutes" },
    ],
  },
  {
    title: "Core Concepts",
    items: [
      { slug: "protocol", title: "MTP Protocol", description: "Protocol entities, execution plans, DAGs" },
      { slug: "agent", title: "Agent API", description: "MTPAgent class, run modes, streaming" },
      { slug: "providers", title: "Providers", description: "13+ LLM provider adapters" },
      { slug: "toolkits", title: "Toolkits", description: "Built-in and custom tool creation" },
      { slug: "policy", title: "Safety Policies", description: "Allow, Ask, Deny execution rules" },
    ],
  },
  {
    title: "Advanced",
    items: [
      { slug: "sessions", title: "Sessions & Storage", description: "JSON, PostgreSQL, MySQL persistence" },
      { slug: "tui", title: "TUI CLI", description: "Interactive terminal interface" },
      { slug: "local-inference", title: "Local Inference", description: "Ollama and LM Studio support" },
      { slug: "mcp", title: "MCP Interop", description: "MCP JSON-RPC adapter" },
      { slug: "transport", title: "Transport", description: "stdio, HTTP, WebSocket envelopes" },
      { slug: "events", title: "Events & Streaming", description: "Runtime event streams" },
    ],
  },
];

export function getDocBySlug(slug: string): DocItem | null {
  for (const section of docSidebar) {
    const item = section.items.find((i) => i.slug === slug);
    if (item) return item;
  }
  return null;
}

export function getAllDocSlugs(): string[] {
  return docSidebar.flatMap((s) => s.items.map((i) => i.slug));
}

export const docPages: Record<string, DocContentBlock[]> = {
  introduction: [
    { type: "heading", value: "What is MTPX?" },
    { type: "text", value: "MTPX (Model Tool Protocol Extended) is a protocol-first Python library for AI agent tool orchestration. It transforms language models from conversational wrappers into structured execution systems — capable of managing real tasks deterministically." },
    { type: "text", value: "Where typical agent frameworks allow models to make unstructured tool calls, MTP requires models to emit structured execution plans (DAGs). The runtime validates schemas, resolves dependencies, enforces policies, and executes deterministically before any tool runs." },
    { type: "heading", value: "Two Explicit Layers" },
    { type: "list", items: [
      "MTP Protocol — protocol entities, tool schemas, execution plans, dependency semantics, and policy contracts.",
      "MTP Agent SDK — the Python framework built on top: providers, toolkits, storage, transport, events, and the agent API.",
    ]},
    { type: "heading", value: "Key Capabilities" },
    { type: "list", items: [
      "Lazy tool loading by toolkit/category",
      "Dependency-aware batch tool execution via DAG plans",
      "Policy-aware execution (allow / ask / deny per tool/param)",
      "Multi-round model-tool-model loops with streaming",
      "13+ provider adapters: Groq, OpenAI, Anthropic, Gemini, Mistral, Cohere, and more",
      "Transport primitives: stdio, HTTP, optional WebSocket envelope transport",
      "MCP JSON-RPC adapter over the same runtime core",
      "Session persistence: JSON, PostgreSQL, MySQL",
    ]},
    { type: "callout", calloutType: "note", value: "MCP support is an interoperability capability, not the product identity. MTP is protocol-first and MCP-compatible." },
    { type: "heading", value: "When to Use MTP" },
    { type: "table", headers: ["Scenario", "Why MTP"], rows: [
      ["Autonomous agents needing multi-step plans", "DAG execution with dependency resolution"],
      ["Production tool orchestration at scale", "Deterministic runtime, policy controls"],
      ["Multi-model applications", "Swap 13+ providers without refactoring"],
      ["Persistent conversation agents", "Built-in session stores (JSON/Postgres/MySQL)"],
      ["MCP ecosystem integration", "First-class MCP JSON-RPC adapter"],
    ]},
  ],

  installation: [
    { type: "heading", value: "From PyPI (Recommended)" },
    { type: "text", value: "Install the base package with pip:" },
    { type: "code", language: "bash", value: "pip install mtpx", output: "Successfully installed mtpx-0.1.17", outputLabel: "Output" },
    { type: "heading", value: "Optional Extras" },
    { type: "text", value: "Install only the provider SDKs you need. The system gracefully handles missing optional dependencies:" },
    { type: "code", language: "bash", value: `# Cloud providers
pip install "mtpx[groq,dotenv]"
pip install "mtpx[openai,anthropic,dotenv]"
pip install "mtpx[gemini]"

# Local inference
pip install "mtpx[lmstudio]"
pip install "mtpx[ollama]"

# Web toolkits
pip install "mtpx[toolkits-web]"

# Database session stores
pip install "mtpx[stores-db]"

# Everything optional
pip install "mtpx[all]"` },
    { type: "heading", value: "Verify Installation" },
    { type: "code", language: "bash", value: `python -c "import mtp; print(f'MTPX version {mtp.__version__} installed!')"`, output: "MTPX version 0.1.17 installed!", outputLabel: "Output" },
    { type: "heading", value: "From Source" },
    { type: "code", language: "bash", value: `git clone https://github.com/GodBoii/Model-Tool-protocol-
cd MTP
python -m venv .venv
.venv\\Scripts\\activate   # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -e .` },
    { type: "callout", calloutType: "tip", value: "Copy .env.example to .env and add your provider API keys. Use the dotenv extra for automatic .env loading: pip install \"mtpx[dotenv]\"" },
  ],

  quickstart: [
    { type: "heading", value: "Create Your First Agent" },
    { type: "text", value: "Build an agent with calculator, file, python, and shell toolkits in under 30 lines:" },
    { type: "code", language: "python", value: `from mtp import Agent
from mtp.providers import Groq
from mtp.toolkits import CalculatorToolkit, FileToolkit, PythonToolkit, ShellToolkit

Agent.load_dotenv_if_available()

tools = Agent.ToolRegistry()
tools.register_toolkit_loader("calculator", CalculatorToolkit())
tools.register_toolkit_loader("file", FileToolkit(base_dir="."))
tools.register_toolkit_loader("python", PythonToolkit(base_dir="."))
tools.register_toolkit_loader("shell", ShellToolkit(base_dir="."))

provider = Groq(model="llama-3.3-70b-versatile")

agent = Agent.MTPAgent(
    provider=provider,
    tools=tools,
    instructions="Use tools when needed. Return concise answers.",
    debug_mode=True,
    strict_dependency_mode=True,
)

response = agent.run(
    "Calculate 25*4+10 and list files in the current directory.",
    max_rounds=4
)
print(response)` },
    { type: "heading", value: "Streaming Responses" },
    { type: "code", language: "python", value: `# Stream final response tokens
agent.print_response("Give a short summary.", max_rounds=4, stream=True)

# Stream structured runtime events
agent.print_response(
    "Give a short summary.",
    max_rounds=4,
    stream=True,
    stream_events=True,
)

# Raw JSON event lines
agent.print_response(
    "Give a short summary.",
    max_rounds=4,
    stream=True,
    stream_events=True,
    event_format="json",
)` },
    { type: "heading", value: "Autoresearch Mode" },
    { type: "text", value: "Enable persistent execution where the model runs until it calls agent.terminate():" },
    { type: "code", language: "python", value: `agent = Agent.MTPAgent(
    provider=provider,
    tools=tools,
    autoresearch=True,
    research_instructions=(
        "Keep working until requirements are satisfied and verified. "
        "Call agent.terminate with reason+summary only when complete."
    ),
    debug_mode=True,
)

agent.print_response(
    "Compute the result and verify with tools. Terminate only after done.",
    max_rounds=12,
    stream=True,
    stream_events=True,
)` },
    { type: "heading", value: "Launch the TUI" },
    { type: "code", language: "bash", value: `mtp tui`, output: `  ███╗   ███╗████████╗██████╗
  ████╗ ████║╚══██╔══╝██╔══██╗
  ██╔████╔██║   ██║   ██████╔╝
  ██║╚██╔╝██║   ██║   ██╔═══╝
  ██║ ╚═╝ ██║   ██║   ██║
  ╚═╝     ╚═╝   ╚═╝   ╚═╝  v0.1.17

  > ready`, outputLabel: "Terminal" },
  ],

  protocol: [
    { type: "heading", value: "Protocol Entities" },
    { type: "text", value: "The MTP protocol defines the core data structures for tool orchestration. These live in mtp.protocol and mtp.schema." },
    { type: "list", items: [
      "ToolSpec — defines a tool: name, description, input schema, risk level",
      "ToolCall — a single invocation: tool name + arguments",
      "ExecutionPlan — an ordered list of ToolCalls forming a DAG",
      "ExecutionResult — output of a single tool call",
      "Envelope — transport wrapper for plans over stdio/HTTP",
    ]},
    { type: "heading", value: "Execution Plan (DAG)" },
    { type: "text", value: "The model emits a structured JSON plan. Each step can declare dependencies on previous steps via $ref. The runtime resolves the graph before executing:" },
    { type: "code", language: "json", value: `{
  "plan": [
    {
      "step_id": "fetch_logs",
      "tool": "read_file",
      "args": { "path": "/var/log/app.log" }
    },
    {
      "step_id": "analyze",
      "tool": "diagnose_trace",
      "args": {
        "log_data": { "$ref": "fetch_logs" }
      }
    }
  ]
}` },
    { type: "callout", calloutType: "note", value: "The $ref syntax allows steps to reference outputs from previous steps, enabling true dependency-aware parallel and sequential execution." },
    { type: "heading", value: "Schema Validation" },
    { type: "text", value: "mtp.schema provides versioned envelope validation and execution plan validation. Plans are checked before any tool executes, giving you early failure detection and safe defaults." },
  ],

  agent: [
    { type: "heading", value: "MTPAgent API" },
    { type: "text", value: "The MTPAgent class is the main interface. It coordinates the provider (LLM), runtime (tool execution), and memory (session state)." },
    { type: "code", language: "python", value: `from mtp import Agent
from mtp.providers import OpenAI

agent = Agent.MTPAgent(
    provider=OpenAI(model="gpt-4o"),
    tools=tools,
    instructions="System instructions for the agent.",
    debug_mode=False,
    strict_dependency_mode=True,
    autoresearch=False,
)` },
    { type: "heading", value: "Constructor Parameters" },
    { type: "table", headers: ["Parameter", "Type", "Description"], rows: [
      ["provider", "BaseProvider", "The LLM provider adapter to use"],
      ["tools", "ToolRegistry", "Registry of available tools/toolkits"],
      ["instructions", "str", "System prompt / agent persona"],
      ["debug_mode", "bool", "Enable verbose logging"],
      ["strict_dependency_mode", "bool", "Enforce DAG dependency resolution"],
      ["autoresearch", "bool", "Enable persistent execution until terminate()"],
      ["session_store", "BaseSessionStore", "Persistence backend for conversation history"],
    ]},
    { type: "heading", value: "Running the Agent" },
    { type: "code", language: "python", value: `# Basic run — returns final response string
response = agent.run("Your prompt here", max_rounds=4)

# Print with streaming
agent.print_response("Your prompt", max_rounds=4, stream=True)

# With session persistence
agent.run(
    "Remember: project codename is Atlas.",
    session_id="chat-1",
    user_id="u1",
)` },
  ],

  providers: [
    { type: "heading", value: "Supported Providers" },
    { type: "text", value: "MTPX includes adapters for 13+ foundation model providers. All implement the same BaseProvider interface — swap them without changing any agent code." },
    { type: "table", headers: ["Provider", "Extra", "Notes"], rows: [
      ["OpenAI", "mtpx[openai]", "GPT-4o, GPT-4o-mini, etc."],
      ["Anthropic", "mtpx[anthropic]", "Claude 3.5 Sonnet, Claude 3 Opus"],
      ["Groq", "mtpx[groq]", "Ultra-fast Llama, Mixtral inference"],
      ["Google Gemini", "mtpx[gemini]", "Gemini 1.5 Pro/Flash"],
      ["OpenRouter", "built-in", "Access 200+ models via one key"],
      ["Mistral", "mtpx[mistral]", "Mistral Large, Codestral"],
      ["Cohere", "mtpx[cohere]", "Command R+"],
      ["DeepSeek", "built-in", "DeepSeek-V3, R1"],
      ["SambaNova", "built-in", "High-throughput inference"],
      ["Cerebras", "built-in", "CS-3 chip inference"],
      ["Together AI", "built-in", "Open model hosting"],
      ["Fireworks AI", "built-in", "Fast open model serving"],
      ["LM Studio", "mtpx[lmstudio]", "Local inference via LM Studio"],
      ["Ollama", "mtpx[ollama]", "Local inference via Ollama"],
    ]},
    { type: "heading", value: "Using a Provider" },
    { type: "code", language: "python", value: `from mtp.providers import Groq, OpenAI, Anthropic, Gemini

# Groq — fastest inference
provider = Groq(model="llama-3.3-70b-versatile")

# OpenAI
provider = OpenAI(model="gpt-4o")

# Anthropic
provider = Anthropic(model="claude-3-5-sonnet-20241022")

# Gemini
provider = Gemini(model="gemini-1.5-pro")` },
    { type: "callout", calloutType: "tip", value: "All providers accept an api_key parameter. If not set, they read from the corresponding environment variable (GROQ_API_KEY, OPENAI_API_KEY, etc.)." },
  ],

  toolkits: [
    { type: "heading", value: "Built-in Toolkits" },
    { type: "text", value: "MTPX ships with production-ready toolkits. Each toolkit is a collection of related tools that can be lazily loaded." },
    { type: "table", headers: ["Toolkit", "Tools Included", "Extra"], rows: [
      ["CalculatorToolkit", "evaluate, compute_expression", "none"],
      ["FileToolkit", "read_file, write_file, list_dir, delete_file", "none"],
      ["PythonToolkit", "run_python_code, execute_script", "none"],
      ["ShellToolkit", "run_shell_command, run_bash", "none"],
      ["WebToolkit", "search_web, fetch_url, scrape_page", "mtpx[toolkits-web]"],
    ]},
    { type: "heading", value: "Registering Toolkits" },
    { type: "code", language: "python", value: `from mtp import Agent
from mtp.toolkits import CalculatorToolkit, FileToolkit

tools = Agent.ToolRegistry()
tools.register_toolkit_loader("calculator", CalculatorToolkit())
tools.register_toolkit_loader("file", FileToolkit(base_dir="/workspace"))` },
    { type: "heading", value: "Creating Custom Tools" },
    { type: "code", language: "python", value: `from mtp.tools import tool

@tool(description="Fetch weather for a city")
def get_weather(city: str, unit: str = "celsius") -> dict:
    """Returns current weather data."""
    # Your implementation here
    return {"city": city, "temp": 22, "unit": unit}

tools.register("get_weather", get_weather)` },
  ],

  policy: [
    { type: "heading", value: "Safety Policy System" },
    { type: "text", value: "MTP's policy module lets you define fine-grained execution rules per tool or parameter. Three rule types are supported:" },
    { type: "list", items: [
      "allow — execute without user confirmation",
      "ask — pause and prompt the user before executing",
      "deny — block execution entirely and return an error",
    ]},
    { type: "heading", value: "Configuring Policies" },
    { type: "code", language: "python", value: `from mtp.policy import Policy, Rule

policy = Policy([
    Rule(tool="read_file", action="allow"),
    Rule(tool="delete_file", action="ask"),
    Rule(tool="run_shell_command", param="cmd", pattern=r"rm -rf", action="deny"),
])

agent = Agent.MTPAgent(
    provider=provider,
    tools=tools,
    policy=policy,
)` },
    { type: "callout", calloutType: "warning", value: "Without a policy, all tools default to 'allow'. For production deployments, always configure explicit policies for destructive tools like delete_file and run_shell_command." },
  ],

  sessions: [
    { type: "heading", value: "Session Persistence" },
    { type: "text", value: "MTPX supports three built-in session stores for persisting conversation history across runs." },
    { type: "heading", value: "JSON Session Store" },
    { type: "code", language: "python", value: `from mtp import Agent, JsonSessionStore
from mtp.providers import OpenAI

session_store = JsonSessionStore(db_path="tmp/mtp_json_db")
agent = Agent.MTPAgent(
    provider=OpenAI(model="gpt-4o"),
    tools=tools,
    session_store=session_store,
)

agent.run("Remember: project codename is Atlas.", session_id="chat-1", user_id="u1")
agent.run("What is the project codename?", session_id="chat-1", user_id="u1")` },
    { type: "heading", value: "PostgreSQL Store" },
    { type: "code", language: "python", value: `from mtp import PostgresSessionStore

pg_store = PostgresSessionStore(
    db_url="postgresql://user:pass@localhost:5432/mtp"
)` },
    { type: "heading", value: "MySQL Store" },
    { type: "code", language: "python", value: `from mtp import MySQLSessionStore

my_store = MySQLSessionStore(
    host="localhost",
    user="root",
    password="secret",
    database="mtp",
    port=3306,
)` },
    { type: "callout", calloutType: "note", value: "Install the stores extra for database backends: pip install \"mtpx[stores-db]\"" },
  ],

  tui: [
    { type: "heading", value: "Interactive TUI" },
    { type: "text", value: "The MTP TUI (mtp tui) is a premium terminal chat interface. It supports 13 AI provider backends, persistent centralized sessions, real-time token metrics, live tool event streaming, an animated cat companion with cursor tracking, and Nerd Font glyph support." },
    { type: "heading", value: "Launch" },
    { type: "code", language: "bash", value: `# Default launch
mtp tui

# Launch with a specific provider
mtp tui --backend groq
mtp tui --backend claude
mtp tui --backend ollama

# Enable autoresearch from launch
mtp tui --backend groq --autoresearch` },
    { type: "heading", value: "Multi-Provider Support" },
    { type: "text", value: "Switch between 13 providers mid-session without losing your conversation. First-time setup prompts for API key and model selection, then saves to ~/.mtp/settings/provider_settings.json." },
    { type: "code", language: "bash", value: `# List all providers with configuration status
/backend

# Cloud providers
/backend groq      # default: llama-3.3-70b-versatile
/backend openai    # default: gpt-4o
/backend claude    # default: claude-3-5-sonnet-20241022
/backend gemini    # default: gemini-2.0-flash-exp

# Local inference (no API key needed)
/backend ollama    # auto-discovers local models
/backend lmstudio  # auto-discovers LM Studio models` },
    { type: "heading", value: "Session Management" },
    { type: "text", value: "Sessions are stored centrally in ~/.mtp/sessions/ and are accessible from any project directory. Session titles are auto-generated from your first message." },
    { type: "code", language: "bash", value: `# List sessions (current directory shown first)
/sessions

# Start a new session with optional label
/new my-research-project

# Resume a saved session
/load <session_id>

# View session as read-only
/open <session_id>

# Show recent n turns
/history
/history 10` },
    { type: "heading", value: "Metrics Display" },
    { type: "text", value: "After each response, TUI displays comprehensive usage metrics. Context bar color codes: green (0–60%), yellow (60–85%), red (85–100%)." },
    { type: "code", language: "bash", value: `ctx [████████████░░░░░░░░] 32,768/131,072 (25%)
tokens(in/out/total/reasoning)=6316/796/7112/643
llm_calls=4  duration=10.80s  speed=658.5 tokens/s

# Thinking tokens (Ollama with supported models):
💭 thinking  Let me calculate this step by step...` },
    { type: "heading", value: "Full Command Reference" },
    { type: "table", headers: ["Command", "Description"], rows: [
      ["/backend [name]", "List or switch to a provider"],
      ["/models", "Show all models for all providers"],
      ["/model <name>", "Switch to a specific model"],
      ["/model add <provider> <name>", "Add a custom model"],
      ["/apikey set <provider> <key>", "Set/update API key"],
      ["/apikey", "List all API keys (masked)"],
      ["/sessions", "List all saved sessions grouped by directory"],
      ["/new [label]", "Start a new labeled session"],
      ["/load <id>", "Resume a saved session"],
      ["/history [n]", "Show recent turns in current session"],
      ["/status", "Current session state + latest metrics"],
      ["/rounds <n>", "Set max_rounds for MTP providers"],
      ["/autoresearch on|off", "Toggle autoresearch mode"],
      ["/cat <show|hide>", "Toggle animated cat companion"],
      ["/nerdfont <on|off>", "Toggle Nerd Font glyph support"],
      ["/clear", "Clear the terminal screen"],
      ["/exit", "Exit TUI"],
    ]},
    { type: "heading", value: "File Attachments" },
    { type: "code", language: "bash", value: `> debug this @src/mtp/cli/tui.py and suggest a fix
> explain the logic in @agent.py and compare to @runtime.py` },
    { type: "heading", value: "Aesthetics" },
    { type: "list", items: [
      "Phosphor Decay: streaming text appears bright then 'cools' into layout — like hot ink drying",
      "Animated Cat Companion: follows your input cursor laterally, reacts to generation states",
      "Input Pulse: dynamic animation on the input box during active generation",
      "Nerd Font Mode: /nerdfont on enables high-fidelity icon glyphs (requires a Nerd Font installed)",
      "Telemetry HUD: right-gutter sidebar shows CWD, Sandbox mode, attachment count",
    ]},
    { type: "callout", calloutType: "tip", value: "Sessions persist even if project directories are deleted. Use /sessions from any directory to find and resume past conversations." },
  ],


  "local-inference": [
    { type: "heading", value: "Local Inference" },
    { type: "text", value: "Run models completely locally using LM Studio or Ollama. No API keys, no data leaving your machine." },
    { type: "heading", value: "Ollama Setup" },
    { type: "code", language: "bash", value: `pip install "mtpx[ollama]"
ollama pull llama3
mtp tui
# then: /backend ollama` },
    { type: "heading", value: "LM Studio Setup" },
    { type: "code", language: "bash", value: `pip install "mtpx[lmstudio]"
# Start LM Studio and load a model
mtp tui
# then: /backend lmstudio` },
    { type: "heading", value: "Programmatic Usage" },
    { type: "code", language: "python", value: `from mtp.providers import Ollama, LMStudio

# Ollama
provider = Ollama(model="llama3", base_url="http://localhost:11434")

# LM Studio
provider = LMStudio(model="local-model", base_url="http://localhost:1234")

agent = Agent.MTPAgent(provider=provider, tools=tools)` },
  ],

  mcp: [
    { type: "heading", value: "MCP Interoperability" },
    { type: "text", value: "MTPX includes a first-class MCP JSON-RPC adapter that wraps the ToolRegistry, making it compatible with any MCP client." },
    { type: "callout", calloutType: "note", value: "MCP support is intentional and strategic. MTP supports MCP method surfaces, transports, auth, cancellation, and progress — but remains its own protocol." },
    { type: "heading", value: "MCP Server via stdio" },
    { type: "code", language: "python", value: `from mtp.mcp import MCPAdapter
from mtp import Agent
from mtp.toolkits import CalculatorToolkit

tools = Agent.ToolRegistry()
tools.register_toolkit_loader("calculator", CalculatorToolkit())

# Expose tools as an MCP server over stdio
adapter = MCPAdapter(tools)
adapter.serve_stdio()` },
    { type: "heading", value: "MCP Transport Modes" },
    { type: "list", items: [
      "stdio transport — for local MCP clients (Claude Desktop, etc.)",
      "HTTP transport — for networked MCP clients",
      "WebSocket envelope transport (experimental)",
    ]},
  ],

  transport: [
    { type: "heading", value: "Transport Layer" },
    { type: "text", value: "The MTP transport layer defines how execution envelopes move between agents, runtimes, and external systems." },
    { type: "heading", value: "stdio Transport" },
    { type: "code", language: "python", value: `from mtp.transport import StdioTransport

transport = StdioTransport()
transport.send(envelope)
response = transport.receive()` },
    { type: "heading", value: "HTTP Transport" },
    { type: "code", language: "python", value: `from mtp.transport import HTTPTransport

transport = HTTPTransport(base_url="http://localhost:8080")
transport.send(envelope)` },
    { type: "callout", calloutType: "note", value: "Transports only move envelopes/messages. Business logic lives in the agent and runtime layers." },
  ],

  events: [
    { type: "heading", value: "Events & Streaming" },
    { type: "text", value: "MTPX emits structured runtime events during agent execution. Subscribe to these for observability, logging, or building custom UIs." },
    { type: "heading", value: "Event Types" },
    { type: "list", items: [
      "agent.start — agent loop begins",
      "tool.call — a tool is about to be invoked",
      "tool.result — a tool execution completed",
      "model.stream — a streaming token from the LLM",
      "agent.complete — the agent loop finished",
      "agent.error — an error occurred",
    ]},
    { type: "heading", value: "Consuming Events" },
    { type: "code", language: "python", value: `# Human-readable event logs (default)
agent.print_response(
    "Your prompt",
    stream=True,
    stream_events=True,
)

# Raw JSON event stream
agent.print_response(
    "Your prompt",
    stream=True,
    stream_events=True,
    event_format="json",
)` },
    { type: "callout", calloutType: "tip", value: "Use stream_events=True with event_format='json' to pipe events into your own monitoring or observability system." },
  ],
};
