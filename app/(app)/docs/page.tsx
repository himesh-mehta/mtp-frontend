import { CodeBlock } from "@/components/CodeBlock";

export default function Documentation() {
  return (
    <div className="min-h-[calc(100vh-64px)] bg-surface flex flex-col text-on-surface">
      <main className="flex-1 max-w-[1600px] w-full mx-auto p-4 md:p-8 lg:px-16 flex gap-12">
        
        {/* Sidebar Nav */}
        <aside className="hidden md:block w-64 flex-shrink-0 border-r border-white/[0.05] pr-6 pt-4">
          <nav className="space-y-8">
            <div>
              <h4 className="font-semibold text-on-surface mb-3 tracking-tight">Introduction</h4>
              <ul className="space-y-2 text-sm text-on-surface-variant">
                <li className="text-primary font-medium cursor-pointer">Getting Started</li>
                <li className="hover:text-primary transition-colors cursor-pointer">Core Concepts</li>
                <li className="hover:text-primary transition-colors cursor-pointer">Architecture</li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold text-on-surface mb-3 tracking-tight">Providers</h4>
              <ul className="space-y-2 text-sm text-on-surface-variant">
                <li className="hover:text-primary transition-colors cursor-pointer">OpenAI</li>
                <li className="hover:text-primary transition-colors cursor-pointer">Anthropic</li>
                <li className="hover:text-primary transition-colors cursor-pointer">Groq</li>
                <li className="hover:text-primary transition-colors cursor-pointer">Cohere</li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold text-on-surface mb-3 tracking-tight">Tools & MTP</h4>
              <ul className="space-y-2 text-sm text-on-surface-variant">
                <li className="hover:text-primary transition-colors cursor-pointer">Defining Tools</li>
                <li className="hover:text-primary transition-colors cursor-pointer">Tool Router</li>
                <li className="hover:text-primary transition-colors cursor-pointer">Error Handling</li>
              </ul>
            </div>
          </nav>
        </aside>

        {/* Article Content */}
        <article className="flex-1 max-w-3xl pt-4 pb-24">
          <p className="text-sm text-tertiary font-mono tracking-widest uppercase mb-2">Introduction / Getting Started</p>
          <h1 className="text-4xl md:text-5xl font-bold tracking-tighter mb-6 text-on-surface">Quickstart Guide</h1>
          
          <p className="text-lg text-on-surface-variant leading-relaxed mb-10">
            Learn how to initialize the Model Tool Protocol (MTP) and execute your first cross-provider agent instruction in under three minutes.
          </p>

          <section className="space-y-6">
            <h2 className="text-2xl font-semibold tracking-tight mt-12 mb-4">Installation</h2>
            <p className="text-on-surface-variant">
              MTP is available on PyPI. Install it using pip. We recommend using a virtual environment.
            </p>
            <CodeBlock 
              language="bash"
              code="pip install mtp-protocol"
            />
          </section>

          <section className="space-y-6">
            <h2 className="text-2xl font-semibold tracking-tight mt-12 mb-4">API Keys</h2>
            <p className="text-on-surface-variant">
              To use MTP, you'll need API keys for the providers you intend to orchestrate. Provide them via environment variables:
            </p>
            <CodeBlock 
              language="bash"
              code={`export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GROQ_API_KEY="gsk_..."`}
            />
          </section>

          <section className="space-y-6">
            <h2 className="text-2xl font-semibold tracking-tight mt-12 mb-4">Your First Agent</h2>
            <p className="text-on-surface-variant">
              Import the <code className="text-primary bg-surface-container-highest px-1.5 py-0.5 rounded text-sm font-mono">Agent</code> and <code className="text-primary bg-surface-container-highest px-1.5 py-0.5 rounded text-sm font-mono">Config</code> modules to get started. MTP naturally abstracts the underlying provider payload schemas.
            </p>
            <CodeBlock 
              language="python"
              code={`import os
from mtp import Config, ProviderType
from mtp.agent import create_agent

# Use Groq for ultra-low latency, fallback to Anthropic if rate-limited
config = Config(
    provider=ProviderType.GROQ,
    fallback=ProviderType.ANTHROPIC,
    verbose=True
)

agent = create_agent(config=config)
response = agent.execute("What are the core design philosophies of MTP?")

print(response.output)`}
            />
            
            <div className="mt-8 p-6 bg-surface-container-low border-l-4 border-l-primary rounded-r-lg">
              <h4 className="font-semibold text-on-surface mb-2">Next Steps</h4>
              <p className="text-sm text-on-surface-variant leading-relaxed">
                Now that you have a basic agent running, explore <span className="underline decoration-white/20 underline-offset-4 hover:text-primary cursor-pointer transition-colors">Defining Tools</span> to see how MTP provides functions safely to underlying models.
              </p>
            </div>
          </section>
        </article>
      </main>
    </div>
  );
}
