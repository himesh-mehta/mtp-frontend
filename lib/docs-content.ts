export interface DocSection {
  title: string;
  items: DocItem[];
}

export interface DocItem {
  slug: string;
  title: string;
  description: string;
  content: DocContentBlock[];
}

export interface DocContentBlock {
  type: "text" | "code" | "heading" | "list" | "callout" | "table";
  value: string;
  language?: string;
  calloutType?: "note" | "tip" | "warning";
  items?: string[];
  rows?: string[][];
  headers?: string[];
  label?: string;
  output?: string;
  outputLabel?: string;
}

export const docSidebar: DocSection[] = [
  {
    title: "Getting Started",
    items: [
      { slug: "introduction", title: "Introduction", description: "What MTP is and why it exists.", content: [] },
      { slug: "quickstart", title: "Quickstart", description: "Get running in under 3 minutes.", content: [] },
      { slug: "installation", title: "Installation", description: "Install from PyPI or source.", content: [] },
    ],
  },
  {
    title: "Core Concepts",
    items: [
      { slug: "agents", title: "Agents", description: "The orchestration loop that connects models to tools.", content: [] },
      { slug: "execution-plans", title: "Execution Plans", description: "DAG-based structured tool execution.", content: [] },
      { slug: "runtime", title: "Runtime Engine", description: "Validation, caching, policy, and batch execution.", content: [] },
    ],
  },
  {
    title: "Tools",
    items: [
      { slug: "tool-registry", title: "Overview", description: "How tools are registered, discovered, and loaded.", content: [] },
      { slug: "toolkits", title: "Built-in Toolkits", description: "Local and web toolkits shipped with MTP.", content: [] },
      { slug: "creating-tools", title: "Creating Tools", description: "Build custom tools from Python functions.", content: [] },
      { slug: "mcp-interop", title: "MCP Tools", description: "JSON-RPC adapter for MCP compatibility.", content: [] },
    ],
  },
  {
    title: "Features",
    items: [
      { slug: "providers", title: "Multi-Model Support", description: "12+ model adapters with a standard interface.", content: [] },
      { slug: "policies", title: "Policies & Safety", description: "Risk-aware execution control.", content: [] },
      { slug: "persistence", title: "Persistence", description: "Session storage across JSON, Postgres, and MySQL.", content: [] },
      { slug: "streaming", title: "Streaming & Events", description: "Provider-agnostic event stream contract.", content: [] },
    ],
  },
  {
    title: "Advanced",
    items: [
      { slug: "transport", title: "Transport Layer", description: "Stdio, HTTP, and WebSocket envelope transports.", content: [] },
      { slug: "autoresearch", title: "Autoresearch Mode", description: "Persistent execution with explicit termination.", content: [] },
      { slug: "cli", title: "CLI Reference", description: "Scaffold, run, and validate MTP projects.", content: [] },
    ],
  },
  {
    title: "Cookbook",
    items: [
      { slug: "cookbook-calc-to-file", title: "Save Result to File", description: "Chain a calculation into a file write.", content: [] },
      { slug: "cookbook-multi-step", title: "Multi-Step Chains", description: "DAG dependencies across multiple tools.", content: [] },
      { slug: "cookbook-safe-agent", title: "Safe Agent Policies", description: "Block destructive actions with risk policies.", content: [] },
      { slug: "cookbook-memory", title: "Agent With Memory", description: "Persist conversations across sessions.", content: [] },
    ],
  },
  {
    title: "Reference",
    items: [
      { slug: "agent-api", title: "Agent API", description: "Complete Agent constructor and method reference.", content: [] },
      { slug: "protocol-spec", title: "Protocol Spec", description: "Core entity definitions and validation rules.", content: [] },
      { slug: "architecture", title: "Architecture", description: "Full layered design and module boundaries.", content: [] },
    ],
  },
];

// Flatten for lookup
export function getAllDocSlugs(): string[] {
  return docSidebar.flatMap((section) => section.items.map((item) => item.slug));
}

export function getDocBySlug(slug: string): DocItem | undefined {
  for (const section of docSidebar) {
    const found = section.items.find((item) => item.slug === slug);
    if (found) return found;
  }
  return undefined;
}

// ─── PAGE CONTENT ───────────────────────────────────────────

