"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { docSidebar } from "@/lib/docs-content";
import { Book, ChevronRight, Search } from "lucide-react";
import { useState } from "react";

export default function DocsLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const [searchQuery, setSearchQuery] = useState("");

  const currentSlug = pathname.split("/docs/")[1] || "introduction";

  const filteredSidebar = docSidebar
    .map((section) => ({
      ...section,
      items: section.items.filter(
        (item) =>
          !searchQuery ||
          item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          item.description.toLowerCase().includes(searchQuery.toLowerCase())
      ),
    }))
    .filter((section) => section.items.length > 0);

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Top Header */}
      <header className="fixed top-0 left-0 right-0 z-50 h-14 border-b border-white/[0.06] bg-black/80 backdrop-blur-xl flex items-center px-6">
        <Link href="/" className="flex items-center gap-2.5 mr-8">
          <Book className="size-5 text-tertiary" />
          <span className="font-semibold text-sm tracking-tight">MTP Docs</span>
        </Link>
        <nav className="hidden md:flex items-center gap-6 text-sm text-white/50">
          <Link href="/docs/introduction" className="hover:text-white transition-colors">Docs</Link>
          <Link href="/docs/agent-api" className="hover:text-white transition-colors">API Reference</Link>
          <Link href="/docs/quickstart" className="hover:text-white transition-colors">Guides</Link>
        </nav>
        <div className="ml-auto">
          <Link href="/" className="text-sm text-white/40 hover:text-white transition-colors">
            ← Back to Home
          </Link>
        </div>
      </header>

      <div className="flex pt-14">
        {/* Sidebar */}
        <aside className="fixed top-14 left-0 bottom-0 w-72 border-r border-white/[0.06] bg-black overflow-y-auto hidden lg:block">
          {/* Search */}
          <div className="p-4 border-b border-white/[0.06]">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 size-4 text-white/30" />
              <input
                type="text"
                placeholder="Search docs..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-white/[0.04] border border-white/[0.08] rounded-lg pl-10 pr-4 py-2 text-sm text-white placeholder:text-white/30 focus:outline-none focus:ring-1 focus:ring-tertiary/30 focus:border-tertiary/30 transition-all"
              />
              <kbd className="absolute right-3 top-1/2 -translate-y-1/2 text-[10px] text-white/20 border border-white/10 rounded px-1.5 py-0.5 font-mono">
                ⌘K
              </kbd>
            </div>
          </div>

          {/* Nav Groups */}
          <nav className="p-4 space-y-6">
            {filteredSidebar.map((section) => (
              <div key={section.title}>
                <h4 className="text-[11px] font-semibold text-white/40 uppercase tracking-[0.12em] mb-2 px-3">
                  {section.title}
                </h4>
                <ul className="space-y-0.5">
                  {section.items.map((item) => {
                    const isActive = currentSlug === item.slug;
                    return (
                      <li key={item.slug}>
                        <Link
                          href={`/docs/${item.slug}`}
                          className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-all group ${
                            isActive
                              ? "bg-white/[0.08] text-white font-medium"
                              : "text-white/50 hover:text-white/80 hover:bg-white/[0.03]"
                          }`}
                        >
                          {isActive && (
                            <div className="w-0.5 h-4 bg-tertiary rounded-full -ml-1 mr-1" />
                          )}
                          {item.title}
                          {isActive && (
                            <ChevronRight className="size-3 ml-auto text-white/30" />
                          )}
                        </Link>
                      </li>
                    );
                  })}
                </ul>
              </div>
            ))}
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 lg:ml-72 min-h-[calc(100vh-3.5rem)]">
          {children}
        </main>
      </div>
    </div>
  );
}
