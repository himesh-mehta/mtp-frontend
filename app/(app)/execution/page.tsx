import { AnimatedCard } from "@/components/AnimatedCard";
import { Activity, GitBranch, Terminal } from "lucide-react";

export default function ExecutionVisualizer() {
  return (
    <div className="min-h-[calc(100vh-64px)] bg-surface flex flex-col text-on-surface">
      <main className="flex-1 max-w-[1600px] mx-auto px-4 md:px-8 lg:px-16 py-12 w-full">
        <header className="mb-12 flex items-end justify-between border-b border-white/[0.05] pb-6">
          <div>
            <h1 className="text-3xl font-semibold tracking-tight mb-2">Execution Flow</h1>
            <p className="text-on-surface-variant text-sm">Visualizing active task resolution through the agent graph.</p>
          </div>
          <div className="flex items-center gap-2">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-tertiary opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-tertiary"></span>
            </span>
            <span className="text-xs font-medium uppercase tracking-widest text-tertiary">Live Processing</span>
          </div>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-[1fr_300px] gap-8">
          {/* Main Visualizer Area */}
          <div className="bg-surface-container-lowest border border-white/[0.05] rounded-xl p-8 relative min-h-[600px] flex flex-col items-center py-20">
            {/* Diagram Background Grid */}
            <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10 pointer-events-none" />
            
            <AnimatedCard className="p-4 w-64 border-primary/20 bg-surface-container flex flex-col items-center gap-2 z-10">
              <span className="text-xs font-mono uppercase tracking-widest text-primary">Entry</span>
              <p className="text-sm text-center">User Request Received</p>
            </AnimatedCard>

            <div className="w-px h-16 bg-gradient-to-b from-primary/50 to-tertiary/50" />

            <AnimatedCard delay={0.2} className="p-4 w-64 border-tertiary/20 bg-surface-container flex flex-col items-center gap-2 z-10">
              <span className="text-xs font-mono uppercase tracking-widest text-tertiary">Planning</span>
              <p className="text-sm text-center text-on-surface-variant">Decomposing intent into 3 steps</p>
            </AnimatedCard>

             <div className="w-px h-16 bg-gradient-to-b from-tertiary/50 to-white/10" />

             {/* Branching */}
             <div className="w-96 h-px bg-white/10 relative">
               <div className="absolute left-0 top-0 w-px h-16 bg-white/10" />
               <div className="absolute right-0 top-0 w-px h-16 bg-white/10" />
               <div className="absolute left-1/2 top-0 w-px h-16 bg-white/10" />
             </div>

             <div className="flex gap-4 w-[420px] justify-between">
                <AnimatedCard delay={0.4} className="p-4 w-[120px] bg-surface-container-low flex flex-col items-center gap-2">
                  <Terminal className="size-4 text-on-surface-variant" />
                  <span className="text-[10px] text-on-surface-variant font-mono">search_db</span>
                </AnimatedCard>
                <AnimatedCard delay={0.5} className="p-4 w-[120px] border-primary/40 bg-surface-container flex flex-col items-center gap-2">
                  <Activity className="size-4 text-primary" />
                  <span className="text-[10px] text-primary font-mono animate-pulse">read_logs</span>
                </AnimatedCard>
                <AnimatedCard delay={0.6} className="p-4 w-[120px] bg-surface-container-low flex flex-col items-center gap-2">
                  <GitBranch className="size-4 text-on-surface-variant" />
                  <span className="text-[10px] text-on-surface-variant font-mono">fork_req</span>
                </AnimatedCard>
             </div>
             
          </div>

          {/* Right sidebar details */}
          <div className="flex flex-col gap-4">
            <h3 className="text-sm font-semibold tracking-wider uppercase">Execution Log</h3>
            <div className="flex-1 bg-surface-container-low rounded-lg p-4 font-mono text-xs overflow-y-auto space-y-3">
              <div className="text-on-surface-variant"><span className="text-primary mr-2">[10:42:01]</span> Incoming payload detected.</div>
              <div className="text-on-surface-variant"><span className="text-primary mr-2">[10:42:01]</span> MTP Router mapping provider...</div>
              <div className="text-tertiary"><span className="text-primary mr-2">[10:42:02]</span> Routed to Anthropic (Claude 3.5 Sonnet).</div>
              <div className="text-on-surface-variant"><span className="text-primary mr-2">[10:42:03]</span> Agent returned 3 tool calls.</div>
              <div className="text-on-surface-variant"><span className="text-primary mr-2">[10:42:03]</span> Executing async: search_db</div>
              <div className="text-on-surface"><span className="text-primary mr-2">[10:42:04]</span> Executing async: read_logs <span className="animate-pulse">_</span></div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
