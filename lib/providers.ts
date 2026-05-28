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
];
