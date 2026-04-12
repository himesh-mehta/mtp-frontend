"use client";

import Link from "next/link";
import { ChevronDown, Globe, Hexagon } from "lucide-react";

export function Navbar() {
  return (
    <nav className="sticky top-0 z-50 w-full h-16 border-b border-white/[0.08] bg-surface flex items-center justify-between px-4 md:px-6">
      
      {/* Left Base */}
      <div className="flex items-center gap-6">
        <Link href="/" className="flex items-center gap-2 group">
          <Hexagon className="size-6 text-tertiary fill-tertiary/20" />
          <span className="font-semibold text-lg tracking-tight text-on-surface">MTPDocs</span>
          <div className="flex items-center gap-1 text-on-surface-variant hover:text-on-surface ml-2 text-sm">
            <span>Platform</span>
            <ChevronDown className="size-3" />
          </div>
        </Link>
      </div>

      {/* Middle Pills Nav */}
      <div className="hidden md:flex flex-1 items-center justify-center gap-1">
        {[
          { name: "Build", active: true },
          { name: "Admin" },
          { name: "Models & pricing" },
          { name: "Client SDKs" },
          { name: "API Reference" },
        ].map((item) => (
          <button
            key={item.name}
            className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
              item.active 
                ? "bg-surface-container-highest text-on-surface" 
                : "text-on-surface-variant hover:text-on-surface hover:bg-surface-container-low"
            }`}
          >
            {item.name}
          </button>
        ))}
      </div>

      {/* Right Controls */}
      <div className="flex items-center gap-4">
        <button className="hidden sm:flex items-center gap-1 text-sm text-on-surface-variant hover:text-on-surface">
          <Globe className="size-4" />
          <span>English</span>
          <ChevronDown className="size-3" />
        </button>
        <button className="bg-white text-black hover:bg-white/90 text-sm font-medium px-4 py-1.5 rounded-md transition-colors">
          Log In
        </button>
      </div>

    </nav>
  );
}

