export interface DocSection {
  title: string;
  items: DocItem[];
  collapsible?: boolean;
}

export interface DocItem {
  slug: string;
  title: string;
  description: string;
  content: DocContentBlock[];
}

export interface DocContentBlock {
  type:
    | "text" | "code" | "heading" | "subheading" | "list" | "callout"
    | "table" | "custom-providers-grid" | "tabs" | "architecture"
    | "api-method" | "divider";
  value?: string;
  language?: string;
  calloutType?: "note" | "tip" | "warning" | "danger";
  items?: string[];
  rows?: string[][];
  headers?: string[];
  tabs?: { label: string; language: string; code: string }[];
  fields?: { name: string; type: string; required: boolean; description: string }[];
  returns?: string;
}

export const docSidebar: DocSection[] = [
  {
    title: "Introduction",
    items: [
      { slug: "introduction", title: "Introduction", description: "What MTPX is and why it exists.", content: [] },
      { slug: "quickstart", title: "Quickstart", description: "Running your first agent in under 3 minutes.", content: [] },
      { slug: "installation", title: "Installation", description: "Install from PyPI or source.", content: [] },
    ],
  },
  {
    title: "Core Concepts",
    collapsible: true,
    items: [
      { slug: "planning", title: "Planning", description: "How models produce structured execution plans.", content: [] },
      { slug: "dag-execution", title: "DAG Execution", description: "Directed acyclic graph-based tool orchestration.", content: [] },
      { slug: "runtime-engine", title: "Runtime Engine", description: "Validation, policy enforcement, and execution.", content: [] },
      { slug: "tool-registry", title: "Tool Registry", description: "How tools are registered, discovered, and invoked.", content: [] },
      { slug: "risk-policies", title: "Risk Policies", description: "Allow, Ask, and Deny execution controls.", content: [] },
      { slug: "stateful-sessions", title: "Stateful Sessions", description: "Persistent agent memory across invocations.", content: [] },
      { slug: "human-approval", title: "Human Approval Gates", description: "Interrupt execution for human decision.", content: [] },
      { slug: "event-streaming", title: "Event Streaming", description: "Real-time execution event contracts.", content: [] },
      { slug: "provider-abstraction", title: "Provider Abstraction", description: "Unified interface across all LLM providers.", content: [] },
      { slug: "execution-lifecycle", title: "Execution Lifecycle", description: "Full lifecycle of an agent invocation.", content: [] },
    ],
  },
  {
    title: "Architecture",
    collapsible: true,
    items: [
      { slug: "execution-flow", title: "Execution Flow", description: "End-to-end walkthrough of agent execution.", content: [] },
      { slug: "planner-vs-runtime", title: "Planner vs Runtime", description: "The strict separation of reasoning and action.", content: [] },
      { slug: "dag-resolution", title: "DAG Resolution", description: "Dependency resolution and parallel scheduling.", content: [] },
      { slug: "state-persistence", title: "State Persistence", description: "How sessions are serialized and restored.", content: [] },
      { slug: "tool-sandboxing", title: "Tool Sandboxing", description: "Execution isolation and resource limits.", content: [] },
      { slug: "event-bus", title: "Event Bus", description: "Internal event routing and subscriber model.", content: [] },
      { slug: "provider-layer", title: "Provider Layer", description: "Adapter pattern for LLM provider integration.", content: [] },
    ],
  },
  {
    title: "SDK Reference",
    collapsible: true,
    items: [
      { slug: "sdk-agent", title: "Agent", description: "The primary orchestration class.", content: [] },
      { slug: "sdk-runtime", title: "Runtime", description: "The execution engine interface.", content: [] },
      { slug: "sdk-tool", title: "Tool", description: "Tool registration and schema definition.", content: [] },
      { slug: "sdk-session", title: "Session", description: "Session management and state persistence.", content: [] },
      { slug: "sdk-policies", title: "Policies", description: "Policy configuration and enforcement.", content: [] },
      { slug: "sdk-events", title: "Events", description: "Event types and subscription model.", content: [] },
      { slug: "sdk-providers", title: "Providers", description: "Provider adapter reference.", content: [] },
      { slug: "sdk-storage", title: "Storage", description: "Backend storage adapters.", content: [] },
    ],
  },
  {
    title: "Providers",
    collapsible: true,
    items: [
      { slug: "providers", title: "Overview", description: "All supported model providers.", content: [] },
      { slug: "provider-openai", title: "OpenAI", description: "GPT-4o, o1, and function-calling support.", content: [] },
      { slug: "provider-anthropic", title: "Anthropic", description: "Claude 3.5 and extended context support.", content: [] },
      { slug: "provider-gemini", title: "Gemini", description: "Google Gemini 1.5 Pro and Flash.", content: [] },
      { slug: "provider-groq", title: "Groq", description: "Ultra-fast inference with LPU hardware.", content: [] },
      { slug: "provider-ollama", title: "Ollama", description: "Local open-source model execution.", content: [] },
      { slug: "provider-custom", title: "Custom Providers", description: "Implement the ProviderAdapter interface.", content: [] },
    ],
  },
  {
    title: "Safety",
    collapsible: true,
    items: [
      { slug: "safety-risk-levels", title: "Risk Levels", description: "READ, WRITE, and DESTRUCTIVE classification.", content: [] },
      { slug: "safety-approval", title: "Approval Gates", description: "Human-in-the-loop execution patterns.", content: [] },
      { slug: "safety-sandboxing", title: "Sandboxing", description: "Process isolation and resource enforcement.", content: [] },
      { slug: "safety-permissions", title: "Tool Permissions", description: "Granular tool access control.", content: [] },
      { slug: "safety-audit", title: "Audit Logs", description: "Tamper-evident execution audit trail.", content: [] },
    ],
  },
  {
    title: "Observability",
    collapsible: true,
    items: [
      { slug: "obs-streaming", title: "Event Streaming", description: "Real-time execution events and subscribers.", content: [] },
      { slug: "obs-tui", title: "TUI Monitoring", description: "Terminal UI for live agent supervision.", content: [] },
      { slug: "obs-logs", title: "Runtime Logs", description: "Structured logging and log levels.", content: [] },
      { slug: "obs-traces", title: "Execution Traces", description: "Full per-invocation execution traces.", content: [] },
      { slug: "obs-dag-viz", title: "DAG Visualization", description: "Visual execution graph rendering.", content: [] },
    ],
  },
  {
    title: "Examples",
    collapsible: true,
    items: [
      { slug: "example-research", title: "Research Agent", description: "Multi-step web research pipeline.", content: [] },
      { slug: "example-coding", title: "Coding Agent", description: "Code generation and test execution.", content: [] },
      { slug: "example-filesystem", title: "File System Agent", description: "Safe file I/O with destructive guards.", content: [] },
      { slug: "example-fallback", title: "Multi-Provider Fallback", description: "Automatic failover across providers.", content: [] },
      { slug: "example-approval", title: "Human Approval Workflow", description: "Interrupt-and-resume patterns.", content: [] },
      { slug: "example-enterprise", title: "Enterprise Audit Pipeline", description: "Full audit trail production setup.", content: [] },
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

export function getSectionForSlug(slug: string): DocSection | undefined {
  return docSidebar.find((section) => section.items.some((item) => item.slug === slug));
}

export const docPages: Record<string, DocContentBlock[]> = {

  // ─── GETTING STARTED ────────────────────────────────────────

  introduction: [
    { type: "text", value: "MTPX (Model Tool Protocol Extended) is a production-grade control plane and orchestration framework for AI agents. It provides a deterministic execution environment that separates reasoning from action, ensuring that agentic workflows are safe, observable, and auditable at scale." },
    
    { type: "heading", value: "Overview" },
    { type: "text", value: "Traditional agent frameworks often rely on a tight loop where the LLM directly invokes tools. This approach introduces non-determinism and security risks, as the model has direct agency over the execution environment. MTPX replaces this with a protocol-first architecture where the model acts as a **Planner**, generating a structured Execution Plan (DAG), which is then processed by a **Runtime Engine** that enforces strict validation and safety policies." },

    { type: "heading", value: "Why It Exists" },
    { type: "text", value: "As AI agents move from experimental demos to production systems, three critical engineering challenges emerge:" },
    { type: "list", value: "", items: [
      "Reliability — Large Language Models are prone to hallucinating tool arguments or execution order. MTPX validates plans before a single line of tool code runs.",
      "Safety — Direct tool access allows for 'agentic escapes'. MTPX intercepts every call at the runtime level to enforce granular risk-based policies (Allow/Ask/Deny).",
      "Observability — Understanding why an agent took a specific action is difficult in black-box loops. MTPX streams structured events for every phase of the lifecycle."
    ]},

    { type: "heading", value: "How It Works" },
    { type: "text", value: "MTPX operates on a 6-stage execution protocol designed to minimize the model's direct influence over the host system while maximizing its planning capabilities." },
    { type: "list", value: "", items: [
      "Planning — The model receives tool specifications and generates a Directed Acyclic Graph (DAG) of intended actions.",
      "Validation — The Runtime checks the DAG for cycles, duplicate IDs, and parameter schema compliance.",
      "Policy Enforcement — The Policy Engine evaluates each tool call against its risk profile (READ/WRITE/DESTRUCTIVE).",
      "Resolution — The Runtime resolves dependencies between tool calls, injecting results from previous steps into subsequent arguments.",
      "Execution — Tools are executed in parallel or sequential batches based on the DAG's structure.",
      "Finalization — The model receives the complete execution trace to produce a final, grounded response."
    ]},

    { type: "heading", value: "Architecture Flow" },
    { type: "architecture", value: `[ Planner (LLM) ]
       ↓
[ Execution DAG ]
       ↓
[ Plan Validator ] ──▶ (Cycle Detection & Schema Check)
       ↓
[ Policy Engine ]  ──▶ (Risk Level Interception)
       ↓
[ Runtime Engine ] ──▶ (Dependency Wiring)
       ↓
[ Tool Executor ]  ──▶ (Parallel/Sequential Dispatch)
       ↓
[ Event Stream ]   ──▶ (Real-time Observability)` },

    { type: "heading", value: "Code Example" },
    { type: "text", value: "A typical MTPX agent setup involves defining a Provider, registering Toolkits, and initializing the MTPAgent orchestrator." },
    { type: "code", language: "python", value: `from mtp import Agent
from mtp.providers import Anthropic
from mtp.toolkits import FileToolkit, SearchToolkit

# 1. Initialize the reasoning engine
provider = Anthropic(model="claude-3-5-sonnet-latest")

# 2. Define the capability registry
tools = Agent.ToolRegistry()
tools.register_toolkit_loader("fs", FileToolkit(base_dir="./sandbox"))
tools.register_toolkit_loader("web", SearchToolkit())

# 3. Initialize the control plane
agent = Agent.MTPAgent(
    provider=provider,
    tools=tools,
    debug_mode=True,
    strict_dependency_mode=True
)

# 4. Execute a deterministic run
response = agent.run("Find the latest MTPX release and save the summary to report.md")` },

    { type: "heading", value: "Runtime Behavior" },
    { type: "text", value: "During execution, MTPX maintains a strict internal state machine. If a model generates a plan with a circular dependency (e.g., Tool A depends on Tool B, which depends on Tool A), the Runtime will raise a `PlanValidationError` before execution starts. This 'dry-run' validation ensures that destructive tools are never reached if the overall plan is logically flawed." },

    { type: "heading", value: "Best Practices" },
    { type: "list", value: "", items: [
      "Granular Toolkits — Group related tools into small, logical toolkits to reduce context window bloat.",
      "Risk Tagging — Explicitly tag tools with DESTRUCTIVE risk levels to trigger mandatory human-in-the-loop (HITL) approval gates.",
      "Lazy Loading — Use ToolkitLoaders to ensure heavy tool dependencies are only initialized when the model actually plans to use them."
    ]},

    { type: "heading", value: "Common Mistakes" },
    { type: "list", value: "", items: [
      "Treating MTPX as a Chatbot — MTPX is an execution engine. Avoid using it for simple conversational tasks where tool calling isn't required.",
      "Oversized Plans — Avoid allowing the model to plan more than 10-15 steps in a single round. Prefer multi-round execution for long-running workflows.",
      "Ignoring Policies — Failing to configure a PolicyEngine in production environments defaults to a permissive state, negating the framework's safety benefits."
    ]},

    { type: "heading", value: "Related Concepts" },
    { type: "table", headers: ["Concept", "Description"], rows: [
      ["Execution DAG", "The structured representation of tool calls and their inter-dependencies."],
      ["Provider Adapter", "The normalization layer that translates model-specific outputs into MTPX plans."],
      ["Risk Level", "The classification (READ/WRITE/DESTRUCTIVE) assigned to every tool spec."],
      ["Event Bus", "The internal routing system for streaming runtime events to external observers."]
    ]},
    { type: "callout", calloutType: "note", value: "MTPX is designed for infrastructure engineers. If you are looking for a simple chatbot UI, this is likely the wrong tool. MTPX is for building resilient, production-grade agentic systems." }
  ],

  quickstart: [
    { type: "text", value: "This guide provides a high-velocity path to deploying your first MTPX agent. You will initialize a reasoning provider (Groq), register a mathematical toolkit, and execute a deterministic tool-calling run in under two minutes." },

    { type: "heading", value: "Overview" },
    { type: "text", value: "The goal of this quickstart is to demonstrate the core MTPX lifecycle: translating a natural language request into a validated execution plan and executing it safely using a local runtime." },

    { type: "heading", value: "Why It Exists" },
    { type: "text", value: "Modern agentic systems require a 'sanity check' baseline. The Quickstart serves as a minimal verifiable example (MVE) to ensure your environment, model provider, and tool registry are correctly wired before moving to complex multi-agent orchestration." },

    { type: "heading", value: "How It Works" },
    { type: "text", value: "Setting up an MTPX agent follows a standardized four-step workflow:" },
    { type: "list", value: "", items: [
      "Dependency Management — Install the base package and provider-specific extras.",
      "Provider Configuration — Initialize the reasoning adapter (e.g., Llama 3 via Groq).",
      "Toolkit Registration — Expose local functions to the agent via the ToolRegistry.",
      "Runtime Execution — Dispatch the user request to the MTPAgent loop."
    ]},

    { type: "heading", value: "Architecture Flow" },
    { type: "architecture", value: `[ User Query ] ──▶ [ MTPAgent ]
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
    [ Groq Provider ]     [ Tool Registry ]
     (Reasoning/DAG)       (Calculator Handler)
             │                   │
             └─────────┬─────────┘
                       ▼
               [ MTPX Runtime ]
             (Execution & Validation)
                       ↓
               [ Final Answer ]` },

    { type: "heading", value: "Code Example" },
    { type: "text", value: "Ensure you have a `GROQ_API_KEY` in your environment. This example uses the built-in CalculatorToolkit for local math operations." },
    { type: "code", language: "python", value: `import os
from mtp import Agent
from mtp.providers import Groq
from mtp.toolkits import CalculatorToolkit

# 1. Load environment and initialize Provider
os.environ["GROQ_API_KEY"] = "your_key_here"
provider = Groq(model="llama-3.3-70b-versatile")

# 2. Setup Tool Registry with a namespace
tools = Agent.ToolRegistry()
tools.register_toolkit_loader("math", CalculatorToolkit())

# 3. Initialize the Agent Control Plane
agent = Agent.MTPAgent(
    provider=provider,
    tools=tools,
    instructions="Use the 'math' toolkit for all calculations. Be precise."
)

# 4. Run the deterministic loop
response = agent.run("Calculate (125 * 4) + 15.3 and tell me the result.")
print(f"Agent Response: {response}")` },

    { type: "heading", value: "Runtime Behavior" },
    { type: "text", value: "When `agent.run()` is called, the runtime first requests an ExecutionPlan from Groq. The plan is received as a JSON DAG. The MTPX Runtime then validates that the 'math.calculate' tool is actually registered and that the arguments match the expected schema before the local Python function is invoked." },

    { type: "heading", value: "Best Practices" },
    { type: "list", value: "", items: [
      "Environment Isolation — Use virtual environments and `.env` files for managing provider credentials.",
      "Namespace Precision — Always use clear prefixes (like 'math.' or 'fs.') when registering toolkits to prevent naming collisions.",
      "Model Pinning — Production agents should pin specific model versions (e.g., 'llama-3.3-70b-versatile') rather than generic aliases to ensure stable planning behavior."
    ]},

    { type: "heading", value: "Common Mistakes" },
    { type: "list", value: "", items: [
      "Missing Provider Extras — Running Groq without `pip install \"mtpx[groq]\"` will result in a ModuleNotFoundError.",
      "Incomplete Instructions — Models often default to 'internal math' rather than using tools unless explicitly instructed to use the registry.",
      "Unset API Keys — The runtime will fail immediately if the provider's required environment variables are not detected."
    ]},

    { type: "heading", value: "Related Concepts" },
    { type: "table", headers: ["Concept", "Related Slug"], rows: [
      ["Provider Normalization", "provider-abstraction"],
      ["Tool Schemas", "tool-registry"],
      ["Risk Assessment", "risk-policies"],
      ["Event Logs", "event-streaming"]
    ]},
    { type: "callout", calloutType: "tip", value: "Use `agent.print_response(prompt, stream=True)` to watch the runtime validate and execute the plan in real-time." }
  ],

  installation: [
    { type: "text", value: "MTPX is distributed as a modular Python package via PyPI. It is designed with a 'lean core' philosophy, allowing engineers to install only the specific provider adapters and storage backends required for their specific infrastructure." },

    { type: "heading", value: "Overview" },
    { type: "text", value: "Installing MTPX involves selecting a base version and optionally layering 'extras' for specific LLM providers (OpenAI, Groq, etc.) or persistence layers (Postgres, Redis). This ensures your production containers remain lightweight and free of unnecessary dependencies." },

    { type: "heading", value: "Why It Exists" },
    { type: "text", value: "Enterprise agent deployments often face 'dependency hell' when frameworks bundle every possible SDK. MTPX solves this by using Python's entry-points and optional dependencies, ensuring that the core runtime remains stable regardless of which providers you choose to integrate." },

    { type: "heading", value: "How It Works" },
    { type: "text", value: "The installation process is categorized into three tiers:" },
    { type: "list", value: "", items: [
      "Core Runtime — The base `mtpx` package containing the protocol, runtime engine, and policy enforcement layers.",
      "Provider Adapters — Optional extras that bundle vendor-specific SDKs (e.g., `openai`, `anthropic`).",
      "Infrastructure Extras — Optional components for database connectivity and advanced observability."
    ]},

    { type: "heading", value: "Architecture Flow" },
    { type: "architecture", value: `[ PyPI Registry ]
       │
       ▼
[ Local Environment ]
       │
       ├─▶ ( mtpx ) ───────────▶ [ Core Logic & Protocol ]
       │
       ├─▶ ( mtpx[openai] ) ───▶ [ OpenAI SDK + Adapter ]
       │
       └─▶ ( mtpx[stores] ) ───▶ [ SQLAlchemy + Drivers ]` },

    { type: "heading", value: "Code Examples" },
    { type: "text", value: "Use standard pip syntax to install the core package and necessary extras. For production, we recommend pinning versions." },
    { type: "tabs", value: "", tabs: [
      { label: "Core Only", language: "bash", code: "pip install mtpx" },
      { label: "With Providers", language: "bash", code: "pip install \"mtpx[openai,groq,anthropic]\"" },
      { label: "Full Suite", language: "bash", code: "pip install \"mtpx[all]\"" }
    ]},
    { type: "text", value: "After installation, verify your environment using the built-in diagnostic tool:" },
    { type: "code", language: "bash", value: "mtp doctor" },

    { type: "heading", value: "Runtime Behavior" },
    { type: "text", value: "When an extra is installed, MTPX registers the corresponding module in the internal `ProviderRegistry`. At runtime, the `MTPAgent` uses lazy-import logic to verify that the required SDK (e.g., `google-generativeai`) is present in the environment before attempting to initialize a provider. If an extra is missing, the runtime will raise a descriptive `AdapterDependencyError` with the specific pip command needed to resolve it." },

    { type: "heading", value: "Best Practices" },
    { type: "list", value: "", items: [
      "Virtual Environments — Always install MTPX within a `venv` or `conda` environment to prevent collision with system-level packages.",
      "Lock Files — Use `requirements.txt` or `poetry.lock` to ensure identical dependency trees across dev, staging, and production.",
      "Environment Variables — Use `.env` files and `python-dotenv` to manage API keys. Never hardcode credentials in your agent scripts."
    ]},

    { type: "heading", value: "Common Mistakes" },
    { type: "list", value: "", items: [
      "Missing Quotes — Failing to use quotes in `pip install \"mtpx[extras]\"` can lead to shell parsing errors in Zsh or Bash.",
      "Global Installation — Installing globally can lead to permission issues and 'module not found' errors when running as a non-privileged user.",
      "Circular Dependencies — Attempting to manually install multiple conflicting versions of LLM SDKs alongside MTPX. Always let MTPX resolve its own extra versions."
    ]},

    { type: "heading", value: "Related Concepts" },
    { type: "table", headers: ["Component", "Purpose"], rows: [
      ["mtp doctor", "Diagnostic CLI for validating environment health."],
      ["Provider Registry", "Internal map of available reasoning adapters."],
      ["Dependency Isolation", "The principle of keeping core runtime free of vendor SDKs."]
    ]}
  ],

  // ─── CORE CONCEPTS ──────────────────────────────────────────

  planning: [
    { type: "text", value: "Planning is the foundational reasoning phase where the LLM translates a natural language objective into a structured, executable blueprint. In MTPX, this blueprint is a Directed Acyclic Graph (DAG) that defines which tools to call, in what order, and how data should flow between them." },

    { type: "heading", value: "Overview" },
    { type: "text", value: "Unlike 'chain-of-thought' agents that execute tools one-by-one in an ad-hoc loop, MTPX forces the model to generate a comprehensive Execution Plan upfront. This structured approach allows the system to validate the logic, optimize for parallel execution, and enforce safety boundaries before any tool handler is invoked." },

    { type: "heading", value: "Why It Exists" },
    { type: "text", value: "Traditional agentic loops suffer from 'execution drift', where the model loses track of its original goal after a few tool interactions. By separating Planning from Execution, MTPX ensures:" },
    { type: "list", value: "", items: [
      "Determinism — The agent's intent is fully declared and inspectable before execution.",
      "Parallelism — Independent tasks are automatically identified and scheduled for concurrent execution.",
      "Safety — The system can reject plans that violate security constraints (e.g., trying to write to a protected file system) without ever running code."
    ]},

    { type: "heading", value: "How It Works" },
    { type: "text", value: "The planning lifecycle involves three primary stages:" },
    { type: "list", value: "", items: [
      "Context Assembly — The ToolRegistry provides a unified schema (ToolSpec) of all available capabilities to the model.",
      "Graph Synthesis — The model generates a JSON structure containing 'batches'. Each batch contains one or more tool calls.",
      "Dependency Wiring — The model uses the `$ref` syntax to indicate that the output of one tool call (e.g., `call_1`) should be used as an input argument for another (e.g., `call_2`)."
    ]},

    { type: "heading", value: "Architecture Flow" },
    { type: "architecture", value: `[ User Query ]
       │
[ System Prompt + Tool Specs ]
       │
[ LLM Reasoning ]
       │
[ Structured Output (JSON) ]
       │
       ▼
{
  "batches": [
    {
      "calls": [ { "id": "c1", "name": "web.search", ... } ]
    },
    {
      "calls": [ { "id": "c2", "name": "fs.write", "args": { "content": "$ref:c1" } } ]
    }
  ]
}` },

    { type: "heading", value: "Code Examples" },
    { type: "text", value: "MTPX providers use structured output patterns to ensure the model adheres to the `ExecutionPlan` schema. Here is how a plan looks internally when generated by a reasoning adapter." },
    { type: "code", language: "json", value: `{
  "batches": [
    {
      "execution_mode": "parallel",
      "calls": [
        { "id": "get_weather", "name": "weather.get", "arguments": { "city": "London" } },
        { "id": "get_time", "name": "clock.now", "arguments": {} }
      ]
    },
    {
      "execution_mode": "sequential",
      "calls": [
        { 
          "id": "format_msg", 
          "name": "utils.format", 
          "arguments": { 
            "weather": { "$ref": "get_weather" },
            "time": { "$ref": "get_time" }
          } 
        }
      ]
    }
  ]
}` },

    { type: "heading", value: "Runtime Behavior" },
    { type: "text", value: "When the Provider Adapter receives a plan, the MTPX Runtime performs a topological sort on the graph. This identifies the 'batches' that can be safely parallelized. If the model references a `$ref` that doesn't exist, or creates a cycle (A depends on B, B depends on A), the runtime raises a `CyclicDependencyError`. This ensures the execution engine never enters an infinite loop or an undefined state." },

    { type: "heading", value: "Best Practices" },
    { type: "list", value: "", items: [
      "Atomic Tooling — Design tools to do one thing well. This gives the planner more flexibility to build complex graphs.",
      "Explicit $ref Usage — Ensure the model uses unique, descriptive IDs for tool calls to make dependency tracking easier for both the model and the human auditor.",
      "Plan Depth Limits — Configure `max_rounds` to prevent the model from planning excessively deep recursions in a single session."
    ]},

    { type: "heading", value: "Common Mistakes" },
    { type: "list", value: "", items: [
      "Implicit Dependencies — Expecting a tool to have access to previous results without using the `$ref` syntax. MTPX is stateless between calls unless explicitly wired.",
      "ID Collisions — Reusing the same `id` for different tool calls within the same plan, which confuses the dependency resolver.",
      "Orphaned References — Referencing the output of a tool call that is in the same parallel batch (and thus hasn't completed yet)."
    ]},

    { type: "heading", value: "Related Concepts" },
    { type: "table", headers: ["Term", "Definition"], rows: [
      ["DAG", "Directed Acyclic Graph; the underlying data structure of an MTPX plan."],
      ["Topological Sort", "The algorithm used to determine execution order based on dependencies."],
      ["Grounded Reasoning", "The process of ensuring the model only plans using available, registered tools."]
    ]}
  ],

  "dag-execution": [
    { type: "text", value: "DAG (Directed Acyclic Graph) Execution is the process of translating a static execution plan into a dynamic sequence of parallel and sequential tool invocations. MTPX optimizes for throughput by identifying independent tasks that can be dispatched concurrently while strictly enforcing data dependencies." },

    { type: "heading", value: "Overview" },
    { type: "text", value: "Once a plan is validated, the MTPX Runtime treats each tool call as a node in a graph. Edges are created whenever a tool uses a `$ref` to depend on another's output. The execution engine then walks this graph to schedule tasks efficiently." },

    { type: "heading", value: "Why It Exists" },
    { type: "text", value: "Sequential execution is the primary bottleneck for complex agentic workflows. By using a DAG-based approach, MTPX achieves:" },
    { type: "list", value: "", items: [
      "Optimal Latency — Independent tools (e.g., searching two different sources) are executed in parallel.",
      "Data Integrity — Tools that depend on previous results are guaranteed to receive resolved, validated data.",
      "Checkpointing — The graph structure allows the runtime to pause and resume execution at specific node boundaries."
    ]},

    { type: "heading", value: "How It Works" },
    { type: "text", value: "The DAG execution lifecycle follows a 4-step pipeline:" },
    { type: "list", value: "", items: [
      "Topological Sorting — The runtime calculates a linear ordering of nodes that respects all dependencies.",
      "Batch Generation — Nodes with zero incoming dependencies are grouped into parallel 'execution waves'.",
      "Asynchronous Dispatch — Each wave is dispatched using non-blocking I/O (e.g., `asyncio.gather` in Python).",
      "Result Injection — As tools complete, their outputs are injected into the 'Context Store' for downstream nodes."
    ]},

    { type: "heading", value: "Architecture Flow" },
    { type: "architecture", value: `[ Validated Plan ]
       │
[ Graph Builder ] ──▶ (Build Adjacency List)
       │
[ Task Sorter ]   ──▶ (Identify Wave 1, Wave 2, ...)
       │
[ Execution Bus ]
       │
   ┌───┴───┐
   ▼       ▼
[ Tool A ] [ Tool B ]  (Parallel Wave)
   │       │
   └───┬───┘
       ▼
   [ Tool C ]          (Sequential Dependent)` },

    { type: "heading", value: "Code Examples" },
    { type: "text", value: "The MTPX Runtime handles graph scheduling automatically. You only need to define the dependency-aware plan." },
    { type: "code", language: "python", value: `from mtp.runtime import DAGExecutor

# Internal representation of a multi-batch execution
executor = DAGExecutor(plan={
    "batches": [
        {
            "mode": "parallel",
            "calls": [
                {"id": "search_1", "name": "web.search", "args": {"q": "MTPX core"}},
                {"id": "search_2", "name": "web.search", "args": {"q": "MTPX docs"}}
            ]
        },
        {
            "mode": "sequential",
            "calls": [
                {"id": "summary", "name": "nlp.summarize", "args": {"docs": ["$ref:search_1", "$ref:search_2"]}}
            ]
        }
    ]
})

# Executes using optimal concurrency
results = await executor.execute_async()` },

    { type: "heading", value: "Runtime Behavior" },
    { type: "text", value: "If a tool within a parallel batch fails, MTPX enters a 'halt-on-error' state by default. It stops the dispatch of subsequent waves while allowing already running tools in the current wave to complete. This prevents the system from entering a half-executed state with missing dependencies. Detailed error traces are streamed to the Event Bus for debugging." },

    { type: "heading", value: "Best Practices" },
    { type: "list", value: "", items: [
      "Handler Idempotency — Ensure tool handlers can be safely retried, as the DAG executor might re-run nodes during recovery.",
      "Non-Blocking I/O — Always use `async` tool definitions for network-bound tasks to maximize the benefits of parallel batches.",
      "Granular Error Handling — Return structured error objects from tools rather than raising raw exceptions to allow the planner to decide on fallbacks."
    ]},

    { type: "heading", value: "Common Mistakes" },
    { type: "list", value: "", items: [
      "Implicit Ordering — Assuming Tool A runs before Tool B when they are in the same parallel batch without an explicit dependency.",
      "Blocking the Loop — Using `time.sleep()` or synchronous requests inside a tool handler, which stalls the entire DAG executor.",
      "Deadlock References — Creating a plan where Tool A references an ID that is only generated in a later, dependent batch."
    ]},

    { type: "heading", value: "Related Concepts" },
    { type: "table", headers: ["Term", "Context"], rows: [
      ["Topological Sort", "The ordering algorithm ensuring dependency compliance."],
      ["Execution Wave", "A group of independent tool calls dispatched concurrently."],
      ["Context Store", "The temporary runtime memory holding tool outputs for reference."]
    ]}
  ],

  "runtime-engine": [
    { type: "text", value: "The Runtime Engine is the core state machine of MTPX. It acts as the 'Control Plane' that orchestrates the entire agent lifecycle, from plan validation to secure tool execution and event streaming." },

    { type: "heading", value: "Overview" },
    { type: "text", value: "While the Provider (LLM) handles the 'Reasoning', the Runtime handles the 'Doing'. It is a sandboxed environment that manages resources, enforces policies, and ensures that the agent's actions remain within defined engineering boundaries." },

    { type: "heading", value: "Why It Exists" },
    { type: "text", value: "A robust agent framework must be more than just a wrapper around an LLM. The MTPX Runtime exists to provide:" },
    { type: "list", value: "", items: [
      "Safety Gates — Intercepting destructive commands before they hit the OS or database.",
      "Observability — Providing a real-time 'black box' recorder for every agent action.",
      "Persistence — Maintaining state across multi-round conversations and complex workflows."
    ]},

    { type: "heading", value: "How It Works" },
    { type: "text", value: "The Runtime Engine operates as a continuous loop of state transitions:" },
    { type: "list", value: "", items: [
      "INGEST — Receives a raw ExecutionPlan from the Provider Adapter.",
      "VALIDATE — Checks the plan for structural integrity and cycle detection.",
      "AUTHORIZE — Consults the PolicyEngine for each tool call in the plan.",
      "DISPATCH — Handlers are invoked via the DAGExecutor.",
      "EMIT — Runtime events are pushed to the internal Event Bus."
    ]},

    { type: "heading", value: "Architecture Flow" },
    { type: "architecture", value: `[ Execution Plan ] ──▶ [ Runtime Controller ]
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
    [ Policy Engine ]                 [ State Manager ]
     (Allow/Deny/Ask)                  (Context & Logs)
            │                                 │
            └────────────────┬────────────────┘
                             ▼
                    [ DAG Executor ]
                             │
                             ▼
                    [ Tool Handlers ]` },

    { type: "heading", value: "Code Examples" },
    { type: "text", value: "You can initialize a custom Runtime to gain granular control over the execution environment and security policies." },
    { type: "code", language: "python", value: `from mtp.runtime import Runtime
from mtp.policies import StrictPolicy
from mtp.observers import ConsoleObserver

# Initialize the core engine
runtime = Runtime(
    policy_engine=StrictPolicy(), # Deny DESTRUCTIVE tools by default
    observers=[ConsoleObserver()], # Stream logs to terminal
    max_parallel_tasks=5
)

# The runtime is typically managed by the Agent, 
# but can be invoked directly for low-level orchestration.
results = runtime.execute(execution_plan)` },

    { type: "heading", value: "Runtime Behavior" },
    { type: "text", value: "The Runtime Engine is inherently asynchronous and event-driven. It maintains a 'Session Context' that tracks the outputs of every tool call. This context is used to resolve \`$ref\` variables in the plan. If the Runtime encounters a 'Human Approval' policy, it suspends execution, serializes the current state, and waits for an external signal before resuming." },

    { type: "heading", value: "Best Practices" },
    { type: "list", value: "", items: [
      "Strict Policies — Always use a restrictive policy engine in production to prevent unintended side effects.",
      "Event Listeners — Attach observers to the runtime to log agent behavior to external monitoring stacks (e.g., Datadog, LangSmith).",
      "Resource Limits — Configure \`max_execution_time\` to prevent runaway agent loops."
    ]},

    { type: "heading", value: "Common Mistakes" },
    { type: "list", value: "", items: [
      "State Leakage — Assuming that global variables in one tool will be available in another. Use the \`$ref\` system instead.",
      "Ignoring Events — Failing to monitor the event stream, which leads to 'silent failures' in complex plans.",
      "Oversized Batches — Dispatching too many parallel tasks that overwhelm the host system's CPU or network throughput."
    ]},

    { type: "heading", value: "Related Concepts" },
    { type: "table", headers: ["Component", "Role"], rows: [
      ["Policy Engine", "The security guard of the runtime."],
      ["Event Bus", "The real-time communication layer."],
      ["State Manager", "The 'short-term memory' of the execution session."]
    ]}
  ],

  "tool-registry": [
    { type: "text", value: "The Tool Registry is the centralized catalog of all capabilities available to the MTPX agent. It acts as the 'Interface Definition Layer', providing the LLM with the precise schemas and documentation it needs to plan effectively." },

    { type: "heading", value: "Overview" },
    { type: "text", value: "In MTPX, tools are not just functions; they are first-class resources with metadata, risk profiles, and versioning. The registry translates your Python code into standardized JSON Schemas that any supported LLM provider can understand." },

    { type: "heading", value: "Why It Exists" },
    { type: "text", value: "Directly exposing raw functions to an LLM is dangerous and brittle. The Tool Registry provides:" },
    { type: "list", value: "", items: [
      "Schema Abstraction — Automatic generation of OpenAI/Anthropic tool definitions from Python type hints.",
      "Capability Discovery — Dynamic loading of 'Toolkits' based on the agent's current objective.",
      "Risk Tagging — Assigning security levels (READ, WRITE, DESTRUCTIVE) to every tool for policy enforcement."
    ]},

    { type: "heading", value: "How It Works" },
    { type: "text", value: "The registration process follows a decorator-based pattern:" },
    { type: "list", value: "", items: [
      "Introspection — The registry inspects the function's docstring and type hints.",
      "Normalization — Arguments are converted into JSON Schema (Draft 7) specifications.",
      "Risk Assessment — Metadata is attached to define the tool's 'Blast Radius'.",
      "Indexing — The tool is indexed under a namespace (e.g., \`fs.write_file\`)."
    ]},

    { type: "heading", value: "Architecture Flow" },
    { type: "architecture", value: `[ Python Function ]
       │
[ @tool Decorator ] ──▶ (Inspect Hints & Docstring)
       │
[ ToolSpec Object ] ──▶ (Attach Risk & Version)
       │
[ Tool Registry ]   ──▶ (Namespace Mapping)
       │
[ Provider Adapter ]──▶ (Convert to Model-Specific JSON)` },

    { type: "heading", value: "Code Examples" },
    { type: "text", value: "Use the \`@tool\` decorator to register functions. Detailed docstrings are mandatory as they serve as the model's instructions." },
    { type: "code", language: "python", value: `from mtp import tool

@tool(risk_level="WRITE")
def save_report(filename: str, content: str) -> str:
    """
    Saves a generated report to the local filesystem.
    
    Args:
        filename: The name of the file (e.g. 'report.md').
        content: The string content to write.
    """
    with open(filename, "w") as f:
        f.write(content)
    return f"Successfully saved to {filename}"

# Registering a full toolkit
registry = Agent.ToolRegistry()
registry.register_tool(save_report)` },

    { type: "heading", value: "Runtime Behavior" },
    { type: "text", value: "When an agent starts, it fetches the 'Active Inventory' from the registry. If a tool requires complex dependencies (like a database driver), the registry can use 'Lazy Loading' to only import the relevant modules when the model actually attempts to include that tool in a plan. This keeps the agent's startup time extremely low." },

    { type: "heading", value: "Best Practices" },
    { type: "list", value: "", items: [
      "Type Hint Everything — Use Python type hints (e.g., \`list[str]\`, \`Optional[int]\`) to generate high-fidelity schemas.",
      "Verbose Docstrings — Treat docstrings as 'Model Documentation'. Explain edge cases and parameter constraints clearly.",
      "Namespace Partitioning — Group related tools into Toolkits (e.g., \`GitHubToolkit\`, \`CloudToolkit\`) for better organization."
    ]},

    { type: "heading", value: "Common Mistakes" },
    { type: "list", value: "", items: [
      "Vague Descriptions — 'Calculates stuff' is a bad docstring. 'Calculates the compound interest for a principal amount' is better.",
      "Missing Type Hints — Failing to use hints defaults the argument to \`Any\`, which often causes the model to hallucinate invalid input types.",
      "Overly Complex Inputs — Passing huge, nested dictionaries. Prefer flattening tool arguments for better model reliability."
    ]},

    { type: "heading", value: "Related Concepts" },
    { type: "table", headers: ["Component", "Description"], rows: [
      ["ToolSpec", "The standardized metadata object for a single capability."],
      ["Toolkit", "A logical grouping of related tools under a single namespace."],
      ["JSON Schema", "The underlying format used to communicate tool interfaces to LLMs."]
    ]}
  ],

  "risk-policies": [
    { type: "text", value: "Risk Policies are the security guardrails of the MTPX framework. They define the 'Blast Radius' of each tool and determine the level of authorization required before a tool can be executed by the runtime." },

    { type: "heading", value: "Overview" },
    { type: "text", value: "In MTPX, tools are not all created equal. A tool that reads a public documentation page has a different risk profile than a tool that drops a database table. Risk Policies allow engineers to classify capabilities and enforce strict execution gates (Allow, Ask, or Deny) based on these profiles." },

    { type: "heading", value: "Why It Exists" },
    { type: "text", value: "Autonomous agents are prone to 'prompt injection' and 'execution drift'. Without a policy engine, an agent could be manipulated into performing unintended destructive actions. Risk Policies provide:" },
    { type: "list", value: "", items: [
      "Least Privilege Execution — Ensuring agents only run what they absolutely need.",
      "Regulatory Compliance — Maintaining an audit trail of authorized high-risk actions.",
      "Safety Boundaries — Preventing 'destructive hallucinations' from hitting production systems."
    ]},

    { type: "heading", value: "How It Works" },
    { type: "text", value: "The MTPX Policy Engine evaluates tool calls using a 3-tier risk classification system:" },
    { type: "table", headers: ["Risk Level", "Description", "Typical Action"], rows: [
      ["READ_ONLY", "Safe, non-mutating data retrieval.", "ALLOW"],
      ["WRITE", "State-changing actions with limited scope.", "ASK (Default)"],
      ["DESTRUCTIVE", "Permanent or high-impact state changes.", "DENY (Default)"]
    ]},

    { type: "heading", value: "Architecture Flow" },
    { type: "architecture", value: `[ Tool Call Request ]
          │
[ Policy Evaluator ] ◀─── [ Active Policy (Strict/Permissive) ]
          │
    ┌─────┴─────┐
    ▼           ▼
[ AUTHORIZED ] [ INTERCEPTED ]
    │           │
    ▼           ├─▶ [ ASK ] ──▶ (Human Approval Gate)
[ EXECUTE ]     │
                └─▶ [ DENY ] ──▶ (Runtime Exception)` },

    { type: "heading", value: "Code Examples" },
    { type: "text", value: "Define a policy by inheriting from `BasePolicy` or using the built-in `StrictPolicy`. Attach it to the Runtime during initialization." },
    { type: "code", language: "python", value: `from mtp.policies import StrictPolicy, Action
from mtp import tool

# 1. Define a tool with a specific risk level
@tool(risk_level="DESTRUCTIVE")
def delete_user(user_id: str):
    """Irreversibly deletes a user from the primary database."""
    pass

# 2. Configure the policy engine
policy = StrictPolicy()
policy.add_override("delete_user", Action.ASK) # Override default DENY to ASK

# 3. Initialize Runtime with the policy
runtime = Runtime(policy_engine=policy)` },

    { type: "heading", value: "Runtime Behavior" },
    { type: "text", value: "When the Runtime encounters a tool call, it first resolves the tool's `risk_level` from the registry. The Policy Engine then compares this against the active session rules. If the result is `Action.ASK`, the runtime suspends the current DAG execution wave, emits a `HumanApprovalRequired` event, and waits for a signed authorization token before proceeding." },

    { type: "heading", value: "Best Practices" },
    { type: "list", value: "", items: [
      "Default to Strict — Always start with a `StrictPolicy` that denies all WRITE/DESTRUCTIVE actions unless explicitly overridden.",
      "Granular Overrides — Use per-tool overrides rather than globally allowing a risk level.",
      "Context-Aware Policies — Implement custom logic that allows 'WRITE' actions in staging but requires 'ASK' in production."
    ]},

    { type: "heading", value: "Common Mistakes" },
    { type: "list", value: "", items: [
      "Missing Risk Tags — Forgetting to tag a tool defaults it to 'READ_ONLY', which might create security holes.",
      "Permissive Overrides — Using `AllowAllPolicy` in production environments, which completely bypasses the safety framework.",
      "Ignoring Interceptions — Failing to handle the 'ASK' signal in the frontend, leading to 'stuck' agent runs."
    ]},

    { type: "heading", value: "Related Concepts" },
    { type: "table", headers: ["Component", "Description"], rows: [
      ["Human Approval", "The workflow for resolving 'ASK' policy signals."],
      ["Audit Logs", "The immutable record of policy evaluations."],
      ["Tool Registry", "Where risk levels are defined during registration."]
    ]}
  ],

  "stateful-sessions": [
    { type: "text", value: "Stateful Sessions enable MTPX agents to maintain continuity across complex, multi-round execution cycles. They provide the 'Short-Term Memory' required to track message history, execution traces, and resolved tool outputs." },

    { type: "heading", value: "Overview" },
    { type: "text", value: "In production, an agent request is rarely a single turn. MTPX uses a `SessionManager` to serialize the entire state of the execution environment (including the Context Store and Conversation History) into a persistent backend, allowing for asynchronous resumption and deep auditability." },

    { type: "heading", value: "Why It Exists" },
    { type: "text", value: "Stateless agents are limited to simple one-off tasks. Stateful Sessions allow for:" },
    { type: "list", value: "", items: [
      "Contextual Continuity — Remembering results from a tool call performed 10 minutes ago.",
      "Workflow Resumption — Pausing an agent for human approval and resuming it on a different server node.",
      "Analytical Tracing — Replaying exact execution sequences for debugging or compliance audits."
    ]},

    { type: "heading", value: "How It Works" },
    { type: "text", value: "MTPX Session Management follows a standardized lifecycle:" },
    { type: "list", value: "", items: [
      "Initialization — A unique `session_id` is assigned to the agent run.",
      "Snapshotting — After every execution wave, the Runtime takes a snapshot of the current state.",
      "Serialization — The snapshot is converted into a vendor-neutral format (JSON) by a Storage Adapter.",
      "Persistence — The data is written to the configured backend (Postgres, Redis, or Local Filesystem)."
    ]},

    { type: "heading", value: "Architecture Flow" },
    { type: "architecture", value: `[ Agent Instance ] ──▶ [ Session Manager ]
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
    [ Memory Layer ]                  [ Storage Adapter ]
     (Message History)                 (Snapshotting)
            │                                 │
            └────────────────┬────────────────┘
                             ▼
                    [ Persistent Store ]
                     (Postgres / Redis)` },

    { type: "heading", value: "Code Examples" },
    { type: "text", value: "Configure a session-aware agent by attaching a `SessionManager` with a specific storage adapter." },
    { type: "code", language: "python", value: `from mtp.sessions import SessionManager
from mtp.storage import PostgresAdapter

# 1. Initialize persistent storage
storage = PostgresAdapter(dsn="postgresql://user:pass@host/db")

# 2. Create the session manager
manager = SessionManager(storage=storage)

# 3. Run the agent within a specific session context
agent = Agent.MTPAgent(provider=p, tools=t, session_manager=manager)
response = agent.run("Resume the data analysis from yesterday.", session_id="user_123_sess_456")` },

    { type: "heading", value: "Runtime Behavior" },
    { type: "text", value: "When a `session_id` is provided, the Runtime first attempts to 'hydrate' its internal state from the Storage Adapter. This populates the `Context Store` with previous tool outputs, allowing the Planner to reference them immediately using the `$ref` syntax. If a session expires or is manually cleared, the Runtime defaults to a 'Cold Start' state." },

    { type: "heading", value: "Best Practices" },
    { type: "list", value: "", items: [
      "TTL Management — Configure Time-To-Live (TTL) policies for sessions to prevent database bloat.",
      "Selective Persistence — Only persist the data necessary for the agent's objective to minimize I/O overhead.",
      "Session Isolation — Ensure `session_id`s are securely generated and scoped to specific users to prevent data leakage."
    ]},

    { type: "heading", value: "Common Mistakes" },
    { type: "list", value: "", items: [
      "Giant Sessions — Storing multi-megabyte tool outputs in the session context, which slows down hydration.",
      "Race Conditions — Multiple agent instances attempting to write to the same `session_id` concurrently without locking.",
      "Incomplete Serialization — Using custom objects in tool outputs that are not JSON-serializable, causing storage failures."
    ]},

    { type: "heading", value: "Related Concepts" },
    { type: "table", headers: ["Term", "Description"], rows: [
      ["Hydration", "The process of loading session state into the active runtime."],
      ["Context Store", "The runtime memory holding tool results for a specific session."],
      ["Storage Adapter", "The layer that bridges MTPX and specific database backends."]
    ]}
  ],

  "human-approval": [
    { type: "text", value: "Human Approval Gates are the ultimate circuit-breakers in MTPX. They allow for an 'Interrupted Execution' flow where high-risk actions are paused until a human operator provides explicit validation." },

    { type: "heading", value: "Overview" },
    { type: "text", value: "MTPX treats 'Human-in-the-Loop' (HITL) not as an edge case, but as a core architectural pattern. When a tool call triggers an 'ASK' policy, the Runtime suspends the execution wave, preserves the session state, and waits for an external approval signal." },

    { type: "heading", value: "Why It Exists" },
    { type: "text", value: "Even the best models can make mistakes. Human Approval Gates provide:" },
    { type: "list", value: "", items: [
      "Blast Radius Control — Preventing irreversible actions (e.g., spending budget, deleting data).",
      "Model Correction — Allowing users to modify hallucinated tool arguments before execution.",
      "Trust & Transparency — Keeping humans 'in the loop' for sensitive enterprise workflows."
    ]},

    { type: "heading", value: "How It Works" },
    { type: "text", value: "The approval lifecycle is a 5-step transaction:" },
    { type: "list", value: "", items: [
      "Interception — The Policy Engine marks a tool call for approval.",
      "Suspension — The Runtime pauses and emits a `HumanApprovalRequired` event.",
      "Serialization — The entire pending execution wave is serialized to the session store.",
      "Resolution — An external agent (Human) provides an `Approve`, `Deny`, or `Revise` signal.",
      "Resumption — The Runtime hydrates the state and proceeds based on the human signal."
    ]},

    { type: "heading", value: "Architecture Flow" },
    { type: "architecture", value: `[ Runtime ] ──▶ [ Policy: ASK ]
                     │
             [ SUSPEND WAVE ]
                     │
             [ EMIT EVENT ] ──▶ (Approval TUI / Webhook)
                     │
             [ WAIT FOR SIGNAL ] ◀── (Human Input)
                     │
             [ RESUME WAVE ]` },

    { type: "heading", value: "Code Examples" },
    { type: "text", value: "Implement an approval handler to capture and resolve 'ASK' signals from the runtime." },
    { type: "code", language: "python", value: `from mtp.runtime import Runtime, ApprovalHandler

class CLIApprovalHandler(ApprovalHandler):
    def resolve(self, request):
        print(f"\\n[!] APPROVAL REQUIRED: {request.tool_name}")
        print(f"Arguments: {request.arguments}")
        choice = input("Approve? (y/n/r for revise): ")
        if choice == 'y': return request.approve()
        if choice == 'r': return request.revise(new_args={"path": "backup.txt"})
        return request.deny()

runtime = Runtime(approval_handler=CLIApprovalHandler())
agent = Agent.MTPAgent(runtime=runtime)` },

    { type: "heading", value: "Runtime Behavior" },
    { type: "text", value: "When an approval gate is hit, the Runtime does not 'block' the thread. Instead, it completes the current execution round, marks the session as 'INTERRUPTED', and returns control to the caller. The session remains in this state until a resolution is pushed. This allows the host application to handle approvals via webhooks, Slack messages, or dashboard UI elements." },

    { type: "heading", value: "Best Practices" },
    { type: "list", value: "", items: [
      "Detailed Context — Provide humans with enough context (e.g., 'Deleting file because...') to make informed decisions.",
      "Timeouts — Implement TTLs for approvals to prevent sessions from hanging indefinitely.",
      "Revision Logic — Allow users to edit tool arguments rather than just performing binary Approve/Deny actions."
    ]},

    { type: "heading", value: "Common Mistakes" },
    { type: "list", value: "", items: [
      "Blocking the Main Thread — Attempting to wait for human input inside a synchronous tool call handler.",
      "Lack of Serialization — Failing to persist the session before waiting for approval, leading to data loss on server restarts.",
      "Obscure Prompts — Failing to explain *why* the approval is needed in the first place."
    ]},

    { type: "heading", value: "Related Concepts" },
    { type: "table", headers: ["Component", "Role"], rows: [
      ["ApprovalRequest", "The metadata object containing tool details and state."],
      ["Session Persistence", "Required for long-lived approval workflows."],
      ["Action.ASK", "The policy signal that triggers the gate."]
    ]}
  ],

  "event-streaming": [
    { type: "text", value: "Event Streaming is the observability backbone of MTPX. It provides a real-time, structured stream of every internal state transition, allowing engineers to monitor agent behavior with millisecond precision." },

    { type: "heading", value: "Overview" },
    { type: "text", value: "MTPX doesn't just return a final answer. It emits a sequence of granular events (RunStarted, PlanReceived, ToolStarted, etc.) through an internal Event Bus. This enables a wide range of integration patterns, from live TUI monitoring to enterprise audit logging." },

    { type: "heading", value: "Why It Exists" },
    { type: "text", value: "Debugging AI agents in production is notoriously difficult without visibility into 'what happened between the prompt and the response'. Event Streaming provides:" },
    { type: "list", value: "", items: [
      "Live Observability — Watching an agent's planning and execution phase in real-time.",
      "Decoupled Integration — Feeding events into separate monitoring stacks without modifying agent code.",
      "Auditable Traces — Maintaining an immutable record of every tool invocation and result."
    ]},

    { type: "heading", value: "How It Works" },
    { type: "text", value: "The MTPX Event Bus uses a standard Pub/Sub model:" },
    { type: "list", value: "", items: [
      "Emission — Internal components (Planner, Runtime, ToolHandlers) push events to the bus.",
      "Categorization — Events are typed (e.g., `BATCH_STARTED`) and include structured payloads.",
      "Observation — 'Observers' subscribe to specific event types and process them asynchronously."
    ]},

    { type: "heading", value: "Architecture Flow" },
    { type: "architecture", value: `[ MTPX Component ] ──▶ [ Event Bus ]
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
    [ Console Observer ]            [ Webhook Observer ]
     (TUI Visualization)             (External Integration)
            │                               │
            ▼                               ▼
      [ User Terminal ]               [ Monitoring DB ]` },

    { type: "heading", value: "Code Examples" },
    { type: "text", value: "Attach multiple observers to an agent to stream events to different destinations simultaneously." },
    { type: "code", language: "python", value: `from mtp.observers import ConsoleObserver, LogFileObserver

# 1. Initialize observers
tui = ConsoleObserver(show_plans=True, show_results=True)
logger = LogFileObserver(path="agent.log")

# 2. Setup the agent with observers
agent = Agent.MTPAgent(
    provider=p, 
    tools=t, 
    observers=[tui, logger]
)

# 3. Events will stream automatically during execution
agent.run("Scan logs and summarize errors.")` },

    { type: "heading", value: "Runtime Behavior" },
    { type: "text", value: "Event emission is non-blocking. The MTPX Runtime ensures that 'heavy' observers (e.g., those writing to a slow database) do not stall the core execution loop. Every event includes a timestamp and a `round_id`, allowing you to reconstruct the exact timeline of a multi-round execution session." },

    { type: "heading", value: "Best Practices" },
    { type: "list", value: "", items: [
      "Structured Logging — Use the `JSONObserver` for production logs to make them easily searchable in stacks like ELK or Splunk.",
      "Selective Observation — In high-throughput systems, filter for 'CRITICAL' events only to reduce overhead.",
      "Real-time TUIs — Use the `ConsoleObserver` during development to understand the model's planning logic immediately."
    ]},

    { type: "heading", value: "Common Mistakes" },
    { type: "list", value: "", items: [
      "Blocking Observers — Implementing synchronous, blocking I/O in a custom observer handler.",
      "Event Overload — Subscribing to every single 'TEXT_CHUNK' event when only the final tool results are needed.",
      "Missing Round IDs — Forgetting to group events by their session and round IDs, making it impossible to reconstruct traces."
    ]},

    { type: "heading", value: "Related Concepts" },
    { type: "table", headers: ["Event Type", "Trigger"], rows: [
      ["PLAN_RECEIVED", "When the model returns its execution blueprint."],
      ["BATCH_STARTED", "When a parallel/sequential wave begins."],
      ["TOOL_FINISHED", "When a specific tool handler returns its result."]
    ]}
  ],

  "provider-abstraction": [
    { type: "text", value: "Provider Abstraction is the interface layer that allows MTPX to remain vendor-agnostic. It normalizes diverse model APIs (OpenAI, Anthropic, Gemini, Groq, etc.) into a unified, protocol-compliant Execution Plan format." },

    { type: "heading", value: "Overview" },
    { type: "text", value: "The 'LLM landscape' is fragmented, with each vendor using different schemas for tool-calling and structured output. MTPX solves this through an 'Adapter Pattern', ensuring your tool logic and runtime remain identical whether you are using a state-of-the-art cloud model or a local model via Ollama." },

    { type: "heading", value: "Why It Exists" },
    { type: "text", value: "Vendor lock-in is a significant risk in AI infrastructure. Provider Abstraction ensures:" },
    { type: "list", value: "", items: [
      "Portability — Swap your 'brain' (OpenAI for Anthropic) by changing a single line of code.",
      "Protocol Compliance — Forcing diverse models to adhere to the strict MTPX DAG-planning schema.",
      "Unified Context — Standardized handling of message history and tool specifications across all providers."
    ]},

    { type: "heading", value: "How It Works" },
    { type: "text", value: "The abstraction layer performs a 3-way translation for every request:" },
    { type: "list", value: "", items: [
      "Outbound Schema Translation — Converting the `ToolRegistry` specs into the vendor's specific format (e.g., OpenAI Function JSON).",
      "Inbound Plan Extraction — Parsing the model's raw output (Text or JSON) into a typed MTPX `ExecutionPlan`.",
      "Error Normalization — Converting vendor-specific API errors (e.g., rate limits, context window issues) into standard MTPX exceptions."
    ]},

    { type: "heading", value: "Architecture Flow" },
    { type: "architecture", value: `[ MTPX Agent ] ──▶ [ BaseProvider ]
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
    [ OpenAI Adapter ]                [ Anthropic Adapter ]
     (Tool-Choice API)                 (Tool-Use Beta API)
            │                                 │
            └────────────────┬────────────────┘
                             ▼
                    [ Vendor Gateway ]` },

    { type: "heading", value: "Code Examples" },
    { type: "text", value: "MTPX makes switching providers a matter of configuration. Your tools and runtime logic stay 100% identical." },
    { type: "code", language: "python", value: `from mtp.providers import OpenAI, Anthropic, Gemini

# Switch between cloud providers with zero logic changes
# provider = OpenAI(model="gpt-4o")
# provider = Anthropic(model="claude-3-5-sonnet-latest")
provider = Gemini(model="gemini-1.5-pro-002")

agent = Agent.MTPAgent(provider=provider, tools=my_registry)` },

    { type: "heading", value: "Runtime Behavior" },
    { type: "text", value: "At runtime, the Provider Adapter is responsible for 'Grounded Reasoning'. It ensures the model is aware of the specific types and risk levels of the tools in the registry. If a provider returns a plan that doesn't follow the MTPX protocol (e.g., missing tool IDs or invalid references), the adapter intercepts this and returns a `MalformedPlanError` to the agent loop before execution begins." },

    { type: "heading", value: "Best Practices" },
    { type: "list", value: "", items: [
      "Provider Fallbacks — Use multiple providers in production to ensure high availability during vendor outages.",
      "Model-Specific Prompts — While the interface is unified, different models may need slightly different instructions to plan effectively.",
      "Cost Monitoring — Attach cost-tracking observers to the provider to monitor token usage across different vendors."
    ]},

    { type: "heading", value: "Common Mistakes" },
    { type: "list", value: "", items: [
      "Vendor-Specific Assumptions — Hardcoding logic that assumes the model uses 'OpenAI-style' tool calls.",
      "Inconsistent Schemas — Manually creating tool definitions instead of letting the `ToolRegistry` normalize them for the provider.",
      "Ignoring Context Windows — Failing to prune session history, which leads to provider-specific context overflow errors."
    ]},

    { type: "heading", value: "Related Concepts" },
    { type: "table", headers: ["Component", "Purpose"], rows: [
      ["Adapter Pattern", "The architectural design used to normalize vendor APIs."],
      ["ExecutionPlan", "The common protocol target for all providers."],
      ["Structured Output", "The technique used to force models to output valid JSON DAGs."]
    ]}
  ],

  "execution-lifecycle": [
    { type: "text", value: "The Execution Lifecycle defines the end-to-end journey of an MTPX request. It is a 6-stage deterministic process that ensures every agent action is planned, validated, authorized, and observable." },

    { type: "heading", value: "Overview" },
    { type: "text", value: "MTPX moves away from 'black-box' agent loops. By defining a clear, stage-gated lifecycle, the framework provides hooks for security, monitoring, and human intervention at every critical junction of the agentic process." },

    { type: "heading", value: "Why It Exists" },
    { type: "text", value: "Standardized lifecycles are essential for production-grade infrastructure. They provide:" },
    { type: "list", value: "", items: [
      "Predictability — You know exactly what stage the agent is in at any given millisecond.",
      "Fault Tolerance — Specific stages (like Validation) can catch errors before destructive actions occur.",
      "Extension Points — Engineers can hook into specific lifecycle stages to add custom logic (e.g., preprocessing plans)."
    ]},

    { type: "heading", value: "How It Works" },
    { type: "text", value: "The MTPX lifecycle consists of 6 discrete phases:" },
    { type: "list", value: "", items: [
      "1. INGEST — The user request and session context are gathered.",
      "2. PLAN — The Provider generates a structured DAG Execution Plan.",
      "3. VALIDATE — The plan is checked for cycles and schema compliance.",
      "4. AUTHORIZE — Each tool call is evaluated against the Policy Engine.",
      "5. EXECUTE — The DAG Executor dispatches tool calls in optimal waves.",
      "6. FINALIZE — The results are synthesized into a final grounded response."
    ]},

    { type: "heading", value: "Architecture Flow" },
    { type: "architecture", value: `[ USER ] ──▶ ( INGEST )
                    │
             (    PLAN    )  ──▶ [ LLM reasoning ]
                    │
             (  VALIDATE  )  ──▶ [ Graph Check ]
                    │
             ( AUTHORIZE  )  ──▶ [ Risk Policy ]
                    │
             (  EXECUTE   )  ──▶ [ Runtime ]
                    │
             (  FINALIZE  )  ──▶ [ Model Synthesis ]
                    │
             [ FINAL RESULT ]` },

    { type: "heading", value: "Code Examples" },
    { type: "text", value: "You can monitor the lifecycle by attaching an observer that listens for stage transition events." },
    { type: "code", language: "python", value: `from mtp import Agent, EventType

class LifecycleObserver:
    def on_event(self, event):
        if event.type == EventType.BATCH_STARTED:
            print(f"Entering EXECUTE phase for wave {event.payload.batch_index}")
        elif event.type == EventType.PLAN_RECEIVED:
            print("Entering VALIDATE phase for new execution plan")

agent = Agent.MTPAgent(..., observers=[LifecycleObserver()])` },

    { type: "heading", value: "Runtime Behavior" },
    { type: "text", value: "The lifecycle is transactional. If a failure occurs in the VALIDATE or AUTHORIZE stages, the lifecycle is aborted before the EXECUTE stage begins. This 'safe-fail' behavior is what makes MTPX suitable for critical infrastructure where executing a broken or unauthorized plan could have severe consequences." },

    { type: "heading", value: "Best Practices" },
    { type: "list", value: "", items: [
      "Pre-Execution Hooks — Use the VALIDATE stage to perform custom logic, like checking available budget or rate limits.",
      "Post-Execution Hooks — Use the FINALIZE stage to clean up temporary resources (e.g., deleting a sandbox file).",
      "Stage Logging — Always log the transition into the AUTHORIZE stage for compliance and auditing."
    ]},

    { type: "heading", value: "Common Mistakes" },
    { type: "list", value: "", items: [
      "Bypassing Stages — Attempting to manually call tools without going through the Planner/Validator stages.",
      "Stage Overload — Putting too much business logic into a single stage, which can lead to performance bottlenecks.",
      "Ignoring Stage Failures — Failing to handle the specific exceptions raised at different lifecycle boundaries."
    ]},

    { type: "heading", value: "Related Concepts" },
    { type: "table", headers: ["Stage", "Primary Component"], rows: [
      ["PLAN", "Provider Adapter"],
      ["VALIDATE", "Plan Validator"],
      ["EXECUTE", "DAG Executor"]
    ]}
  ],

  // ─── ARCHITECTURE ───────────────────────────────────────────

  "execution-flow": [
    { type: "text", value: "The Execution Flow represents the deterministic journey of a request from user input to tool execution and grounded response synthesis." },

    { type: "heading", value: "Overview" },
    { type: "text", value: "Traditional agent loops are often 'black boxes' where the model's reasoning and tool calls are inextricably linked. MTPX breaks this into a pipeline of discrete stages. By separating planning from execution, MTPX provides hooks for validation, policy enforcement, and observability that are impossible in direct-call systems." },

    { type: "heading", value: "Why It Exists" },
    { type: "text", value: "The execution flow exists to provide a 'Safety Buffer' between model intent and system action. It ensures:" },
    { type: "list", value: "", items: [
      "Transactional Integrity — Plans are validated before any tool is invoked.",
      "Observability — Every stage transition emits a standard event for monitoring.",
      "Interposability — Security layers can intercept the flow at any stage to deny or modify actions."
    ]},

    { type: "heading", value: "How It Works" },
    { type: "text", value: "The flow consists of six discrete gates:" },
    { type: "list", value: "", items: [
      "1. Ingest — Normalizing the user prompt and loading session state.",
      "2. Plan — The LLM generates a structured DAG (Directed Acyclic Graph) of tool calls.",
      "3. Validate — The Runtime checks the DAG for logical consistency and dependency cycles.",
      "4. Authorize — The Policy Engine evaluates the risk level of each tool call.",
      "5. Execute — The Runtime dispatches tools in optimal waves (sequential or parallel).",
      "6. Synthesize — The results are fed back to the LLM for a final, grounded answer."
    ]},

    { type: "heading", value: "Architecture Flow" },
    { type: "architecture", value: `[ User Request ]
       │
       ▼
 [ Context Ingest ] ──▶ [ Persistence Store ]
       │
       ▼
 [ Planner (LLM) ] ──▶ [ Tool Registry ]
       │
       ▼
 [ Execution Plan ] ◀── [ Cycle Validator ]
       │
       ▼
 [ Policy Engine ]  ──▶ [ Risk Policies ]
       │
       ▼
 [ Runtime Engine ] ──▶ [ Tool Sandboxes ]
       │
       ▼
 [ Final Response ]` },

    { type: "heading", value: "Code Examples" },
    { type: "text", value: "MTPX handles the entire flow internally, but you can inspect the state at any stage using observers." },
    { type: "code", language: "python", value: `from mtp import Agent
from mtp.observers import EventType

# A simple observer to log flow transitions
def flow_logger(event):
    if event.type == EventType.STAGE_TRANSITION:
        print(f"[FLOW] Entering {event.payload.stage} stage...")

agent = Agent.MTPAgent(..., observers=[flow_logger])
agent.run("Analyze the latest server logs and report errors.")` },

    { type: "heading", value: "Runtime Behavior" },
    { type: "text", value: "The flow is strictly sequential until the 'Execute' stage. If the 'Plan' stage fails (e.g., the model produces invalid JSON), the entire flow is short-circuited. During the 'Execute' stage, the flow may become non-linear as the DAG resolution engine determines which tools can be run in parallel based on their dependency graph." },

    { type: "heading", value: "Best Practices" },
    { type: "list", value: "", items: [
      "Context Isolation — Ensure each execution flow starts with a fresh session unless persistence is explicitly required.",
      "Timeout Policies — Configure per-stage timeouts to prevent a slow LLM response from stalling the entire pipeline.",
      "Dry Runs — Use the 'Validate' stage to perform 'pre-flight' checks without actually executing tools."
    ]},

    { type: "heading", value: "Common Mistakes" },
    { type: "list", value: "", items: [
      "Mixing Logic — Attempting to handle tool results inside the 'Plan' stage instead of letting the 'Synthesize' stage handle them.",
      "Ignoring Events — Not monitoring stage transitions, leading to 'silent failures' in complex multi-step tasks.",
      "Oversized Context — Passing too much history in the 'Ingest' stage, which degrades the Planner's ability to create accurate DAGs."
    ]},

    { type: "heading", value: "Related Concepts" },
    { type: "table", headers: ["Stage", "Control Mechanism"], rows: [
      ["Plan", "Provider Adapter"],
      ["Authorize", "Policy Engine"],
      ["Execute", "DAG Runtime"]
    ]}
  ],

  "planner-vs-runtime": [
    { type: "text", value: "The Planner and Runtime are the two primary pillars of MTPX, strictly separating 'Reasoning' from 'Execution'." },

    { type: "heading", value: "Overview" },
    { type: "text", value: "Most agent frameworks treat the model and the code as a single entity. MTPX enforces a 'Chinese Wall' between them. The Planner (LLM) is an untrusted entity that suggests actions, while the Runtime (Code) is the trusted entity that validates and executes those actions." },

    { type: "heading", value: "Why It Exists" },
    { type: "text", value: "This separation is the core of the MTP security model. It exists to:" },
    { type: "list", value: "", items: [
      "Prevent Injection — Even if a model is compromised (Prompt Injection), the Runtime prevents it from calling dangerous tools without authorization.",
      "Ensure Determinism — The Runtime executes the DAG exactly as planned, regardless of model variations.",
      "Simplify Debugging — Reasoning errors (Planner) are clearly separated from execution errors (Runtime)."
    ]},

    { type: "heading", value: "How It Works" },
    { type: "text", value: "The interaction follows a Request-Plan-Execution-Result (RPER) pattern:" },
    { type: "list", value: "", items: [
      "1. Request — The User sends a prompt to the Planner.",
      "2. Plan — The Planner returns a structured JSON DAG of tool calls (The 'Intent').",
      "3. Execute — The Runtime receives the intent, checks it against the Tool Registry and Policy Engine, and invokes the tools (The 'Action').",
      "4. Result — The Runtime feeds the tool outputs back to the Planner for final synthesis."
    ]},

    { type: "heading", value: "Architecture Flow" },
    { type: "architecture", value: `      [ PLANNER ]                    [ RUNTIME ]
    (The Reasoning Layer)          (The Execution Layer)
           │                              │
           │  1. Suggests Plan (DAG)      │
           ├─────────────────────────────▶│
           │                              │  2. Validates Plan
           │                              │  3. Enforces Policies
           │                              │  4. Executes Tools
           │  5. Returns Raw Results      │
           │◀─────────────────────────────┤
           │                              │
           ▼                              ▼
    [ Final Synthesis ]           [ State Update ]` },

    { type: "heading", value: "Code Examples" },
    { type: "text", value: "The separation is reflected in the code through the `Provider` (Planner) and `Runtime` (Executor) classes." },
    { type: "code", language: "python", value: `# Planner configuration (LLM specific)
planner = OpenAI(model="gpt-4o", temperature=0)

# Runtime configuration (Execution specific)
runtime = MTPRuntime(
    registry=my_tools,
    policy_engine=strict_policies,
    sandbox=DockerSandbox()
)

# The Agent orchestrates the bridge between them
agent = Agent.MTPAgent(provider=planner, runtime=runtime)` },

    { type: "heading", value: "Runtime Behavior" },
    { type: "text", value: "The Runtime is effectively 'LLM-blind'. It does not care which model produced the DAG; it only cares if the DAG is logically sound and compliant with local security policies. This allows you to hot-swap planners (e.g., moving from gpt-4 to claude-3) without ever touching your tool execution logic or sandbox configurations." },

    { type: "heading", value: "Best Practices" },
    { type: "list", value: "", items: [
      "Zero-Trust Planning — Treat all Planner output as potentially malicious until validated by the Runtime.",
      "Runtime Constraints — Set hard CPU and memory limits on the Runtime, independent of the Planner's token limits.",
      "Clear Interface — Ensure tool descriptions in the Planner are descriptive enough to generate valid DAG arguments."
    ]},

    { type: "heading", value: "Common Mistakes" },
    { type: "list", value: "", items: [
      "Logic Leakage — Putting complex business logic inside a Tool Handler instead of letting the Planner orchestrate it via smaller tools.",
      "Bypassing the Runtime — Allowing the Planner to directly access system APIs without going through the defined MTP toolkit.",
      "Shared State — Assuming the Planner knows the exact state of the system; always let the Runtime provide the final grounded truth."
    ]},

    { type: "heading", value: "Related Concepts" },
    { type: "table", headers: ["Pillar", "Responsibility"], rows: [
      ["Planner", "Intent Generation, Reasoning, Synthesis"],
      ["Runtime", "Validation, Execution, Security, Sandboxing"]
    ]}
  ],

  "dag-resolution": [
    { type: "text", value: "DAG Resolution is the process of decomposing a complex Execution Plan into a sequence of executable waves based on tool dependencies." },

    { type: "heading", value: "Overview" },
    { type: "text", value: "A standard agent executes tools one-by-one. MTPX, however, treats tool calls as nodes in a Directed Acyclic Graph (DAG). This allows the runtime to identify which tools are independent and can be executed in parallel, and which must wait for the output of a previous node." },

    { type: "heading", value: "Why It Exists" },
    { type: "text", value: "DAG resolution is the engine behind MTPX's performance and reliability. It provides:" },
    { type: "list", value: "", items: [
      "Parallelism — Execute non-dependent tools (e.g., fetching 3 different URLs) simultaneously to reduce latency.",
      "Deterministic Ordering — Ensure that a 'Summarize' tool never runs before the 'Read' tool has provided its input.",
      "Cycle Detection — Automatically identify and reject execution plans that contain circular dependencies."
    ]},

    { type: "heading", value: "How It Works" },
    { type: "text", value: "The resolution engine performs three primary operations:" },
    { type: "list", value: "", items: [
      "1. Dependency Mapping — Parsing the 'depends_on' field of every action in the Execution Plan.",
      "2. Topological Sort — Sorting the nodes into 'Waves'. Wave 0 contains all nodes with zero dependencies. Wave 1 contains nodes that only depend on Wave 0, and so on.",
      "3. Sequential Dispatch — The Runtime executes Wave 0 in parallel, waits for all results, injects the outputs into the next wave, and repeats until the graph is exhausted."
    ]},

    { type: "heading", value: "Architecture Flow" },
    { type: "architecture", value: `[ Execution Plan ]
       │
       ▼
 [ Graph Builder ] ──▶ [ Cycle Detector ]
       │
       ▼
 [ Topological Sorter ]
       │
       ├─▶ [ Wave 0: Parallel Tool Calls ]
       │      (Tool A, Tool B, Tool C)
       │
       ├─▶ [ Wave 1: Dependent Tool Calls ]
       │      (Tool D -> depends on A)
       │
       └─▶ [ Wave 2: Final Synthesis ]
              (Tool E -> depends on D)` },

    { type: "heading", value: "Code Examples" },
    { type: "text", value: "The resolution happens automatically, but you can see the wave distribution in the `ExecutionPlan` object." },
    { type: "code", language: "python", value: `plan = agent.last_plan
print(f"Total Waves: {len(plan.waves)}")

for i, wave in enumerate(plan.waves):
    print(f"Wave {i}: {[action.tool_id for action in wave.actions]}")

# Output Example:
# Wave 0: ['fetch_url_1', 'fetch_url_2']
# Wave 1: ['summarize_content']` },

    { type: "heading", value: "Runtime Behavior" },
    { type: "text", value: "During execution, if any tool in Wave N fails, the Runtime immediately halts the resolution. Dependent tools in Wave N+1 are never invoked, preventing 'Cascading Failures'. This ensures that a tool downstream never receives null or invalid input from its dependencies." },

    { type: "heading", value: "Best Practices" },
    { type: "list", value: "", items: [
      "Granular Tools — Build small, single-purpose tools. The more granular your tools, the more opportunities the DAG engine has for parallelism.",
      "Explicit Dependencies — Ensure your Provider is instructed to always specify dependencies in the JSON output.",
      "Resource Limits — When running large parallel waves, ensure your sandbox has enough concurrent process/thread capacity."
    ]},

    { type: "heading", value: "Common Mistakes" },
    { type: "list", value: "", items: [
      "Circular References — Creating a plan where Tool A depends on B, and B depends on A (The Runtime will catch this during Validation).",
      "Implicit Dependencies — Assuming a tool will run after another without explicitly defining it in the DAG.",
      "Wave Bottlenecks — Including one extremely slow tool in an otherwise fast parallel wave, which stalls the entire resolution."
    ]},

    { type: "heading", value: "Related Concepts" },
    { type: "table", headers: ["Algorithm", "Application"], rows: [
      ["Topological Sort", "Determining the execution order of non-cyclic nodes."],
      ["Kahn's Algorithm", "The specific implementation used for dependency resolution."],
      ["Wait-For-All", "The synchronization primitive used between execution waves."]
    ]}
  ],

  "state-persistence": [
    { type: "text", value: "State Persistence ensures that agents retain memory, context, and checkpoint data across multiple rounds of interaction and system restarts." },

    { type: "heading", value: "Overview" },
    { type: "text", value: "In production AI systems, statelessness is a liability. MTPX provides a robust persistence layer that serializes the entire agent state—including message history, session variables, and tool execution traces—into a persistent store." },

    { type: "heading", value: "Why It Exists" },
    { type: "text", value: "Persistence is required for building systems that aren't just 'chatbots' but 'long-running workers'. It provides:" },
    { type: "list", value: "", items: [
      "Continuity — An agent can remember a file it created 3 days ago.",
      "Resilience — If the runtime crashes mid-execution, the agent can be restored from the last known-good checkpoint.",
      "Auditing — A permanent record of every plan, tool call, and result for compliance and debugging."
    ]},

    { type: "heading", value: "How It Works" },
    { type: "text", value: "MTPX uses a 'Session-Based' persistence model:" },
    { type: "list", value: "", items: [
      "1. Snapshotting — At the end of every execution round, the `SessionManager` captures the current delta of the agent state.",
      "2. Serialization — The state is converted into a vendor-neutral format (usually JSON) via the `BaseStorageAdapter`.",
      "3. Storage — The adapter writes to the configured backend (Postgres, Redis, MongoDB, or local Disk).",
      "4. Hydration — On the next request, the agent is initialized with the `session_id`, and the storage adapter restores the state."
    ]},

    { type: "heading", value: "Architecture Flow" },
    { type: "architecture", value: `[ MTP Agent ] ◀──▶ [ Session Manager ]
                          │
            ┌─────────────┴─────────────┐
            ▼                           ▼
    [ Memory Buffer ]           [ Storage Adapter ]
    (L1 Cache: RAM)             (L2 Persist: DB)
            │                           │
            └─────────────┬─────────────┘
                          ▼
                  [ Persistence DB ]` },

    { type: "heading", value: "Code Examples" },
    { type: "text", value: "Configuring persistence is done by passing a storage adapter to the agent or session manager." },
    { type: "code", language: "python", value: `from mtp.storage import PostgresStorage
from mtp import SessionManager

# 1. Initialize persistent storage
db = PostgresStorage(connection_string="postgresql://...")

# 2. Attach to the agent
agent = Agent.MTPAgent(
    ...,
    session_id="research_task_45",
    storage=db
)

# The agent will now automatically load and save state
agent.run("Continue where we left off on the market report.")` },

    { type: "heading", value: "Runtime Behavior" },
    { type: "text", value: "The persistence layer uses 'Atomic Checkpointing'. The state is only updated *after* the `Finalize` stage of the execution lifecycle completes successfully. If a crash occurs during tool execution, the storage remains at the previous round's state, preventing the system from persisting corrupted or incomplete session data." },

    { type: "heading", value: "Best Practices" },
    { type: "list", value: "", items: [
      "History Pruning — For long-running sessions, use a `PruningPolicy` to summarize old messages and save context tokens.",
      "Encrypted Storage — Sensitive session data (like tool outputs containing PII) should be stored in an encrypted database.",
      "Session TTLs — Set expiration times on sessions to automatically clean up resources for finished tasks."
    ]},

    { type: "heading", value: "Common Mistakes" },
    { type: "list", value: "", items: [
      "Unbounded History — Letting session history grow until it exceeds the model's context window.",
      "Race Conditions — Attempting to write to the same session ID from two different agent instances simultaneously.",
      "Leaking State — Forgetting to clear a session's state after a task is completed, leading to context pollution in future runs."
    ]},

    { type: "heading", value: "Related Concepts" },
    { type: "table", headers: ["Component", "Function"], rows: [
      ["Storage Adapter", "The bridge to the physical database."],
      ["State Hydration", "Loading saved JSON into active Python objects."],
      ["Pruning Policy", "Strategies for managing context window overflow."]
    ]}
  ],

  "tool-sandboxing": [
    { type: "text", value: "Tool Sandboxing provides secure isolation for tool execution, ensuring that an agent cannot access or damage the host system beyond its explicitly granted permissions." },

    { type: "heading", value: "Overview" },
    { type: "text", value: "When an LLM generates arguments for a tool, it is effectively generating code that will run on your infrastructure. MTPX treats every tool call as 'Untrusted Input'. Sandboxing is the mechanism that wraps these calls in a protective boundary, limiting their access to CPU, memory, network, and the filesystem." },

    { type: "heading", value: "Why It Exists" },
    { type: "text", value: "Without sandboxing, a compromised or hallucinating model could inadvertently (or maliciously) delete files, leak credentials, or perform SSRF attacks. Sandboxing provides:" },
    { type: "list", value: "", items: [
      "Blast Radius Limitation — If a tool fails or behaves unexpectedly, the damage is contained within the sandbox.",
      "Resource Governance — Prevent a 'Heavy' tool from consuming all host RAM and crashing the server.",
      "Security Hardening — Disabling network access for tools that only need to perform local data processing."
    ]},

    { type: "heading", value: "How It Works" },
    { type: "text", value: "MTPX supports a tiered sandboxing model:" },
    { type: "list", value: "", items: [
      "1. Process Sandbox — Running tools in a separate OS process with restricted environment variables and working directories.",
      "2. Container Sandbox — Executing tools inside a fresh Docker or Podman container for near-total filesystem isolation.",
      "3. Virtualized Sandbox — (Coming soon) Micro-VM based isolation (Firecracker) for high-security enterprise environments."
    ]},

    { type: "heading", value: "Architecture Flow" },
    { type: "architecture", value: `[ MTP Runtime ]
       │
       ▼
 [ Sandbox Manager ] ◀── [ Resource Limits ]
       │
       ├─▶ [ Process Jail ] ──▶ ( Tool A )
       │      (Restricted FS)
       │
       └─▶ [ Docker Container ] ──▶ ( Tool B )
              (No Network)
              (256MB RAM Limit)` },

    { type: "heading", value: "Code Examples" },
    { type: "text", value: "You can configure the global sandbox for the runtime or override it for specific high-risk tools." },
    { type: "code", language: "python", value: `from mtp.runtime import MTPRuntime
from mtp.sandbox import DockerSandbox

# 1. Define a strict sandbox
secure_sandbox = DockerSandbox(
    image="python:3.11-slim",
    allow_network=False,
    mem_limit="512m",
    workdir="/tmp/agent_workspace"
)

# 2. Attach to the runtime
runtime = MTPRuntime(..., sandbox=secure_sandbox)

# Tools executed by this runtime will now run inside isolated containers.` },

    { type: "heading", value: "Runtime Behavior" },
    { type: "text", value: "The sandbox is initialized immediately before the `Execute` stage. The Runtime mounts only the necessary data into the sandbox environment. Once the tool returns its result, the sandbox is torn down (or reset), and any temporary files created by the tool are automatically purged. This 'Ephemeral execution' pattern ensures no state leaks between different tool calls or user sessions." },

    { type: "heading", value: "Best Practices" },
    { type: "list", value: "", items: [
      "Least Privilege — Only grant a tool the minimum permissions it needs. If a tool doesn't need internet access, disable the network in the sandbox config.",
      "Timeouts — Always set a `max_execution_time` for sandboxed processes to prevent infinite loops (e.g., a model generating `while True: pass`).",
      "Monitoring — Attach an observer to log sandbox resource usage (CPU/RAM) to identify inefficient tools."
    ]},

    { type: "heading", value: "Common Mistakes" },
    { type: "list", value: "", items: [
      "Shared Workdirs — Using the same local directory for multiple agents, allowing them to see or modify each other's files.",
      "Environment Leaks — Passing sensitive host environment variables (like DB passwords) into the sandbox unnecessarily.",
      "Missing Limits — Running unsandboxed code on the host machine during development, which can lead to accidental file deletion."
    ]},

    { type: "heading", value: "Related Concepts" },
    { type: "table", headers: ["Sandbox Type", "Isolation Level"], rows: [
      ["Process", "Low (OS Level)"],
      ["Docker", "Medium (Kernel Level)"],
      ["Firecracker", "High (Hardware Level)"]
    ]}
  ],

  "event-bus": [
    { type: "text", value: "The Event Bus is the central nervous system of MTPX, responsible for routing internal state transitions to observers, logs, and real-time streaming interfaces." },

    { type: "heading", value: "Overview" },
    { type: "text", value: "MTPX utilizes a decoupled Pub/Sub architecture. Components like the Runtime or Policy Engine do not know about your UI or logging stack; they simply emit events to the Event Bus. This allows you to attach any number of observers (Console, Sentry, Webhooks) without modifying the core execution logic." },

    { type: "heading", value: "Why It Exists" },
    { type: "text", value: "The Event Bus provides the 'Observability' pillar of MTPX. It exists to:" },
    { type: "list", value: "", items: [
      "Decouple Concerns — The execution engine stays focused on tools, while the Event Bus handles reporting.",
      "Real-time Feedback — Enable low-latency TUIs and web dashboards that show 'what the agent is thinking' as it happens.",
      "Auditability — Create a non-repudiable trace of every action taken by the model."
    ]},

    { type: "heading", value: "How It Works" },
    { type: "text", value: "The bus operates on a simple asynchronous dispatch mechanism:" },
    { type: "list", value: "", items: [
      "1. Emission — A component (e.g., the Planner) calls `bus.emit(event)` with a payload.",
      "2. Dispatch — The Bus identifies all registered observers subscribed to that event type.",
      "3. Consumption — The Bus invokes the `on_event` handler of each observer. In production, this is done in a non-blocking thread to ensure zero performance impact on the agent reasoning loop."
    ]},

    { type: "heading", value: "Architecture Flow" },
    { type: "architecture", value: `[ Runtime Engine ]       [ Policy Engine ]
           │                        │
           └───────┬────────────────┘
                   ▼
             [ EVENT BUS ]
                   │
    ┌──────────────┴──────────────┬──────────────┐
    ▼                             ▼              ▼
[ Log Observer ]        [ Console TUI ]    [ Webhook ]
 (File/S3)               (Developer)        (UI/API)` },

    { type: "heading", value: "Code Examples" },
    { type: "text", value: "Creating a custom observer is as simple as implementing the `on_event` method." },
    { type: "code", language: "python", value: `from mtp.events import EventBus, Event
from mtp.observers import BaseObserver

class MySecurityLogger(BaseObserver):
    def on_event(self, event: Event):
        if event.type == "POLICY_VIOLATION":
            send_slack_alert(f"Critical: {event.payload['tool_id']} was blocked!")

# Attach to the agent
agent = Agent.MTPAgent(..., observers=[MySecurityLogger()])` },

    { type: "heading", value: "Runtime Behavior" },
    { type: "text", value: "The Event Bus is strictly one-way. Observers can read events but cannot modify the execution state. This ensures that a buggy observer cannot crash the core agent or inject unintended data into the tool loop. Every event emitted by the bus is timestamped and assigned a unique `event_id` and `round_id` for distributed tracing." },

    { type: "heading", value: "Best Practices" },
    { type: "list", value: "", items: [
      "Asynchronous Handlers — If your observer performs I/O (like writing to a DB), use the built-in `AsyncObserver` wrapper to prevent stalling the runtime.",
      "Event Filtering — Subscribe only to the event types you need (e.g., `TOOL_STARTED`, `TOOL_FINISHED`) to reduce overhead in high-traffic systems.",
      "Structured Payloads — Always treat event payloads as JSON-serializable to ensure compatibility with external monitoring stacks."
    ]},

    { type: "heading", value: "Common Mistakes" },
    { type: "list", value: "", items: [
      "Blocking the Bus — Performing heavy computations directly inside the `on_event` handler.",
      "Ignoring Metadata — Failing to log the `round_id`, which makes it impossible to link events back to a specific user conversation.",
      "Over-Subscription — Attaching too many redundant observers in a performance-sensitive environment."
    ]},

    { type: "heading", value: "Related Concepts" },
    { type: "table", headers: ["Event Type", "Payload Example"], rows: [
      ["PLAN_RECEIVED", "{ 'waves': 3, 'actions': 5 }"],
      ["TOOL_STARTED", "{ 'tool_id': 'calculator', 'args': {...} }"],
      ["STATE_UPDATED", "{ 'session_id': 'abc', 'round': 2 }"]
    ]}
  ],

  "provider-layer": [
    { type: "text", value: "The Provider Layer is the normalization bridge between MTPX and various Large Language Model vendors." },

    { type: "heading", value: "Overview" },
    { type: "text", value: "Different models speak different 'dialects' of tool-calling. OpenAI uses `tools` and `function_call`, Anthropic uses `tool_use`, and Gemini uses its own SDK format. The Provider Layer abstracts these differences, allowing the rest of the MTPX framework to interact with a single, unified interface." },

    { type: "heading", value: "Why It Exists" },
    { type: "text", value: "The Provider Layer exists to provide 'Model Portability'. It ensures:" },
    { type: "list", value: "", items: [
      "Vendor Neutrality — Change models without changing your tool definitions or runtime logic.",
      "Schema Normalization — MTPX tools use standard type hints, which the Provider Layer automatically translates into vendor-specific JSON schemas.",
      "Prompt Consistency — The layer handles system prompt injection and tool-choice formatting consistently across all vendors."
    ]},

    { type: "heading", value: "How It Works" },
    { type: "text", value: "The layer follows a 4-step transformation pipeline:" },
    { type: "list", value: "", items: [
      "1. Registration — The `ToolRegistry` provides abstract tool specs to the Provider.",
      "2. Translation — The Provider converts these specs into the vendor's specific tool schema.",
      "3. Inference — The Provider sends the prompt and tools to the LLM API.",
      "4. Extraction — The Provider parses the vendor's tool-call response into a typed MTPX `ExecutionPlan`."
    ]},

    { type: "heading", value: "Architecture Flow" },
    { type: "architecture", value: `[ MTPX Agent ]
       │
       ▼
 [ BaseProvider ] ◀── [ ToolRegistry ]
       │
 ┌─────┴─────┬────────────┐
 ▼           ▼            ▼
[ OpenAI ] [ Anthropic ] [ Ollama ]
 (SDK A)    (SDK B)      (REST API)` },

    { type: "heading", value: "Code Examples" },
    { type: "text", value: "All providers share the same constructor interface, making them easily interchangeable." },
    { type: "code", language: "python", value: `from mtp.providers import OpenAI, Anthropic

# These two objects are functionally identical to the MTP Agent
p1 = OpenAI(model="gpt-4o", api_key="...")
p2 = Anthropic(model="claude-3-5-sonnet", api_key="...")

# You can swap them at runtime based on task complexity
provider = p2 if task == "coding" else p1` },

    { type: "heading", value: "Runtime Behavior" },
    { type: "text", value: "The Provider Layer is responsible for 'Plan Grounding'. If a model hallucinates a tool that doesn't exist in the registry, the Provider Layer is the first line of defense, catching the error and returning a `InvalidToolReference` exception before the Runtime even attempts to start execution." },

    { type: "heading", value: "Best Practices" },
    { type: "list", value: "", items: [
      "Unified Tool Specs — Always define tools using MTP's `@tool` decorator to ensure they can be translated to any provider correctly.",
      "Temperature Tuning — For planning tasks, keep temperature low (0.0 to 0.2) to ensure the model adheres to the structured JSON schema.",
      "Provider Fallbacks — Implement a fallback provider (e.g., Groq or local Llama-3) to maintain availability during vendor downtime."
    ]},

    { type: "heading", value: "Common Mistakes" },
    { type: "list", value: "", items: [
      "Manual Schema Building — Trying to build OpenAI/Anthropic tool JSONs manually instead of using the `ToolRegistry`.",
      "Mixing Provider SDKs — Attempting to use the raw `openai` or `anthropic` clients directly inside the agent loop.",
      "Missing API Keys — Forgetting to set environment variables for the specific provider used."
    ]},

    { type: "heading", value: "Related Concepts" },
    { type: "table", headers: ["Provider", "Key Strength"], rows: [
      ["OpenAI", "Reliable function calling & instruction following."],
      ["Anthropic", "Large context windows & nuanced reasoning."],
      ["Groq", "Extreme low-latency tool execution (LPU)."]
    ]}
  ],

  // ─── SDK REFERENCE ──────────────────────────────────────────

  "sdk-agent": [
    { type: "text", value: "The `MTPAgent` is the primary entry point for orchestrating model reasoning and tool execution." },
    { type: "api-method", value: "MTPAgent(provider, tools, instructions, observers=None, ...)", fields: [
      { name: "provider", type: "BaseProvider", required: true, description: "An instance of a model provider (OpenAI, Anthropic, etc.)." },
      { name: "tools", type: "ToolRegistry | List[Toolkit]", required: true, description: "The collection of tools available to the agent." },
      { name: "instructions", type: "str", required: false, description: "System-level instructions for the agent's behavior." },
      { name: "observers", type: "List[BaseObserver]", required: false, description: "Optional list of event listeners." }
    ]},
    { type: "api-method", value: "agent.run(prompt, session_id=None, ...)", fields: [
      { name: "prompt", type: "str", required: true, description: "The user's request text." },
      { name: "session_id", type: "str", required: false, description: "The unique ID for maintaining state across rounds." }
    ], returns: "RunOutput" },
    { type: "api-method", value: "agent.stream(prompt, ...)", fields: [
       { name: "prompt", type: "str", required: true, description: "The user's request text." }
    ], returns: "Iterator[Event]" }
  ],

  "sdk-runtime": [
    { type: "text", value: "The `MTPRuntime` engine is responsible for the deterministic execution of DAG plans and policy enforcement." },
    { type: "api-method", value: "MTPRuntime(registry, policy_engine=None, sandbox=None)", fields: [
      { name: "registry", type: "ToolRegistry", required: true, description: "The registry containing tool handlers." },
      { name: "policy_engine", type: "PolicyEngine", required: false, description: "The security layer for risk evaluation." },
      { name: "sandbox", type: "BaseSandbox", required: false, description: "The isolation environment for tool calls." }
    ]},
    { type: "api-method", value: "runtime.execute_plan(plan, session=None)", fields: [
      { name: "plan", type: "ExecutionPlan", required: true, description: "The validated DAG plan to execute." },
      { name: "session", type: "Session", required: false, description: "The context for state injection." }
    ], returns: "ExecutionResult" }
  ],

  "sdk-tool": [
    { type: "text", value: "Tools are defined using the `@mtp_tool` decorator, which extracts metadata and type hints for the Planner." },
    { type: "api-method", value: "@mtp_tool(name=None, description=None, risk_level=RiskLevel.READ)", fields: [
      { name: "name", type: "str", required: false, description: "Override the function name sent to the model." },
      { name: "description", type: "str", required: false, description: "The documentation for the model's reasoning." },
      { name: "risk_level", type: "RiskLevel", required: false, description: "The security classification of the tool." }
    ]},
    { type: "code", language: "python", value: `@mtp_tool(risk_level=RiskLevel.WRITE)
def write_file(path: str, content: str):
    """Writes content to a specific filesystem path."""
    with open(path, "w") as f:
        f.write(content)` }
  ],

  "sdk-session": [
    { type: "text", value: "The `Session` class manages message history and transient state during an agentic round." },
    { type: "api-method", value: "session.get_history(limit=50)", fields: [
      { name: "limit", type: "int", required: false, description: "The number of recent messages to retrieve." }
    ], returns: "List[Message]" },
    { type: "api-method", value: "session.checkpoint(label=None)", fields: [
      { name: "label", type: "str", required: false, description: "An optional name for the state snapshot." }
    ], returns: "None" }
  ],

  "sdk-policies": [
    { type: "text", value: "The `PolicyEngine` evaluates tool calls against a set of predefined security rules." },
    { type: "api-method", value: "PolicyEngine.add_rule(risk_level, action)", fields: [
      { name: "risk_level", type: "RiskLevel", required: true, description: "The level to apply the rule to (READ/WRITE/DESTRUCTIVE)." },
      { name: "action", type: "PolicyAction", required: true, description: "The enforcement action (ALLOW/ASK/DENY)." }
    ]},
    { type: "api-method", value: "engine.evaluate(action, context)", fields: [
      { name: "action", type: "AgentAction", required: true, description: "The proposed tool call." }
    ], returns: "PolicyResolution" }
  ],

  "sdk-events": [
    { type: "text", value: "MTPX emits standard events throughout the execution lifecycle for monitoring and debugging." },
    { type: "table", headers: ["Event Class", "Description"], rows: [
      ["PlanReceived", "Emitted when the LLM returns its execution DAG."],
      ["ToolStarted", "Emitted immediately before a tool handler is invoked."],
      ["ToolFinished", "Emitted after a tool handler returns its result."],
      ["BatchStarted", "Emitted when a parallel wave of tools begins."]
    ]}
  ],

  "sdk-providers": [
    { type: "text", value: "Providers implement the `BaseProvider` interface to bridge specific model APIs to MTPX." },
    { type: "api-method", value: "BaseProvider.generate_plan(prompt, tools, history)", fields: [
      { name: "prompt", type: "str", required: true, description: "The current user query." },
      { name: "tools", type: "List[ToolSpec]", required: true, description: "The tool definitions." }
    ], returns: "ExecutionPlan" }
  ],

  "sdk-storage": [
    { type: "text", value: "Storage adapters allow session data to be persisted to various database backends." },
    { type: "api-method", value: "SessionStore.save_session(session)", fields: [
      { name: "session", type: "Session", required: true, description: "The session object to serialize." }
    ], returns: "None" },
    { type: "api-method", value: "SessionStore.load_session(session_id)", fields: [
      { name: "session_id", type: "str", required: true, description: "The unique ID to restore." }
    ], returns: "Session" }
  ],

  // ─── PROVIDERS ──────────────────────────────────────────────

  providers: [
    { type: "custom-providers-grid", value: "" }
  ],

  "provider-openai": [
    { type: "code", language: "python", value: "from mtp.providers import OpenAI\nprovider = OpenAI(model=\"gpt-4o\")" }
  ],

  "provider-anthropic": [
    { type: "code", language: "python", value: "from mtp.providers import Anthropic\nprovider = Anthropic(model=\"claude-3-5-sonnet-latest\")" }
  ],

  "provider-gemini": [
    { type: "code", language: "python", value: "from mtp.providers import Gemini\nprovider = Gemini(model=\"gemini-1.5-pro\")" }
  ],

  "provider-groq": [
    { type: "code", language: "python", value: "from mtp.providers import Groq\nprovider = Groq(model=\"llama-3.3-70b-versatile\")" }
  ],

  "provider-ollama": [
    { type: "code", language: "python", value: "from mtp.providers import Ollama\nprovider = Ollama(model=\"llama3\")" }
  ],

  "provider-custom": [
    { type: "text", value: "Implement the ProviderAdapter base class to add support for custom models." }
  ],

  // ─── SAFETY ─────────────────────────────────────────────────

  "safety-risk-levels": [
    { type: "table", headers: ["Level", "Action"], rows: [["READ", "Allow"], ["WRITE", "Ask"], ["DESTRUCTIVE", "Deny"]] }
  ],

  "safety-approval": [
    { type: "text", value: "Configuring approval_handler for Human-in-the-Loop workflows." }
  ],

  "safety-sandboxing": [
    { type: "text", value: "Best practices for isolating agents from sensitive host resources." }
  ],

  "safety-permissions": [
    { type: "text", value: "Role-based access control (RBAC) for tool usage." }
  ],

  "safety-audit": [
    { type: "text", value: "Generating tamper-evident execution logs for compliance." }
  ],

  // ─── OBSERVABILITY ──────────────────────────────────────────

  "obs-streaming": [
    { type: "text", value: "Using stream=True and stream_events=True for real-time feedback." }
  ],

  "obs-tui": [
    { type: "text", value: "The 'mtp tui' command for interactive agent development." }
  ],

  "obs-logs": [
    { type: "text", value: "Configuring structured logging for production monitoring." }
  ],

  "obs-traces": [
    { type: "text", value: "Integrating with OpenTelemetry for distributed tracing." }
  ],

  "obs-dag-viz": [
    { type: "text", value: "Generating visual representations of execution plans." }
  ],

  // ─── EXAMPLES ───────────────────────────────────────────────

  "example-research": [
    { type: "text", value: "Research agent using web search and summarization." }
  ],

  "example-coding": [
    { type: "text", value: "Agent for automated code generation and test execution." }
  ],

  "example-filesystem": [
    { type: "text", value: "Safe file operations with destructive action protection." }
  ],

  "example-fallback": [
    { type: "text", value: "Multi-provider setups with automatic failover." }
  ],

  "example-approval": [
    { type: "text", value: "Workflow requiring manual sign-off for financial transactions." }
  ],

  "example-enterprise": [
    { type: "text", value: "Complete enterprise setup with SQL persistence and RBAC." }
  ],

  architecture: [
    { type: "heading", value: "System Architecture" },
    { type: "text", value: "MTPX is built on a 10-layer protocol stack, ensuring clean isolation of concerns." },
    { type: "list", value: "", items: [
      "Providers convert model responses into AgentAction. They do not execute tools.",
      "Toolkits own tool specs and handlers. They avoid provider-specific assumptions.",
      "Runtime is the single source of truth for plan execution.",
      "Agent is the orchestration loop only. No provider-specific parsing logic.",
      "Transport handles message ingress/egress only. No business logic.",
    ]},
  ],
};
