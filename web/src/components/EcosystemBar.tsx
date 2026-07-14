import React from 'react';
import { ShieldCheck, HardDrive } from 'lucide-react';

export default function EcosystemBar() {
  return (
    <section id="ecosystem-section" className="w-full border-b border-[#27272A] bg-[#09090B]/40 py-10">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center justify-between gap-6 md:flex-row">
          {/* Section title */}
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-md border border-[#27272A] bg-[#18181B] text-[#A1A1AA]">
              <HardDrive className="h-4 w-4 text-[#10B981]" />
            </div>
            <div>
              <p className="font-mono text-xs font-bold uppercase tracking-wider text-[#A1A1AA]">
                Compatibility Layer
              </p>
              <h3 className="font-mono text-sm font-semibold text-[#FAFAFA]">
                Scans 4 Core Ecosystems
              </h3>
            </div>
          </div>

          {/* Grayscale -> Colored Grid */}
          <div className="grid w-full grid-cols-2 gap-4 sm:grid-cols-4 md:w-auto md:flex md:items-center md:gap-8">
            {/* Node.js */}
            <div
              id="eco-node"
              className="group flex flex-col items-start rounded-lg border border-[#27272A] bg-[#18181B]/50 p-3 md:border-0 md:bg-transparent md:p-0 transition-all duration-300"
            >
              <div className="flex items-center gap-2">
                <svg
                  className="h-5 w-5 fill-current text-[#A1A1AA] group-hover:text-[#10B981] transition-colors"
                  viewBox="0 0 24 24"
                >
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 14.25c0 .41-.34.75-.75.75s-.75-.34-.75-.75V11c0-.41.34-.75.75-.75s.75.34.75.75v5.25zm-.25-7.5c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1z" />
                </svg>
                <span className="font-mono text-sm font-semibold text-[#A1A1AA] group-hover:text-[#FAFAFA] transition-colors">
                  Node.js
                </span>
              </div>
              <span className="mt-1 font-mono text-[10px] text-[#A1A1AA] group-hover:text-[#10B981]/80 transition-colors">
                node_modules
              </span>
            </div>

            {/* Rust Cargo */}
            <div
              id="eco-rust"
              className="group flex flex-col items-start rounded-lg border border-[#27272A] bg-[#18181B]/50 p-3 md:border-0 md:bg-transparent md:p-0 transition-all duration-300"
            >
              <div className="flex items-center gap-2">
                <svg
                  className="h-5 w-5 fill-current text-[#A1A1AA] group-hover:text-amber-500 transition-colors"
                  viewBox="0 0 24 24"
                >
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z" />
                </svg>
                <span className="font-mono text-sm font-semibold text-[#A1A1AA] group-hover:text-[#FAFAFA] transition-colors">
                  Rust Cargo
                </span>
              </div>
              <span className="mt-1 font-mono text-[10px] text-[#A1A1AA] group-hover:text-amber-500/80 transition-colors">
                target/ debug
              </span>
            </div>

            {/* Python venv */}
            <div
              id="eco-python"
              className="group flex flex-col items-start rounded-lg border border-[#27272A] bg-[#18181B]/50 p-3 md:border-0 md:bg-transparent md:p-0 transition-all duration-300"
            >
              <div className="flex items-center gap-2">
                <svg
                  className="h-5 w-5 fill-current text-[#A1A1AA] group-hover:text-blue-400 transition-colors"
                  viewBox="0 0 24 24"
                >
                  <path d="M12 2c5.52 0 10 4.48 10 10s-4.48 10-10 10S2 17.52 2 12 6.48 2 12 2zm0 18c3.31 0 6-2.69 6-6s-2.69-6-6-6-6 2.69-6 6 2.69 6 6 6zm-1-9H9v2h2v-2zm4 0h-2v2h2v-2z" />
                </svg>
                <span className="font-mono text-sm font-semibold text-[#A1A1AA] group-hover:text-[#FAFAFA] transition-colors">
                  Python
                </span>
              </div>
              <span className="mt-1 font-mono text-[10px] text-[#A1A1AA] group-hover:text-blue-400/80 transition-colors">
                .venv & __pycache__
              </span>
            </div>

            {/* Go Build */}
            <div
              id="eco-go"
              className="group flex flex-col items-start rounded-lg border border-[#27272A] bg-[#18181B]/50 p-3 md:border-0 md:bg-transparent md:p-0 transition-all duration-300"
            >
              <div className="flex items-center gap-2">
                <svg
                  className="h-5 w-5 fill-current text-[#A1A1AA] group-hover:text-sky-400 transition-colors"
                  viewBox="0 0 24 24"
                >
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z" />
                </svg>
                <span className="font-mono text-sm font-semibold text-[#A1A1AA] group-hover:text-[#FAFAFA] transition-colors">
                  Go Build
                </span>
              </div>
              <span className="mt-1 font-mono text-[10px] text-[#A1A1AA] group-hover:text-sky-400/80 transition-colors">
                pkg/mod & caches
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
