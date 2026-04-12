import { AnimatedCard } from "@/components/AnimatedCard";
import { Activity, Clock, Server, CheckCircle2, AlertTriangle } from "lucide-react";

export default function Dashboard() {
  return (
    <div className="min-h-[calc(100vh-64px)] bg-surface text-on-surface">
      <main className="max-w-[1600px] w-full mx-auto px-4 md:px-8 lg:px-16 py-12">
        <header className="mb-12">
          <h1 className="text-3xl font-semibold tracking-tight">System Dashboard</h1>
          <p className="text-on-surface-variant text-sm mt-2">Real-time metrics and provider health across MTP.</p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <AnimatedCard className="p-6">
            <div className="flex items-center gap-3 mb-4">
              <Activity className="size-5 text-tertiary" />
              <h2 className="text-sm font-medium text-on-surface-variant uppercase tracking-widest">Active Runs</h2>
            </div>
            <p className="text-4xl font-light tracking-tighter">1,024</p>
          </AnimatedCard>

          <AnimatedCard className="p-6" delay={0.1}>
            <div className="flex items-center gap-3 mb-4">
              <Clock className="size-5 text-primary" />
              <h2 className="text-sm font-medium text-on-surface-variant uppercase tracking-widest">Avg Latency</h2>
            </div>
            <p className="text-4xl font-light tracking-tighter">234<span className="text-lg text-on-surface-variant ml-1">ms</span></p>
          </AnimatedCard>

          <AnimatedCard className="p-6" delay={0.2}>
            <div className="flex items-center gap-3 mb-4">
              <Server className="size-5 text-primary" />
              <h2 className="text-sm font-medium text-on-surface-variant uppercase tracking-widest">Providers</h2>
            </div>
            <p className="text-4xl font-light tracking-tighter">12<span className="text-lg text-on-surface-variant ml-1">online</span></p>
          </AnimatedCard>

          <AnimatedCard className="p-6" delay={0.3}>
            <div className="flex items-center gap-3 mb-4">
              <AlertTriangle className="size-5 text-error-dim" />
              <h2 className="text-sm font-medium text-on-surface-variant uppercase tracking-widest">Error Rate</h2>
            </div>
            <p className="text-4xl font-light tracking-tighter">0.12<span className="text-lg text-on-surface-variant ml-1">%</span></p>
          </AnimatedCard>
        </div>

        <h2 className="text-xl font-medium tracking-tight mb-4 mt-12 border-b border-white/[0.05] pb-4">Provider Health</h2>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {[
            { name: "Groq", status: "Operational", lat: "14ms", p: "Llama 3 8B" },
            { name: "Cohere", status: "Operational", lat: "320ms", p: "Command R+" },
            { name: "Anthropic", status: "Operational", lat: "800ms", p: "Claude 3.5 Sonnet" },
            { name: "Together AI", status: "Degraded", lat: "1.2s", p: "Mixtral 8x7B", err: true }
          ].map((provider, i) => (
            <AnimatedCard key={provider.name} delay={0.4 + i * 0.1} className="p-4 flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="p-2 bg-surface-container-highest rounded-md border border-white/[0.05]">
                  <Server className="size-5 text-primary" />
                </div>
                <div>
                  <h3 className="font-medium text-on-surface">{provider.name}</h3>
                  <p className="text-xs text-on-surface-variant">{provider.p}</p>
                </div>
              </div>
              <div className="text-right flex flex-col items-end gap-1">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-mono text-on-surface-variant">{provider.lat}</span>
                  {provider.err ? (
                    <AlertTriangle className="size-4 text-error-dim" />
                  ) : (
                    <CheckCircle2 className="size-4 text-tertiary" />
                  )}
                </div>
                <span className={`text-xs uppercase tracking-wider ${provider.err ? 'text-error-dim' : 'text-tertiary'}`}>
                  {provider.status}
                </span>
              </div>
            </AnimatedCard>
          ))}
        </div>
      </main>
    </div>
  );
}
