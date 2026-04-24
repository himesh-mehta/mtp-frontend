"use client";

import { BubbleBackground } from "@/components/BubbleBackground";
import { MarketingNavbar } from "@/components/MarketingNavbar";
import { HeroSection } from "@/components/sections/HeroSection";
import { ProvidersSection } from "@/components/sections/ProvidersSection";
import { TuiSection } from "@/components/sections/TuiSection";
import { FeaturesSection } from "@/components/sections/FeaturesSection";
import { CtaSection } from "@/components/sections/CtaSection";

export default function MTPLanding() {
  return (
    <div className="relative min-h-screen bg-[#030305] text-white overflow-x-hidden" style={{ fontFamily: "var(--font-display, 'Space Grotesk', ui-sans-serif)" }}>
      {/* Ambient background — needed for glass to work */}
      <BubbleBackground />

      {/* Deep ambient gradient blobs */}
      <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
        <div className="absolute top-0 left-1/4 w-[600px] h-[600px] rounded-full opacity-60"
          style={{ background: "radial-gradient(ellipse, rgba(79,142,247,0.07) 0%, transparent 70%)", transform: "translateY(-50%)" }} />
        <div className="absolute bottom-1/4 right-0 w-[500px] h-[500px] rounded-full opacity-60"
          style={{ background: "radial-gradient(ellipse, rgba(250,204,21,0.05) 0%, transparent 70%)" }} />
        <div className="absolute top-1/2 left-0 w-[400px] h-[400px] rounded-full opacity-40"
          style={{ background: "radial-gradient(ellipse, rgba(139,92,246,0.06) 0%, transparent 70%)" }} />
      </div>

      <MarketingNavbar />

      <main className="relative z-10 flex flex-col items-center w-full">
        <HeroSection />
        <FeaturesSection />
        <ProvidersSection />
        <TuiSection />
        <CtaSection />
      </main>
    </div>
  );
}
