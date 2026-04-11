"use client";

import { motion } from "framer-motion";
import { BubbleBackground } from "@/components/BubbleBackground";
import { MarketingNavbar } from "@/components/MarketingNavbar";
import { Terminal, Zap, Layers, ArrowRight, Shield, Cpu } from "lucide-react";
import Link from "next/link";

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.8, ease: "easeOut" } }
};

export default function AntigravityLanding() {
  return (
    <div className="relative min-h-screen bg-[#0a0a0a] text-white selection:bg-tertiary selection:text-black overflow-x-hidden font-sans">
      <BubbleBackground />
      <MarketingNavbar />
      
      {/* 
        Z-Index Layering:
        BubbleBackground is z-0
        Content is z-10 
      */}
      <main className="relative z-10 flex flex-col items-center w-full">
        
        {/* HERO SECTION */}
        <section className="w-full max-w-7xl mx-auto px-6 h-screen flex flex-col items-center justify-center text-center pt-20">
          <motion.div 
            initial="hidden" 
            animate="visible" 
            variants={fadeUp}
            className="flex flex-col items-center"
          >
            <div className="px-4 py-1.5 rounded-full border border-tertiary/30 bg-tertiary/10 text-tertiary text-xs font-semibold tracking-widest uppercase mb-8 backdrop-blur-md">
              MTPX is now available
            </div>
            
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight mb-6 leading-[1.15] drop-shadow-2xl max-w-4xl">
              The definitive protocol for <br className="hidden md:block" />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-tertiary via-white to-white">
                agent tool orchestration.
              </span>
            </h1>
            
            <p className="text-lg md:text-xl text-white/50 max-w-2xl mb-12 leading-relaxed">
              Build, run, and scale policy-aware AI workflows seamlessly. Featuring lazy tool loading, dependency-aware batch execution, and native support for 12+ providers.
            </p>

            <div className="flex flex-col sm:flex-row items-center gap-4">
              <Link href="/docs" className="group relative">
                <div className="absolute inset-0 bg-tertiary blur-xl opacity-50 group-hover:opacity-100 transition-opacity rounded-full duration-500" />
                <button className="relative bg-tertiary text-black font-semibold px-8 py-4 rounded-full flex items-center gap-2 hover:scale-105 transition-transform duration-300">
                  <Terminal className="size-5" />
                  Go to docs
                </button>
              </Link>
              
              <Link href="/dashboard">
                <button className="px-8 py-4 rounded-full border border-white/10 bg-white/5 hover:bg-white/10 text-white font-medium transition-all duration-300 hover:scale-105 backdrop-blur-md">
                  Explore use cases
                </button>
              </Link>
            </div>
          </motion.div>
        </section>

        {/* FEATURES GRID */}
        <section className="w-full max-w-7xl mx-auto px-6 py-32 flex flex-col items-center">
          <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-100px" }}
            variants={fadeUp}
            className="text-center mb-20"
          >
            <h2 className="text-3xl md:text-4xl font-bold mb-6">Designed for enterprise agents.</h2>
            <p className="text-white/50 text-lg max-w-2xl mx-auto">MTP provides a standardized architecture for executing complex, multi-round tools across a highly secure protocol extension.</p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full">
            {[
              { icon: Layers, title: "Dependency-Aware Execution", desc: "Batch multiple tools in parallel by automatically mapping and resolving execution dependencies." },
              { icon: Shield, title: "Policy-Aware Routing", desc: "Rigorous execution control with Allow, Ask, and Deny security policies evaluated before any tool interacts with local systems." },
              { icon: Zap, title: "Multi-Round Orchestration", desc: "Seamless recursive model-tool-model loops structured to handle multi-step planning naturally." }
            ].map((Feature, i) => (
              <motion.div
                key={i}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true, margin: "-50px" }}
                variants={{
                  hidden: { opacity: 0, y: 30 },
                  visible: { opacity: 1, y: 0, transition: { duration: 0.6, delay: i * 0.2 } }
                }}
                className="group p-8 rounded-3xl border border-white/10 bg-white/[0.02] hover:bg-white/[0.04] transition-colors relative overflow-hidden backdrop-blur-sm"
              >
                <div className="absolute top-0 right-0 w-32 h-32 bg-tertiary/10 blur-[50px] opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none" />
                <Feature.icon className="size-8 text-tertiary mb-6" />
                <h3 className="text-xl font-bold mb-3">{Feature.title}</h3>
                <p className="text-white/50 leading-relaxed">{Feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </section>

        {/* UI PREVIEW SECTION */}
        <section className="w-full max-w-6xl mx-auto px-4 py-32 flex flex-col items-center">
          <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeUp}
            className="w-full relative group"
          >
            {/* Massive Soft Glow behind IDE */}
            <div className="absolute inset-0 bg-tertiary blur-[120px] opacity-10 group-hover:opacity-20 transition-opacity duration-1000 pointer-events-none rounded-[3rem]" />
            
            {/* The IDE Window */}
            <div className="relative rounded-[2rem] border border-white/10 bg-[#050505]/80 backdrop-blur-xl shadow-2xl overflow-hidden flex flex-col">
              {/* Window Controls */}
              <div className="h-12 border-b border-white/10 flex items-center px-6 gap-2 bg-[#0a0a0a]/50">
                <div className="size-3 rounded-full bg-white/20" />
                <div className="size-3 rounded-full bg-white/20" />
                <div className="size-3 rounded-full bg-white/20" />
                <div className="mx-auto text-xs text-white/30 font-mono">mtp-playground.ts</div>
              </div>
              
              {/* Code Panel Fake UI */}
              <div className="flex h-[500px]">
                {/* Sidebar File Tree */}
                <div className="w-64 border-r border-white/5 p-4 flex flex-col gap-2 font-mono text-sm hidden md:flex">
                  <div className="text-white/30 mb-2 uppercase text-xs">Explorer</div>
                  <div className="text-white/70 flex items-center gap-2"><Cpu className="size-4 text-tertiary" /> main.ts</div>
                  <div className="text-white/40 flex items-center gap-2 px-6">router.ts</div>
                  <div className="text-white/40 flex items-center gap-2 px-6">config.json</div>
                </div>
                {/* Editor Content */}
                <div className="flex-1 p-8 font-mono text-sm leading-relaxed overflow-hidden">
                  <div className="text-tertiary">import</div> <div className="text-white inline">{"{ orchestrate }"}</div> <div className="text-tertiary inline">from</div> <div className="text-green-400">"@mtp/core"</div>;
                  <br /><br />
                  <div className="text-tertiary inline">const</div> <div className="text-white inline">agent = await orchestrate({"{"}</div>
                  <br />
                  <div className="ml-4 text-white/50">provider:</div> <div className="text-green-400">"anthropic"</div><div className="text-white">,</div>
                  <br />
                  <div className="ml-4 text-white/50">model:</div> <div className="text-green-400">"claude-3-opus"</div><div className="text-white">,</div>
                  <br />
                  <div className="ml-4 text-white/50">tools:</div> <div className="text-white">[fileSystem, bash, github]</div>
                  <br />
                  <div className="text-white">{"});"}</div>
                  <br /><br />
                  <div className="text-white/30">{"// Awaiting instructions..."}</div>
                  <div className="flex items-center gap-2 mt-2">
                    <div className="size-2 bg-tertiary rounded-full animate-pulse" />
                    <div className="text-tertiary">agent is active</div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </section>

        {/* FINAL CTA SECTION */}
        <section className="w-full max-w-4xl mx-auto px-6 py-48 text-center">
          <motion.div
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={fadeUp}
            className="flex flex-col items-center"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">Ready to deploy?</h2>
            <p className="text-lg text-white/50 mb-10 max-w-xl mx-auto">Join thousands of engineers building the next generation of multi-agent software.</p>
            
            <Link href="/dashboard">
              <button className="group relative">
                <div className="absolute inset-0 bg-white blur-xl opacity-20 group-hover:opacity-40 transition-opacity duration-500 rounded-full" />
                <div className="relative bg-white text-black font-bold text-lg px-12 py-5 rounded-full flex items-center gap-3 hover:scale-105 active:scale-95 transition-all">
                  Get Started Free
                  <ArrowRight className="size-5 group-hover:translate-x-1 transition-transform" />
                </div>
              </button>
            </Link>
          </motion.div>
        </section>

      </main>
    </div>
  );
}
