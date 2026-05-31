export interface Model {
  name: string;
  contextWindow: string;
  capabilities: string[];
}

export interface Provider {
  name: string;
  alias: string;
  sdkSnippet: string;
  modelCount: number;
  models: Model[];
  icon: string;
  color: string;
}

export const providers: Provider[] = [
  {
    name: "Groq",
    alias: "Groq",
    sdkSnippet: "mtpx[groq]",
    modelCount: 4,
    icon: "⚡",
    color: "#f55036",
    models: [
      { name: "llama-3.3-70b-versatile", contextWindow: "128k", capabilities: ["streaming", "function-calling"] },
      { name: "mixtral-8x7b-32768", contextWindow: "32k", capabilities: ["streaming"] },
      { name: "llama3-70b-8192", contextWindow: "8k", capabilities: ["streaming", "function-calling"] },
      { name: "gemma2-9b-it", contextWindow: "8k", capabilities: ["streaming"] },
    ]
  },
  {
    name: "OpenAI",
    alias: "OpenAI",
    sdkSnippet: "mtpx[openai]",
    modelCount: 5,
    icon: "🤖",
    color: "#10a37f",
    models: [
      { name: "gpt-4o", contextWindow: "128k", capabilities: ["vision", "streaming", "function-calling"] },
      { name: "gpt-4o-mini", contextWindow: "128k", capabilities: ["vision", "streaming", "function-calling"] },
      { name: "o1-preview", contextWindow: "128k", capabilities: ["reasoning", "streaming"] },
      { name: "gpt-4-turbo", contextWindow: "128k", capabilities: ["vision", "streaming", "function-calling"] },
      { name: "gpt-3.5-turbo", contextWindow: "16k", capabilities: ["streaming", "function-calling"] },
    ]
  },
  {
    name: "Anthropic",
    alias: "Anthropic",
    sdkSnippet: "mtpx[anthropic]",
    modelCount: 3,
    icon: "🧠",
    color: "#d97757",
    models: [
      { name: "claude-3-5-sonnet-latest", contextWindow: "200k", capabilities: ["vision", "streaming", "function-calling"] },
      { name: "claude-3-opus-latest", contextWindow: "200k", capabilities: ["vision", "streaming", "function-calling"] },
      { name: "claude-3-haiku-latest", contextWindow: "200k", capabilities: ["vision", "streaming", "function-calling"] },
    ]
  },
  {
    name: "Google Gemini",
    alias: "Gemini",
    sdkSnippet: "mtpx[gemini]",
    modelCount: 3,
    icon: "✨",
    color: "#4f8ef7",
    models: [
      { name: "gemini-1.5-pro", contextWindow: "2M", capabilities: ["vision", "streaming", "function-calling"] },
      { name: "gemini-1.5-flash", contextWindow: "1M", capabilities: ["vision", "streaming", "function-calling"] },
      { name: "gemini-2.0-flash-exp", contextWindow: "1M", capabilities: ["vision", "streaming", "function-calling"] },
    ]
  },
  {
    name: "Mistral",
    alias: "Mistral",
    sdkSnippet: "mtpx[mistral]",
    modelCount: 3,
    icon: "🌊",
    color: "#ff7000",
    models: [
      { name: "mistral-large-latest", contextWindow: "128k", capabilities: ["streaming", "function-calling"] },
      { name: "pixtral-large-latest", contextWindow: "128k", capabilities: ["vision", "streaming"] },
      { name: "codestral-latest", contextWindow: "32k", capabilities: ["streaming", "function-calling"] },
    ]
  },
  {
    name: "Cohere",
    alias: "Cohere",
    sdkSnippet: "mtpx[cohere]",
    modelCount: 2,
    icon: "🔗",
    color: "#39c5bb",
    models: [
      { name: "command-r-plus", contextWindow: "128k", capabilities: ["streaming", "function-calling"] },
      { name: "command-r", contextWindow: "128k", capabilities: ["streaming", "function-calling"] },
    ]
  },
  {
    name: "OpenRouter",
    alias: "OpenRouter",
    sdkSnippet: "mtpx[openrouter]",
    modelCount: 3,
    icon: "🔀",
    color: "#6366f1",
    models: [
      { name: "openai/gpt-4o", contextWindow: "128k", capabilities: ["vision", "streaming", "function-calling"] },
      { name: "anthropic/claude-3.5-sonnet", contextWindow: "200k", capabilities: ["vision", "streaming", "function-calling"] },
      { name: "meta-llama/llama-3.3-70b-instruct", contextWindow: "128k", capabilities: ["streaming", "function-calling"] },
    ]
  },
  {
    name: "DeepSeek",
    alias: "DeepSeek",
    sdkSnippet: "mtpx[deepseek]",
    modelCount: 2,
    icon: "🔭",
    color: "#00bcd4",
    models: [
      { name: "deepseek-chat", contextWindow: "64k", capabilities: ["streaming", "function-calling"] },
      { name: "deepseek-reasoner", contextWindow: "64k", capabilities: ["reasoning", "streaming"] },
    ]
  },
  {
    name: "Together AI",
    alias: "TogetherAI",
    sdkSnippet: "mtpx[togetherai]",
    modelCount: 3,
    icon: "🤝",
    color: "#8b5cf6",
    models: [
      { name: "llama-3.3-70b-instruct-turbo", contextWindow: "128k", capabilities: ["streaming", "function-calling"] },
      { name: "mixtral-8x7b-instruct-v0.1", contextWindow: "32k", capabilities: ["streaming"] },
      { name: "Qwen/Qwen2.5-72B-Instruct-Turbo", contextWindow: "128k", capabilities: ["streaming", "function-calling"] },
    ]
  },
  {
    name: "Fireworks AI",
    alias: "FireworksAI",
    sdkSnippet: "mtpx[fireworksai]",
    modelCount: 2,
    icon: "🎆",
    color: "#ec4899",
    models: [
      { name: "accounts/fireworks/models/llama-v3p3-70b-instruct", contextWindow: "128k", capabilities: ["streaming", "function-calling"] },
      { name: "accounts/fireworks/models/qwen2p5-72b-instruct", contextWindow: "128k", capabilities: ["streaming", "function-calling"] },
    ]
  },
  {
    name: "Ollama",
    alias: "Ollama",
    sdkSnippet: "mtpx[ollama]",
    modelCount: 3,
    icon: "🦙",
    color: "#84cc16",
    models: [
      { name: "llama3.3", contextWindow: "128k", capabilities: ["streaming", "function-calling"] },
      { name: "mistral", contextWindow: "32k", capabilities: ["streaming", "function-calling"] },
      { name: "qwen2.5", contextWindow: "128k", capabilities: ["streaming", "function-calling"] },
    ]
  },
  {
    name: "LM Studio",
    alias: "LMStudio",
    sdkSnippet: "mtpx[lmstudio]",
    modelCount: 2,
    icon: "🖥",
    color: "#a78bfa",
    models: [
      { name: "local models (OpenAI-compat)", contextWindow: "varies", capabilities: ["streaming", "function-calling"] },
      { name: "lmstudio-community/*", contextWindow: "varies", capabilities: ["streaming"] },
    ]
  },
  {
    name: "SambaNova",
    alias: "SambaNova",
    sdkSnippet: "mtpx[sambanova]",
    modelCount: 2,
    icon: "🚀",
    color: "#f59e0b",
    models: [
      { name: "Meta-Llama-3.1-70B-Instruct", contextWindow: "128k", capabilities: ["streaming", "function-calling"] },
      { name: "DeepSeek-V3", contextWindow: "64k", capabilities: ["streaming", "function-calling"] },
    ]
  },
  {
    name: "Cerebras",
    alias: "Cerebras",
    sdkSnippet: "mtpx[cerebras]",
    modelCount: 2,
    icon: "🧊",
    color: "#0ea5e9",
    models: [
      { name: "llama3.1-8b", contextWindow: "8k", capabilities: ["streaming"] },
      { name: "llama-3.3-70b", contextWindow: "128k", capabilities: ["streaming", "function-calling"] },
    ]
  },
  {
    name: "Xiaomi",
    alias: "Xiaomi",
    sdkSnippet: "mtpx[xiaomi]",
    modelCount: 2,
    icon: "📱",
    color: "#ff6900",
    models: [
      { name: "MiLM-7B", contextWindow: "8k", capabilities: ["streaming"] },
      { name: "local models (OpenAI-compat)", contextWindow: "varies", capabilities: ["streaming"] },
    ]
  },
];
