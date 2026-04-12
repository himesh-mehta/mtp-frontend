"use client";

import { motion, Variants } from "framer-motion";
import { BubbleBackground } from "@/components/BubbleBackground";
import { MarketingNavbar } from "@/components/MarketingNavbar";
import { Terminal, Zap, Layers, ArrowRight, Shield, GitMerge, Database, Bot, CheckCircle2, ChevronRight } from "lucide-react";
import Link from "next/link";

const fadeUp: Variants = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.8, ease: "easeOut" } }
};

export default function MTPLanding() {
  return (
    <div className="relative min-h-screen bg-[#0a0a0a] text-white selection:bg-tertiary selection:text-black overflow-x-hidden font-sans">
      <BubbleBackground />
      <MarketingNavbar />
      
      <main className="relative z-10 flex flex-col items-center w-full">
        
        {/* SECTION 1: HERO */}
        <section className="w-full max-w-7xl mx-auto px-6 pt-32 pb-24 md:pt-48 md:pb-32 flex flex-col items-center justify-center text-center">
          <motion.div initial="hidden" animate="visible" variants={fadeUp} className="flex flex-col items-center">
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight mb-6 leading-[1.15] drop-shadow-2xl max-w-4xl">
              Orchestrate AI execution.
            </h1>
            
            <p className="text-lg md:text-xl text-white/60 max-w-2xl mb-12 leading-relaxed">
              MTP transforms language models from conversational wrappers into structured execution systems. Construct workflows, manage tool dependencies, and execute real tasks deterministically.
            </p>

            <div className="flex flex-col sm:flex-row items-center gap-4">
              <Link href="/docs" className="group relative">
                <div className="absolute inset-0 bg-tertiary blur-xl opacity-50 group-hover:opacity-100 transition-opacity rounded-full duration-500" />
                <button className="relative bg-tertiary text-black font-semibold px-8 py-4 rounded-full flex items-center gap-2 hover:scale-105 transition-transform duration-300">
                  <Terminal className="size-5" />
                  Get Started
                </button>
              </Link>
              
              <Link href="/dashboard">
                <button className="px-8 py-4 rounded-full border border-white/10 bg-white/5 hover:bg-white/10 text-white font-medium transition-all duration-300 hover:scale-105 backdrop-blur-md">
                  View Docs
                </button>
              </Link>
            </div>
          </motion.div>
        </section>

        {/* SECTION 2: WHAT IS MTP */}
        <section className="w-full max-w-4xl mx-auto px-6 py-24 text-center">
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp}>
            <p className="text-2xl md:text-3xl font-light leading-relaxed text-white/80">
              MTP is a standardized agent orchestration framework designed for production environments.
            </p>
            <p className="text-lg text-white/50 mt-6 leading-relaxed max-w-3xl mx-auto">
              It explicitly decouples language model reasoning from environment execution. Instead of relying on a model to blindly trigger direct tool calls, MTP requires models to output structured execution plans. This separation of concerns allows the underlying runtime to validate schemas, parallelize tasks, and enforce strict execution policies before any code runs.
            </p>
          </motion.div>
        </section>

        {/* SECTION 3: HOW IT WORKS & SECTION 4: CODE EXAMPLE */}
        <section className="w-full max-w-6xl mx-auto px-6 py-32 grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp}>
            <h2 className="text-3xl font-bold mb-8">How it works</h2>
            <div className="space-y-6">
              {[
                { step: "1", title: "Instruction", desc: "The system receives user input and environment context." },
                { step: "2", title: "Planning", desc: "The LLM generates a structured execution plan (DAG)." },
                { step: "3", title: "Execution", desc: "The MTP runtime validates dependencies and executes the tools." },
                { step: "4", title: "Context", desc: "Execution results are appended back into memory state." },
                { step: "5", title: "Resolution", desc: "The loop continues recursively until the objective is complete." },
              ].map((item) => (
                <div key={item.step} className="flex items-start gap-4">
                  <div className="flex-shrink-0 size-8 rounded-full bg-white/5 border border-white/10 flex items-center justify-center font-mono text-sm text-tertiary">
                    {item.step}
                  </div>
                  <div>
                    <h3 className="font-semibold text-white/90">{item.title}</h3>
                    <p className="text-sm text-white/50">{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="relative group">
            <div className="absolute inset-0 bg-tertiary blur-[100px] opacity-10 group-hover:opacity-20 transition-opacity duration-1000 rounded-3xl" />
            <div className="relative rounded-2xl border border-white/10 bg-[#050505]/90 backdrop-blur-xl overflow-hidden shadow-2xl">
              <div className="flex items-center px-4 py-3 border-b border-white/5 bg-[#0a0a0a]">
                <div className="flex gap-2">
                  <div className="size-3 rounded-full bg-white/20" />
                  <div className="size-3 rounded-full bg-white/20" />
                  <div className="size-3 rounded-full bg-white/20" />
                </div>
                <div className="mx-auto text-xs font-mono text-white/40">execution_plan.json</div>
              </div>
              <div className="p-6 font-mono text-sm overflow-x-auto text-white/70 leading-loose">
                <span className="text-white">{"{"}</span><br />
                <span className="text-tertiary ml-4">"plan"</span><span className="text-white">: [</span><br />
                <span className="ml-8 text-white">{"{"}</span><br />
                <span className="text-tertiary ml-12">"step_id"</span><span className="text-white">: </span><span className="text-green-400">"fetch_system_logs"</span>,<br />
                <span className="text-tertiary ml-12">"tool"</span><span className="text-white">: </span><span className="text-green-400">"read_file"</span>,<br />
                <span className="text-tertiary ml-12">"args"</span><span className="text-white">: {"{"} </span><span className="text-tertiary">"path"</span><span className="text-white">: </span><span className="text-green-400">"/var/log/syslog"</span><span className="text-white"> {"}"}</span><br />
                <span className="ml-8 text-white">{"},"}</span><br />
                <span className="ml-8 text-white">{"{"}</span><br />
                <span className="text-tertiary ml-12">"step_id"</span><span className="text-white">: </span><span className="text-green-400">"analyze_error"</span>,<br />
                <span className="text-tertiary ml-12">"tool"</span><span className="text-white">: </span><span className="text-green-400">"diagnose_trace"</span>,<br />
                <span className="text-tertiary ml-12">"args"</span><span className="text-white">: {"{"}</span><br />
                <span className="text-tertiary ml-16">"log_data"</span><span className="text-white">: {"{"} </span><span className="text-tertiary">"$ref"</span><span className="text-white">: </span><span className="text-green-400">"fetch_system_logs"</span><span className="text-white"> {"}"}</span><br />
                <span className="ml-12 text-white">{"}"}</span><br />
                <span className="ml-8 text-white">{"}"}</span><br />
                <span className="ml-4 text-white">]</span><br />
                <span className="text-white">{"}"}</span>
              </div>
            </div>
          </motion.div>
        </section>

        {/* SECTION 5: CORE FEATURES */}
        <section className="w-full max-w-7xl mx-auto px-6 py-24">
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="text-center mb-16">
            <h2 className="text-3xl font-bold mb-4">Core Architecture</h2>
          </motion.div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { icon: Layers, title: "Tool Orchestration", desc: "Dynamically load, cache, and coordinate thousands of tools securely via unified schemas." },
              { icon: GitMerge, title: "Execution Plans (DAG)", desc: "Map complex batch executions using verifiable graph-based dependency resolution." },
              { icon: Bot, title: "Multi-Model Support", desc: "Abstract provider logic. Seamlessly interchange 12+ foundation models without refactoring code." },
              { icon: Shield, title: "Safety Policies", desc: "Enforce rigorous Allow, Ask, and Deny rule configurations on specific tool parameters." },
              { icon: Database, title: "Persistence", desc: "Maintain precise loop state bridging JSON, PostgreSQL, and MySQL session adapters natively." }
            ].map((feature, idx) => (
              <motion.div 
                key={idx} 
                initial="hidden" whileInView="visible" viewport={{ once: true }} 
                variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0, transition: { delay: idx * 0.1 } } }}
                className="p-8 rounded-2xl bg-white/[0.02] border border-white/5 hover:bg-white/[0.04] transition-colors"
              >
                <feature.icon className="size-6 text-tertiary mb-4" />
                <h3 className="font-semibold text-lg mb-2">{feature.title}</h3>
                <p className="text-sm text-white/50 leading-relaxed">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </section>

        {/* SECTION 6: WHY MTP & SECTION 7: USE CASES */}
        <section className="w-full max-w-7xl mx-auto px-6 py-32 grid grid-cols-1 lg:grid-cols-2 gap-16">
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp}>
            <h2 className="text-3xl font-bold mb-8">Normal AI vs. MTP</h2>
            <div className="space-y-4">
              {[
                { old: "Probabilistic text generation", new: "Deterministic task execution" },
                { old: "Unstructured sequence calls", new: "DAG-based workflows" },
                { old: "Ephemeral stateless memory", new: "Persistent database state" },
                { old: "Trust-based black-box access", new: "Policy-driven execution control" },
              ].map((compare, idx) => (
                <div key={idx} className="flex items-center gap-4 p-4 rounded-xl bg-white/[0.02] border border-white/5">
                  <span className="flex-1 text-sm text-white/40 line-through decoration-white/20">{compare.old}</span>
                  <ChevronRight className="size-4 text-tertiary flex-shrink-0" />
                  <span className="flex-1 text-sm font-medium text-white">{compare.new}</span>
                </div>
              ))}
            </div>
          </motion.div>

          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp}>
            <h2 className="text-3xl font-bold mb-8">Use Cases</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {[
                { title: "Autonomous Agents", desc: "Deploy self-correcting loops that execute complex multi-step protocols reliably." },
                { title: "Workflow Automation", desc: "Deterministically bridge and orchestrate disconnected internal and third-party APIs." },
                { title: "Dev Assistants", desc: "Safely enable iterative execution across read/write terminal and filesystem operations." },
                { title: "Research Agents", desc: "Construct deeply persistent web-scraping agents that retain context over endless sessions." },
              ].map((useCase, idx) => (
                <div key={idx} className="p-6 rounded-xl border border-white/10 bg-gradient-to-br from-white/5 to-transparent">
                  <h3 className="font-semibold mb-2">{useCase.title}</h3>
                  <p className="text-xs text-white/60 leading-relaxed">{useCase.desc}</p>
                </div>
              ))}
            </div>
          </motion.div>
        </section>

        {/* SECTION 8: QUICKSTART */}
        <section className="w-full max-w-4xl mx-auto px-6 py-24 text-center">
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp}>
            <h2 className="text-3xl font-bold mb-4">Start Building</h2>
            <p className="text-white/50 mb-8">Shift into production agent orchestrations in under a minute.</p>
            
            <div className="max-w-md mx-auto text-left relative group">
              <div className="absolute inset-0 bg-tertiary blur-3xl opacity-5 group-hover:opacity-10 transition-opacity rounded-2xl pointer-events-none" />
              <div className="bg-[#050505] border border-white/10 rounded-2xl p-6 font-mono text-sm shadow-xl relative">
                <div className="flex items-center gap-4 text-white/40 mb-2">
                  <span>bash</span>
                </div>
                <div className="text-white">
                  <span className="text-tertiary mr-2">$</span>pip install mtpx<br />
                  <span className="text-tertiary mr-2">$</span>python -m mtp init<br />
                  <span className="text-tertiary mr-2">$</span>python agent.py
                </div>
              </div>
            </div>
          </motion.div>
        </section>

        {/* SECTION 9: FINAL CTA */}
        <section className="w-full max-w-4xl mx-auto px-6 py-32 text-center border-t border-white/[0.02]">
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} className="flex flex-col items-center">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">Models reason. MTP executes.</h2>
            <p className="text-lg text-white/50 mb-10 max-w-xl mx-auto">
              Stop building chatbots. Start shipping structured execution pipelines.
            </p>
            
            <div className="flex gap-4">
              <Link href="/dashboard">
                <button className="group relative">
                  <div className="absolute inset-0 bg-white blur-xl opacity-20 group-hover:opacity-40 transition-opacity duration-500 rounded-full" />
                  <div className="relative bg-white text-black font-semibold px-8 py-3 rounded-full flex items-center gap-2 hover:scale-105 active:scale-95 transition-all">
                    Get Started
                    <ArrowRight className="size-4" />
                  </div>
                </button>
              </Link>
              <Link href="/docs">
                <button className="px-8 py-3 rounded-full border border-white/10 bg-white/5 hover:bg-white/10 text-white font-medium transition-all duration-300 hover:scale-105">
                  View Docs
                </button>
              </Link>
            </div>
          </motion.div>
        </section>

      </main>
    </div>
  );
}