export const docPages: Record<string, DocContentBlock[]> = {

  // ────────────────────────────────────────────────────────────
  // GETTING STARTED
  // ────────────────────────────────────────────────────────────

  introduction: [
    { type: "text", value: "MTP (Model Tool Protocol) is an agent orchestration framework that separates language model reasoning from environment execution." },
    { type: "text", value: "Instead of letting models call tools directly, MTP requires them to produce structured execution plans. The runtime validates, resolves dependencies, and executes tools under strict policy control." },
    { type: "text", value: "MTP is not a chatbot framework. It is a protocol for building execution systems where AI models plan and tools execute." },
    { type: "heading", value: "Key Principles" },
    { type: "list", value: "", items: [
      "Separation of concerns — models reason, runtime executes.",
      "Structured plans — DAG-based execution with dependency resolution.",
      "Policy enforcement — Allow, Ask, and Deny rules before any tool runs.",
      "Provider agnostic — 12+ model adapters with a unified interface.",
      "Production-ready — session persistence, streaming events, and transport primitives.",
    ]},
    { type: "heading", value: "Two Layers" },
    { type: "text", value: "MTP has two explicit layers:" },
    { type: "list", value: "", items: [
      "MTP Protocol — protocol entities and execution semantics (ToolSpec, ToolCall, ExecutionPlan).",
      "MTP Agent SDK — framework, runtime, providers, toolkits, and transports built on top of the protocol.",
    ]},
    { type: "callout", calloutType: "note", value: "MCP support is an interoperability surface, not the core project identity. MTP can serve tools over MCP but is not limited to it." },
  ],

  quickstart: [
    { type: "text", value: "This guide gets you from zero to a running agent in under 3 minutes." },
    { type: "heading", value: "1. Install" },
    { type: "code", language: "bash", value: `$ pip install mtpx

# With Groq provider and dotenv
$ pip install "mtpx[groq,dotenv]"` },
    { type: "heading", value: "2. Configure API Key" },
    { type: "text", value: "Create a .env file in your project root:" },
    { type: "code", language: "env", value: `GROQ_API_KEY=your_groq_api_key_here` },
    { type: "heading", value: "3. Build Your First Agent" },
    { type: "code", language: "python", label: "my_agent.py", value: `from mtp import Agent
from mtp.providers import Groq
from mtp.toolkits import CalculatorToolkit, FileToolkit

Agent.load_dotenv_if_available()

tools = Agent.ToolRegistry()
tools.register_toolkit_loader("calculator", CalculatorToolkit())
tools.register_toolkit_loader("file", FileToolkit(base_dir="."))

provider = Groq(model="llama-3.3-70b-versatile")

agent = Agent.MTPAgent(
    provider=provider,
    tools=tools,
    instructions="Use tools when needed. Be concise.",
    debug_mode=True,
)

result = agent.run("Calculate 25*4+10 and list files.", max_rounds=4)
print(result)`, output: `[MTP] Round 1: plan with 2 batches
✓ calculator.multiply(a=25, b=4) → 100
✓ calculator.add(a=100, b=10) → 110
✓ file.list_files(path=".") → ["app.py", ".env", "config.json"]

The result of 25*4+10 is 110. Current files: app.py, .env, config.json.`, outputLabel: "Output" },
    { type: "heading", value: "4. What Happens" },
    { type: "list", value: "", items: [
      "Messages and tool schemas are sent to the provider.",
      "Provider returns a tool execution plan (or direct text).",
      "Runtime validates the plan, resolves dependencies, and executes tools.",
      "Tool results are added back to conversation context.",
      "Loop continues until the provider returns final text.",
    ]},
    { type: "callout", calloutType: "tip", value: "Use agent.print_response(..., stream=True, stream_events=True) to see runtime events in your terminal." },
  ],

  installation: [
    { type: "text", value: "MTPX is available on PyPI. Python 3.10+ is required." },
    { type: "heading", value: "From PyPI (Recommended)" },
    { type: "code", language: "bash", value: `$ pip install mtpx` },
    { type: "heading", value: "Common Extras" },
    { type: "code", language: "bash", value: `# Groq + dotenv
$ pip install "mtpx[groq,dotenv]"

# OpenAI + Anthropic
$ pip install "mtpx[openai,anthropic,dotenv]"

# Web scraping toolkits
$ pip install "mtpx[toolkits-web]"

# Database session stores
$ pip install "mtpx[stores-db]"

# Everything
$ pip install "mtpx[all]"` },
    { type: "heading", value: "From Source" },
    { type: "code", language: "bash", value: `$ git clone https://github.com/yourusername/MTP.git
$ cd MTP
$ python -m venv .venv
$ .venv\\Scripts\\activate   # Windows
$ pip install -e .` },
    { type: "heading", value: "Verify" },
    { type: "code", language: "bash", value: `$ python -c "import mtp; print(f'MTPX {mtp.__version__} installed')"` },
    { type: "heading", value: "CLI Bootstrap (Optional)" },
    { type: "text", value: "Scaffold a starter project instead of building manually:" },
    { type: "code", language: "bash", value: `$ mtp new my_agent --template minimal
$ cd my_agent
$ mtp run` },
  ],

  // ────────────────────────────────────────────────────────────
  // CORE CONCEPTS
  // ────────────────────────────────────────────────────────────

  agents: [
    { type: "text", value: "An Agent is the orchestration loop that connects a language model (provider) to a set of tools (registry). It manages the multi-round cycle of planning, executing, and returning results." },
    { type: "heading", value: "The Agent Loop" },
    { type: "list", value: "", items: [
      "Gather available tool specifications from the registry.",
      "Send messages + tool schemas to the provider adapter.",
      "Provider returns either direct text or a tool execution plan.",
      "Runtime executes the plan (parallel or sequential batches).",
      "Tool results are appended to conversation history.",
      "Loop repeats until provider returns final text or max_rounds is reached.",
    ]},
    { type: "heading", value: "Two Agent Classes" },
    { type: "text", value: "Agent is the low-level orchestration engine. MTPAgent is a high-level ergonomic wrapper with a simplified API:" },
    { type: "code", language: "python", value: `from mtp import Agent
from mtp.providers import Groq

# MTPAgent — recommended for most use cases
agent = Agent.MTPAgent(
    provider=Groq(model="llama-3.3-70b-versatile"),
    tools=registry,
    instructions="Be concise and use tools.",
)

# Simple API
result = agent.run("Summarize the project files.", max_rounds=4)

# Streaming
agent.print_response("List files.", stream=True, stream_events=True)` },
    { type: "heading", value: "Orchestration Mode" },
    { type: "text", value: "Agents can delegate tasks to member agents. Set mode=\"orchestration\" and pass a members dict:" },
    { type: "code", language: "python", value: `orchestrator = Agent.MTPAgent(
    provider=provider,
    tools=registry,
    mode="orchestration",
    members={"researcher": research_agent, "coder": code_agent},
)` },
    { type: "text", value: "Each member is exposed as a tool: agent.member.<name>. The orchestrator can delegate sub-tasks to specialized agents." },
    { type: "callout", calloutType: "note", value: "MTP injects internal system instructions automatically. Your instructions= are layered on top." },
  ],

  "execution-plans": [
    { type: "text", value: "Execution Plans are the core abstraction that separates MTP from direct tool-calling frameworks. Instead of models invoking tools immediately, they produce structured plans that the runtime validates and executes." },
    { type: "heading", value: "Plan Structure" },
    { type: "text", value: "An ExecutionPlan contains ordered batches. Each batch contains tool calls that can run in parallel or sequential mode." },
    { type: "code", language: "json", value: `{
  "batches": [
    {
      "mode": "parallel",
      "calls": [
        {
          "id": "call_1",
          "name": "file.read_file",
          "arguments": { "path": "config.json" }
        },
        {
          "id": "call_2",
          "name": "calculator.multiply",
          "arguments": { "a": 25, "b": 4 }
        }
      ]
    },
    {
      "mode": "sequential",
      "calls": [
        {
          "id": "call_3",
          "name": "file.write_file",
          "arguments": {
            "path": "result.txt",
            "content": { "$ref": "call_2" }
          },
          "depends_on": ["call_2"]
        }
      ]
    }
  ]
}` },
    { type: "heading", value: "Dependency Resolution" },
    { type: "text", value: "Tool calls can reference outputs of previous calls using {\"$ref\": \"<call_id>\"}. The runtime resolves these references before execution." },
    { type: "heading", value: "Validation Rules" },
    { type: "list", value: "", items: [
      "No duplicate ToolCall IDs within a plan.",
      "Every dependency must reference an existing call ID.",
      "Dependency graph must be acyclic (no circular references).",
    ]},
    { type: "callout", calloutType: "tip", value: "Enable strict_dependency_mode=True to reject plans where the model guesses intermediate values instead of using $ref." },
  ],

  "tool-registry": [
    { type: "text", value: "The ToolRegistry is the central store for all tools available to an agent. It manages registration, lazy loading, caching, and spec discovery." },
    { type: "heading", value: "Registering Tools" },
    { type: "code", language: "python", value: `from mtp import Agent
from mtp.toolkits import CalculatorToolkit, FileToolkit

tools = Agent.ToolRegistry()
tools.register_toolkit_loader("calculator", CalculatorToolkit())
tools.register_toolkit_loader("file", FileToolkit(base_dir="."))` },
    { type: "heading", value: "Lazy Loading" },
    { type: "text", value: "Toolkit handlers load only when a matching tool is called. Tool names are discoverable through loader spec preview so providers can see all available tools before any handler loads." },
    { type: "heading", value: "Dynamic Mutations" },
    { type: "text", value: "You can add or replace tools after agent initialization:" },
    { type: "code", language: "python", value: `agent.add_tool(my_custom_tool)
agent.set_tools([tool_a, tool_b, tool_c])` },
    { type: "callout", calloutType: "note", value: "Tool names follow the pattern toolkit.action (e.g. file.read_file, calculator.add)." },
  ],

  runtime: [
    { type: "text", value: "The Runtime Engine is the single source of truth for plan execution. It handles validation, dependency resolution, caching, policy enforcement, and batch execution." },
    { type: "heading", value: "Execution Flow" },
    { type: "list", value: "", items: [
      "Validate the execution plan (duplicate IDs, missing deps, cycles).",
      "Execute batches in order.",
      "For sequential batches — execute calls in listed order.",
      "For parallel batches — execute all calls concurrently.",
      "Resolve $ref argument references to prior call outputs.",
      "Enforce risk policy before each tool invocation.",
      "Apply cache lookup/store if TTL is configured.",
    ]},
    { type: "heading", value: "Caching" },
    { type: "text", value: "Tools can declare cache_ttl_seconds in their ToolSpec. The runtime caches results and returns cached outputs for identical calls within the TTL window." },
    { type: "heading", value: "Policy Enforcement" },
    { type: "text", value: "Before executing any tool, the runtime checks the risk policy. Tools marked as destructive require explicit approval through the approval_handler callback." },
    { type: "heading", value: "Control Flow Exceptions" },
    { type: "code", language: "python", value: `from mtp.exceptions import RetryAgentRun, StopAgentRun

# Inside a tool handler:
raise RetryAgentRun("Input format was wrong, try again.")
raise StopAgentRun("Manual review required.")` },
    { type: "text", value: "RetryAgentRun injects feedback and asks the model to replan. StopAgentRun pauses the current run and returns with paused=True." },
  ],

  // ────────────────────────────────────────────────────────────
  // FEATURES
  // ────────────────────────────────────────────────────────────

  providers: [
    { type: "text", value: "MTP provides a standardized ProviderAdapter interface. Each adapter translates model-specific API responses into MTP's AgentAction format. This means you can swap models without changing your agent code." },
    { type: "heading", value: "Supported Providers" },
    { type: "table", value: "", headers: ["Provider", "Alias", "SDK Extra"], rows: [
      ["Groq", "Groq", "mtpx[groq]"],
      ["OpenAI", "OpenAI", "mtpx[openai]"],
      ["Anthropic", "Anthropic", "mtpx[anthropic]"],
      ["Google Gemini", "Gemini", "mtpx[gemini]"],
      ["OpenRouter", "OpenRouter", "mtpx[openrouter]"],
      ["Cohere", "Cohere", "mtpx[cohere]"],
      ["Mistral", "Mistral", "mtpx[mistral]"],
      ["DeepSeek", "DeepSeek", "mtpx[deepseek]"],
      ["SambaNova", "SambaNova", "mtpx[sambanova]"],
      ["Cerebras", "Cerebras", "mtpx[cerebras]"],
      ["Together AI", "TogetherAI", "mtpx[togetherai]"],
      ["Fireworks AI", "FireworksAI", "mtpx[fireworksai]"],
    ]},
    { type: "heading", value: "Usage" },
    { type: "code", language: "python", value: `from mtp.providers import Groq

# Alias-style (recommended)
provider = Groq(model="llama-3.3-70b-versatile")

# Explicit class
from mtp.providers import GroqToolCallingProvider
provider = GroqToolCallingProvider(model="llama-3.3-70b-versatile")` },
    { type: "heading", value: "Capability Contract" },
    { type: "text", value: "Each provider exposes a capabilities() method declaring supported features: tool calling, parallel calls, input modalities, streaming support, and structured output quality." },
    { type: "text", value: "The Agent enforces these capabilities at runtime. Unsupported features fail fast with clear errors instead of silently producing incorrect results." },
    { type: "heading", value: "Adding a Custom Provider" },
    { type: "code", language: "python", value: `from mtp.agent import AgentAction, ProviderAdapter

class CustomProvider(ProviderAdapter):
    def next_action(self, messages, tools) -> AgentAction:
        ...

    def finalize(self, messages, tool_results) -> str:
        ...` },
  ],

  toolkits: [
    { type: "text", value: "MTP ships with local toolkits that require no API keys, plus optional web toolkits for research agents." },
    { type: "heading", value: "Local Toolkits" },
    { type: "table", value: "", headers: ["Toolkit", "Tools", "Notes"], rows: [
      ["calculator", "add, subtract, multiply, divide, sqrt", "Basic arithmetic"],
      ["file", "list_files, read_file, write_file, search_in_files", "Constrained to base_dir"],
      ["python", "run_code, run_file", "Isolated subprocess mode by default"],
      ["shell", "run_command", "Allowlisted commands only"],
    ]},
    { type: "heading", value: "Register All Local Toolkits" },
    { type: "code", language: "python", value: `from mtp import Agent

registry = Agent.ToolRegistry()
Agent.register_local_toolkits(registry, base_dir=".")` },
    { type: "heading", value: "Web Toolkits (Optional)" },
    { type: "code", language: "bash", value: `pip install "mtpx[toolkits-web]"` },
    { type: "table", value: "", headers: ["Toolkit", "Tool", "Dependency"], rows: [
      ["wikipedia", "search_wikipedia", "wikipedia"],
      ["website", "read_url", "requests, beautifulsoup4"],
      ["newspaper4k", "read_article", "newspaper4k, lxml_html_clean"],
      ["crawl4ai", "web_crawler", "crawl4ai"],
    ]},
    { type: "callout", calloutType: "note", value: "Web toolkits are lazily loaded. You can register them without installing packages — the first call will fail with an install hint if dependencies are missing." },
  ],

  "creating-tools": [
    { type: "text", value: "Build custom tools from plain Python functions. MTP infers parameter schemas from type hints automatically." },
    { type: "heading", value: "1. Define a Tool" },
    { type: "code", language: "python", value: `from mtp import Agent

@Agent.mtp_tool(
    description="Add two integers.",
    risk_level=Agent.ToolRiskLevel.READ_ONLY,
    cache_ttl_seconds=60,
)
def add(a: int, b: int) -> int:
    return a + b` },
    { type: "heading", value: "2. Create a Toolkit" },
    { type: "code", language: "python", value: `toolkit = Agent.toolkit_from_functions("math", add)
# Produces tool name: math.add` },
    { type: "heading", value: "3. Register and Use" },
    { type: "code", language: "python", value: `registry = Agent.ToolRegistry()
registry.register_toolkit_loader("math", toolkit)

agent = Agent.MTPAgent(provider=provider, tools=registry)
print(agent.run("Use math.add with a=20 and b=22"))` },
    { type: "heading", value: "Best Practices" },
    { type: "list", value: "", items: [
      "Write precise descriptions. The model reads them.",
      "Keep parameter names explicit and stable.",
      "Mark risk_level correctly: read_only, write, or destructive.",
      "For side effects, prefer explicit user confirmation via policy.",
    ]},
  ],

  policies: [
    { type: "text", value: "MTP enforces risk-aware execution policies before any tool runs. This gives you explicit control over what actions an AI agent can take." },
    { type: "heading", value: "Risk Levels" },
    { type: "list", value: "", items: [
      "read_only — safe data retrieval. Default policy: allow.",
      "write — creates or modifies data. Default policy: allow.",
      "destructive — deletes data or runs irreversible operations. Default policy: ask.",
    ]},
    { type: "heading", value: "Policy Decisions" },
    { type: "list", value: "", items: [
      "allow — execute immediately without user input.",
      "ask — pause execution and request human approval via approval_handler.",
      "deny — block execution entirely. Tool result is marked as skipped.",
    ]},
    { type: "heading", value: "Custom Policy" },
    { type: "text", value: "Customize the risk policy when creating a ToolRegistry to enforce stricter rules for production environments." },
    { type: "callout", calloutType: "warning", value: "Tools marked as destructive with the default policy will pause execution and wait for approval. Always configure an approval_handler for production agents." },
  ],

  persistence: [
    { type: "text", value: "MTP session persistence is opt-in and provider-agnostic. When configured, conversation history and run metadata are saved and restored across process restarts." },
    { type: "heading", value: "Supported Stores" },
    { type: "table", value: "", headers: ["Store", "Use Case", "Install"], rows: [
      ["JsonSessionStore", "Local dev and demos", "Built-in"],
      ["PostgresSessionStore", "Production, multi-process", 'mtpx[store-postgres]'],
      ["MySQLSessionStore", "Production, multi-process", 'mtpx[store-mysql]'],
    ]},
    { type: "heading", value: "Usage" },
    { type: "code", language: "python", value: `from mtp import Agent, JsonSessionStore

store = JsonSessionStore(db_path="tmp/mtp_json_db")

agent = Agent.MTPAgent(
    provider=provider,
    tools=tools,
    session_store=store,
)

agent.run("Remember: codename is Atlas.", session_id="s1", user_id="u1")
agent.run("What is the codename?", session_id="s1", user_id="u1")` },
    { type: "heading", value: "Stored Data" },
    { type: "list", value: "", items: [
      "session_id, user_id, metadata",
      "messages — full conversation history",
      "runs — run_id, input, final_text, tool call count, timestamps",
    ]},
    { type: "callout", calloutType: "tip", value: "Without session_store, behavior is unchanged — MTP uses in-memory message history only." },
  ],

  streaming: [
    { type: "text", value: "MTP exposes a provider-agnostic event stream. All providers map into the same event shape, so frontend code can consume one stable model regardless of the underlying LLM." },
    { type: "heading", value: "Usage" },
    { type: "code", language: "python", value: `# Human-readable terminal logs
agent.print_response(prompt, stream=True, stream_events=True)

# Raw JSON lines
agent.print_response(prompt, stream=True, stream_events=True, event_format="json")

# Iterator API
for event in agent.run_events(prompt, max_rounds=5):
    print(event["type"])` },
    { type: "heading", value: "Event Types" },
    { type: "table", value: "", headers: ["Event", "Description"], rows: [
      ["run_started", "Run begins with user message and available tools"],
      ["round_started", "New reasoning round begins"],
      ["plan_received", "Model returned an execution plan"],
      ["batch_started", "Tool batch begins execution"],
      ["tool_started", "Individual tool execution begins"],
      ["tool_finished", "Tool completed with output or error"],
      ["text_chunk", "Streamed text fragment from model"],
      ["run_completed", "Run finished with final text"],
      ["run_paused", "Run paused by StopAgentRun"],
      ["run_cancelled", "Run cancelled by user"],
      ["run_failed", "Run failed with error"],
    ]},
    { type: "heading", value: "Debug Verbosity" },
    { type: "text", value: "Set debug_mode=True for full trace including plans, batch starts, tool payloads, and metrics blocks. Set debug_mode=False for concise lifecycle logs." },
  ],

  // ────────────────────────────────────────────────────────────
  // ADVANCED
  // ────────────────────────────────────────────────────────────

  "mcp-interop": [
    { type: "text", value: "MTP includes an experimental MCP-compatible JSON-RPC adapter built on top of the ToolRegistry. This allows MTP tools to be served over standard MCP transports without changing any tool code." },
    { type: "heading", value: "Supported MCP Methods" },
    { type: "table", value: "", headers: ["Category", "Methods"], rows: [
      ["Lifecycle", "initialize, notifications/initialized"],
      ["Core", "ping, tools/list, tools/call"],
      ["Resources", "resources/list, resources/read"],
      ["Prompts", "prompts/list, prompts/get"],
      ["Progress", "notifications/progress, $/cancelRequest, notifications/cancelled"],
    ]},
    { type: "heading", value: "Example: MCP HTTP Server" },
    { type: "code", language: "python", value: `from mtp import MCPHTTPTransportServer, MCPJsonRpcServer, ToolRegistry, ToolSpec

tools = ToolRegistry()
tools.register_tool(ToolSpec(name="calc.add", description="Add"), lambda a, b: a + b)

server = MCPJsonRpcServer(tools=tools)
transport = MCPHTTPTransportServer("127.0.0.1", 8081, server)
transport.start()` },
    { type: "heading", value: "Auth Plugin" },
    { type: "text", value: "MCPJsonRpcServer supports pluggable auth via auth_provider=. Auth decisions include allowed, error codes, and WWW-Authenticate headers for OAuth-style flows." },
    { type: "callout", calloutType: "note", value: "MCP support is an interoperability surface. MTP's own agent loop, policy engine, and session persistence operate independently of MCP." },
  ],

  transport: [
    { type: "text", value: "MTP provides transport primitives shared across the ecosystem. All use MessageEnvelope JSON serialization." },
    { type: "heading", value: "Transports" },
    { type: "table", value: "", headers: ["Transport", "Protocol", "Dependency"], rows: [
      ["run_stdio_transport", "Line-delimited JSON over stdin/stdout", "Built-in"],
      ["HTTPTransportServer", "POST endpoint with JSON envelopes", "Built-in"],
      ["WebSocketTransportServer", "Async bidirectional envelopes", "websockets"],
    ]},
    { type: "heading", value: "HTTP Transport Example" },
    { type: "code", language: "python", value: `from mtp.transport import HTTPTransportServer
from mtp.schema import MessageEnvelope

def handler(env: MessageEnvelope, cancel_checker=None) -> MessageEnvelope:
    return MessageEnvelope.create(kind="ok", payload={"echo": env.kind})

server = HTTPTransportServer("127.0.0.1", 8080, handler)
server.start()` },
    { type: "heading", value: "Cancellation" },
    { type: "text", value: "All transports support cancel control messages (kind=\"cancel\" or kind=\"cancel_request\"). The transport records the cancelled request ID and provides a cancel_checker callback to handlers." },
  ],

  autoresearch: [
    { type: "text", value: "Autoresearch mode enables persistent execution where the model keeps working until it explicitly terminates. Direct assistant text is treated as intermediate progress, not completion." },
    { type: "heading", value: "Usage" },
    { type: "code", language: "python", value: `agent = Agent.MTPAgent(
    provider=provider,
    tools=tools,
    autoresearch=True,
    research_instructions=(
        "Keep working until requirements are fully met. "
        "Call agent.terminate with reason and summary only when complete."
    ),
)

agent.print_response(
    "Research and summarize the latest findings.",
    max_rounds=12,
    stream=True,
    stream_events=True,
)` },
    { type: "heading", value: "How It Works" },
    { type: "list", value: "", items: [
      "MTP injects an internal agent.terminate(reason, summary) tool.",
      "Direct text from the model is treated as intermediate progress.",
      "Completion only happens via agent.terminate, user cancellation, or max_rounds limit.",
      "Event stream includes run_terminated before run_completed.",
    ]},
    { type: "callout", calloutType: "tip", value: "Autoresearch is ideal for long-running tasks like code generation, research, and data analysis where the model needs multiple rounds to verify its work." },
  ],

  cli: [
    { type: "text", value: "MTP provides a first-party CLI for scaffolding projects, running agents, and validating environments." },
    { type: "heading", value: "Scaffold a Project" },
    { type: "code", language: "bash", value: `mtp new my_agent
mtp new my_server --template mcp-http
mtp new my_memory_agent --template session-json` },
    { type: "heading", value: "Run a Project" },
    { type: "code", language: "bash", value: `mtp run
mtp run --path ./my_agent
mtp run --path ./my_server --entry server.py` },
    { type: "heading", value: "Validate Environment" },
    { type: "code", language: "bash", value: `mtp doctor
mtp doctor --provider groq
mtp doctor --provider openai --provider anthropic` },
    { type: "text", value: "Checks Python version, dotenv availability, SDK imports, and API key environment variables." },
    { type: "heading", value: "List Providers" },
    { type: "code", language: "bash", value: `mtp providers list` },
    { type: "heading", value: "Interactive TUI" },
    { type: "code", language: "bash", value: `mtp tui
mtp tui --backend mtp-openai --openai-model gpt-5.4-mini` },
    { type: "text", value: "The TUI supports slash commands: /models, /backend, /model, /reasoning, /rounds, /autoresearch, /status, /exit." },
  ],

  // ────────────────────────────────────────────────────────────
  // REFERENCE
  // ────────────────────────────────────────────────────────────

  "agent-api": [
    { type: "text", value: "Complete reference for the Agent and MTPAgent classes." },
    { type: "heading", value: "Constructor Parameters" },
    { type: "code", language: "python", value: `Agent(
    provider: ProviderAdapter,
    tools: ToolRegistry | None = None,
    debug_mode: bool = False,
    strict_dependency_mode: bool = False,
    instructions: str | None = None,
    autoresearch: bool = False,
    research_instructions: str | None = None,
    session_store: SessionStore | None = None,
    mode: str = "standalone",   # standalone | member | orchestration
    members: dict[str, Agent] | None = None,
)` },
    { type: "heading", value: "Execution Methods" },
    { type: "table", value: "", headers: ["Method", "Returns", "Notes"], rows: [
      ["run(input)", "str", "Single-round execution"],
      ["arun(input)", "str", "Async single-round"],
      ["run_loop(input, max_rounds=5)", "str", "Multi-round with tool loops"],
      ["run_output(...)", "RunOutput", "Structured output with schema validation"],
      ["run_loop_stream(...)", "Iterator[str]", "Stream final text tokens"],
      ["run_loop_events(...)", "Iterator[dict]", "Stream structured events"],
    ]},
    { type: "heading", value: "RunOutput Fields" },
    { type: "list", value: "", items: [
      "run_id, input, final_text, messages, tool_results",
      "user_id, session_id, metadata",
      "cancelled, paused, pause_reason",
      "terminated, termination_reason",
      "total_tool_calls, output, output_validation_error",
    ]},
    { type: "heading", value: "Cancellation & Continuation" },
    { type: "code", language: "python", value: `agent.cancel_run(run_id)
agent.continue_run(run_output=previous_output)` },
  ],

  "protocol-spec": [
    { type: "text", value: "Draft v0.1.0 of the MTP protocol specification. Defines the in-process protocol model used by mtpx." },
    { type: "heading", value: "Core Entities" },
    { type: "heading", value: "ToolSpec" },
    { type: "list", value: "", items: [
      "name — stable tool identifier (toolkit.action recommended).",
      "description — model-facing description.",
      "input_schema — JSON schema for tool arguments.",
      "risk_level — read_only | write | destructive.",
      "cache_ttl_seconds — optional cache hint for runtime.",
    ]},
    { type: "heading", value: "ToolCall" },
    { type: "list", value: "", items: [
      "id — unique call identifier inside a plan.",
      "name — selected tool name.",
      "arguments — dict payload.",
      "depends_on — list of call IDs required before this call.",
    ]},
    { type: "heading", value: "ExecutionPlan" },
    { type: "list", value: "", items: [
      "batches — ordered list of ToolBatch (parallel or sequential).",
      "metadata — provider/planner metadata.",
    ]},
    { type: "heading", value: "ToolResult" },
    { type: "list", value: "", items: [
      "call_id, tool_name, output, success, error.",
      "cached — whether this was a cache hit.",
      "approval — policy decision used (allow/ask/deny).",
      "skipped — true when blocked by policy.",
    ]},
    { type: "heading", value: "MessageEnvelope" },
    { type: "list", value: "", items: [
      "mtp_version — protocol version.",
      "kind — message type.",
      "payload — message data.",
      "metadata — optional context.",
    ]},
  ],

  architecture: [
    { type: "text", value: "MTP is organized as a layered architecture with strict module boundaries." },
    { type: "heading", value: "Layers" },
    { type: "table", value: "", headers: ["Layer", "Module", "Responsibility"], rows: [
      ["1", "mtp.protocol", "Core entities: ToolSpec, ToolCall, ExecutionPlan, ToolResult"],
      ["2", "mtp.schema", "Protocol envelope (MessageEnvelope), plan validation"],
      ["3", "mtp.policy", "Risk-aware policy decisions (allow/ask/deny)"],
      ["4", "mtp.runtime", "Tool registry, lazy loading, caching, batch execution"],
      ["5", "mtp.agent", "Orchestration loop: plan → execute → return"],
      ["6", "mtp.providers", "12 model adapters with standard ProviderAdapter interface"],
      ["7", "mtp.toolkits", "Built-in local and web toolkits"],
      ["8", "mtp.transport", "Stdio, HTTP, WebSocket envelope transports"],
      ["9", "mtp.session_store", "JSON/PostgreSQL/MySQL session persistence"],
      ["10", "mtp.mcp", "MCP JSON-RPC adapter over ToolRegistry"],
    ]},
    { type: "heading", value: "Module Boundaries" },
    { type: "list", value: "", items: [
      "Providers convert model responses into AgentAction. They do not execute tools.",
      "Toolkits own tool specs and handlers. They avoid provider-specific assumptions.",
      "Runtime is the single source of truth for plan execution.",
      "Agent is the orchestration loop only. No provider-specific parsing logic.",
      "Transport handles message ingress/egress only. No business logic.",
      "MCP is a protocol adapter boundary (JSON-RPC in/out). It delegates to runtime.",
    ]},
    { type: "callout", calloutType: "note", value: "MTP protocol and MTP Agent SDK are distinct layers in the same project. MCP support is an interoperability capability, not the product identity." },
  ],

  // ────────────────────────────────────────────────────────────
  // COOKBOOK
  // ────────────────────────────────────────────────────────────

  "cookbook-calc-to-file": [
    { type: "text", value: "This recipe shows how to chain a calculation result into a file write using MTP's dependency resolution. The model generates a plan where the second tool call references the output of the first." },
    { type: "heading", value: "Problem" },
    { type: "text", value: "You want the agent to compute a value and then save that result to a file — without hardcoding the intermediate value." },
    { type: "heading", value: "Code" },
    { type: "code", language: "python", label: "agent_calc_write.py", value: `from mtp import Agent
from mtp.providers import Groq
from mtp.toolkits import CalculatorToolkit, FileToolkit

Agent.load_dotenv_if_available()

tools = Agent.ToolRegistry()
tools.register_toolkit_loader("calculator", CalculatorToolkit())
tools.register_toolkit_loader("file", FileToolkit(base_dir="."))

agent = Agent.MTPAgent(
    provider=Groq(model="llama-3.3-70b-versatile"),
    tools=tools,
    instructions="Use tools. Be concise.",
    strict_dependency_mode=True,
)

result = agent.run(
    "Calculate (25 * 4) + 10 and save the result to output.txt",
    max_rounds=4,
)
print(result)`, output: `[MTP] Plan received: 2 batches
[MTP] Batch 1 (parallel): calculator.multiply(a=25, b=4)
[MTP] Batch 2 (sequential): calculator.add(a=$ref:call_1, b=10) → file.write_file(path="output.txt", content=$ref:call_2)

✓ calculator.multiply → 100
✓ calculator.add → 110
✓ file.write_file → wrote 3 bytes to output.txt

The result of (25 × 4) + 10 = 110 has been saved to output.txt.`, outputLabel: "Result" },
    { type: "heading", value: "How It Works" },
    { type: "list", value: "", items: [
      "The model generates an ExecutionPlan with dependency references ($ref).",
      "Batch 1 runs calculator.multiply first.",
      "Batch 2 resolves $ref:call_1 to 100, then passes 110 to file.write_file.",
      "strict_dependency_mode ensures the model cannot guess intermediate values.",
    ]},
    { type: "callout", calloutType: "tip", value: "Enable debug_mode=True to see the full execution plan JSON in your terminal." },
  ],

  "cookbook-multi-step": [
    { type: "text", value: "This recipe demonstrates multi-step tool chaining where output from one toolkit flows into another through DAG dependencies." },
    { type: "heading", value: "Problem" },
    { type: "text", value: "You want to read a config file, extract a value, compute something with it, and write the result back — all in one agent call." },
    { type: "heading", value: "Execution Plan" },
    { type: "text", value: "The model generates this plan automatically:" },
    { type: "code", language: "json", label: "Generated ExecutionPlan", value: `{
  "batches": [
    {
      "mode": "parallel",
      "calls": [
        {
          "id": "read_cfg",
          "name": "file.read_file",
          "arguments": { "path": "config.json" }
        }
      ]
    },
    {
      "mode": "sequential",
      "calls": [
        {
          "id": "compute",
          "name": "calculator.multiply",
          "arguments": { "a": { "$ref": "read_cfg" }, "b": 2 },
          "depends_on": ["read_cfg"]
        },
        {
          "id": "save",
          "name": "file.write_file",
          "arguments": {
            "path": "doubled.txt",
            "content": { "$ref": "compute" }
          },
          "depends_on": ["compute"]
        }
      ]
    }
  ]
}`, output: `✓ file.read_file("config.json") → "42"
✓ calculator.multiply(42, 2) → 84
✓ file.write_file("doubled.txt", "84") → wrote 2 bytes`, outputLabel: "Execution trace" },
    { type: "heading", value: "Key Concepts" },
    { type: "list", value: "", items: [
      "Batch 1 runs independently — reads the config file.",
      "Batch 2 is sequential — each call depends on the previous.",
      "$ref values are resolved by the runtime before the tool handler executes.",
      "The model never sees raw intermediate values — only structured references.",
    ]},
    { type: "callout", calloutType: "note", value: "Validation rules enforce: no duplicate IDs, no missing deps, and no cycles. Invalid plans are rejected before any tool runs." },
  ],

  "cookbook-safe-agent": [
    { type: "text", value: "This recipe shows how MTP's policy engine prevents destructive actions and requires human approval for risky operations." },
    { type: "heading", value: "Problem" },
    { type: "text", value: "You want the agent to read files freely but block any file deletion or shell command unless a human approves." },
    { type: "heading", value: "Code" },
    { type: "code", language: "python", label: "safe_agent.py", value: `from mtp import Agent
from mtp.providers import Groq
from mtp.toolkits import FileToolkit, ShellToolkit

tools = Agent.ToolRegistry()
tools.register_toolkit_loader("file", FileToolkit(base_dir="."))
tools.register_toolkit_loader("shell", ShellToolkit(base_dir="."))

def approval_handler(tool_name, arguments, risk_level):
    print(f"⚠️  APPROVAL NEEDED: {tool_name}")
    print(f"   Risk: {risk_level}")
    print(f"   Args: {arguments}")
    answer = input("   Allow? (y/n): ")
    return answer.lower() == "y"

agent = Agent.MTPAgent(
    provider=Groq(model="llama-3.3-70b-versatile"),
    tools=tools,
    instructions="Use tools as needed.",
)

# The runtime will pause before destructive tools
result = agent.run(
    "Delete the temp folder and list remaining files",
    max_rounds=4,
)
print(result)`, output: `[MTP] Plan: shell.run_command(command="rm -rf temp/") → file.list_files(path=".")

⚠️  APPROVAL NEEDED: shell.run_command
   Risk: destructive
   Args: {"command": "rm -rf temp/"}
   Allow? (y/n): n

[MTP] tool shell.run_command DENIED by policy (skipped)
✓ file.list_files → ["config.json", "output.txt", "temp/"]

I was unable to delete the temp folder as the operation was denied.
The current files are: config.json, output.txt, temp/`, outputLabel: "Result (denied)" },
    { type: "heading", value: "Risk Level Reference" },
    { type: "table", value: "", headers: ["Level", "Default Policy", "Examples"], rows: [
      ["read_only", "allow", "file.read_file, calculator.add"],
      ["write", "allow", "file.write_file"],
      ["destructive", "ask", "shell.run_command"],
    ]},
    { type: "callout", calloutType: "warning", value: "In production, always set an approval_handler. Without one, destructive tools will be blocked by default." },
  ],

  "cookbook-memory": [
    { type: "text", value: "This recipe demonstrates session persistence — how an agent can remember context across separate invocations." },
    { type: "heading", value: "Problem" },
    { type: "text", value: "You want to tell the agent something in one run, then ask about it in a completely separate run (even after process restart)." },
    { type: "heading", value: "Code" },
    { type: "code", language: "python", label: "memory_agent.py", value: `from mtp import Agent, JsonSessionStore
from mtp.providers import OpenAI

store = JsonSessionStore(db_path="tmp/mtp_sessions")

agent = Agent.MTPAgent(
    provider=OpenAI(model="gpt-4o"),
    tools=Agent.ToolRegistry(),
    session_store=store,
)

# Run 1: Store information
agent.run(
    "Remember: the project codename is Atlas and the deadline is March 15.",
    session_id="project-chat",
    user_id="dev-1",
)

# Run 2: Retrieve information (can be after restart)
result = agent.run(
    "What is the project codename and when is the deadline?",
    session_id="project-chat",
    user_id="dev-1",
)
print(result)`, output: `The project codename is Atlas and the deadline is March 15.`, outputLabel: "Result (Run 2)" },
    { type: "heading", value: "How It Works" },
    { type: "list", value: "", items: [
      "JsonSessionStore saves conversation history to disk as JSON files.",
      "Each run with the same session_id loads prior messages automatically.",
      "Works across process restarts — the store is file-based.",
      "PostgresSessionStore and MySQLSessionStore work the same way for production.",
    ]},
    { type: "heading", value: "Stored Data" },
    { type: "code", language: "json", label: "Session record structure", value: `{
  "session_id": "project-chat",
  "user_id": "dev-1",
  "messages": [
    {"role": "user", "content": "Remember: the project codename is Atlas..."},
    {"role": "assistant", "content": "Got it! I'll remember that..."},
    {"role": "user", "content": "What is the project codename..."},
    {"role": "assistant", "content": "The project codename is Atlas..."}
  ],
  "runs": [
    {"run_id": "run_abc123", "input": "Remember: ...", "total_tool_calls": 0},
    {"run_id": "run_def456", "input": "What is ...", "total_tool_calls": 0}
  ]
}` },
    { type: "callout", calloutType: "tip", value: "Use JsonSessionStore for development and PostgresSessionStore for production. The API is identical — just swap the store constructor." },
  ],
};
