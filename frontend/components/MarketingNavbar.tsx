"use client";

import Link from "next/link";
import { Hexagon } from "lucide-react";
import { motion, useScroll, useTransform } from "framer-motion";

export function MarketingNavbar() {
  const { scrollY } = useScroll();
  const background = useTransform(
    scrollY,
    [0, 50],
    ["rgba(0, 0, 0, 0)", "rgba(10, 10, 10, 0.8)"]
  );
  const border = useTransform(
    scrollY,
    [0, 50],
    ["rgba(255, 255, 255, 0)", "rgba(255, 255, 255, 0.05)"]
  );

  return (
    <motion.nav 
      style={{ background, borderColor: border }}
      className="fixed top-0 left-0 right-0 z-50 border-b backdrop-blur-md transition-all h-20 flex items-center px-6 md:px-12"
    >
      <div className="flex items-center justify-between w-full">
        {/* Left: Logo */}
        <Link href="/" className="flex items-center gap-3 group relative z-10">
          <div className="relative">
            <div className="absolute inset-0 bg-tertiary blur-lg opacity-40 group-hover:opacity-80 transition-opacity" />
            <Hexagon className="size-8 text-tertiary relative z-10 fill-tertiary/20" />
          </div>
          <span className="font-bold text-xl tracking-tight text-white drop-shadow-md">
            MTP Protocol
          </span>
        </Link>

        {/* Middle: Links */}
        <div className="hidden md:flex items-center gap-8 px-8 py-2 rounded-full border border-white/[0.05] bg-white/[0.02]">
          {["Product", "Use Cases", "Pricing", "Blog", "Resources"].map((item) => (
            <Link 
              key={item} 
              href="#" 
              className="text-sm font-medium text-white/70 hover:text-white hover:text-tertiary transition-colors"
            >
              {item}
            </Link>
          ))}
        </div>

        {/* Right: CTA */}
        <div className="flex items-center relative z-10">
          <Link href="/docs" className="group relative">
            <div className="absolute inset-0 bg-white blur-md opacity-20 group-hover:opacity-40 transition-opacity rounded-full" />
            <button className="relative bg-white text-black font-semibold text-sm px-6 py-2.5 rounded-full hover:scale-105 active:scale-95 transition-transform">
              Go to docs
            </button>
          </Link>
        </div>
      </div>
    </motion.nav>
  );
}
