import React, { useState } from 'react';
import { Copy, Check, ExternalLink, ArrowRight, BookOpen, Star, HelpCircle } from 'lucide-react';
import { motion } from 'motion/react';

export default function HeroSection() {
  const [copied, setCopied] = useState(false);
  const commandText = 'npm install -g devklean';

  const handleCopy = () => {
    navigator.clipboard.writeText(commandText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const scrollToSection = (id: string) => {
    const el = document.getElementById(id);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <section id="hero-section" className="relative w-full overflow-hidden bg-[#09090B] pt-20 pb-28">
      {/* Background gradients for radial depth */}
      <div className="absolute top-0 left-1/4 -z-10 h-[500px] w-[500px] rounded-full bg-[#10B981]/5 blur-3xl"></div>
      <div className="absolute right-10 bottom-10 -z-10 h-[300px] w-[300px] rounded-full bg-blue-500/5 blur-3xl"></div>

      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        
        {/* Banner Announcement */}
        <div className="mb-8 flex justify-center lg:justify-start">
          <div className="inline-flex items-center gap-2 rounded-full border border-[#27272A] bg-[#18181B] px-3.5 py-1.5 font-mono text-xs text-[#FAFAFA]">
            <span className="flex h-2 w-2 rounded-full bg-[#10B981] animate-pulse"></span>
            <span className="text-[#10B981] font-semibold">NEW RELEASE:</span>
            <span>v1.2.0 is officially live with full Python .venv support</span>
          </div>
        </div>

        {/* Two-Column Desktop / Stacked Mobile Layout */}
        <div className="grid gap-12 lg:grid-cols-12 lg:items-center">
          
          {/* Left Column: Text & Primary CTA Actions */}
          <div className="space-y-6 lg:col-span-6 text-center lg:text-left">
            <h1 className="font-sans text-5xl md:text-7xl font-extrabold tracking-tight text-[#FAFAFA] leading-tight">
              Reclaim your <br className="hidden md:inline" />
              <span className="bg-gradient-to-r from-[#FAFAFA] via-[#FAFAFA] to-[#10B981] bg-clip-text text-transparent">
                local disk space.
              </span>
            </h1>

            <p className="font-sans text-base md:text-lg leading-relaxed text-[#A1A1AA] max-w-xl mx-auto lg:mx-0">
              The fastest way to safely scan and purge unused build artifacts from Node.js, Python, and Rust. Get gigabytes of local SSD back in seconds.
            </p>

            {/* CTAs and Copy Segment */}
            <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4 pt-2">
              {/* Custom Copy-to-Clipboard block */}
              <div
                id="hero-copy-snippet"
                className="group flex items-center justify-between rounded-lg border border-[#27272A] bg-[#18181B] px-4 py-3 font-mono text-xs text-[#10B981] w-full sm:w-auto sm:min-w-[280px]"
              >
                <div className="flex items-center gap-2">
                  <span className="text-[#A1A1AA] select-none">$</span>
                  <span className="text-[#FAFAFA] font-medium">{commandText}</span>
                </div>
                <button
                  id="btn-hero-copy"
                  onClick={handleCopy}
                  className="ml-4 rounded-md p-1.5 text-[#A1A1AA] hover:text-[#FAFAFA] hover:bg-[#27272A] transition-colors"
                  title="Copy installation CLI string"
                >
                  {copied ? (
                    <Check className="h-4 w-4 text-[#10B981]" />
                  ) : (
                    <Copy className="h-4 w-4 group-hover:scale-105 transition-transform" />
                  )}
                </button>
              </div>

              {/* Secondary Documentation Button */}
              <button
                id="btn-hero-docs"
                onClick={() => scrollToSection('demo-section')}
                className="flex items-center justify-center gap-2 rounded-lg border border-[#27272A] bg-transparent hover:bg-[#18181B] text-[#FAFAFA] px-5 py-3.5 text-xs font-semibold font-mono w-full sm:w-auto transition-all duration-200"
              >
                <BookOpen className="h-4 w-4 text-[#10B981]" />
                Interactive Demo
              </button>
            </div>

            {/* Micro proof counts */}
            <div className="flex items-center justify-center lg:justify-start gap-5 pt-4 text-xs font-mono text-[#A1A1AA]">
              <div className="flex items-center gap-1.5">
                <span className="text-[#10B981] font-bold">★ 4.8k</span> stars on GitHub
              </div>
              <div className="h-3 w-[1px] bg-[#27272A]"></div>
              <div className="flex items-center gap-1.5">
                <span className="text-[#10B981] font-bold">100%</span> open-source
              </div>
              <div className="h-3 w-[1px] bg-[#27272A]"></div>
              <div className="flex items-center gap-1.5">
                <span className="text-[#10B981] font-bold">0MB</span> telemetry
              </div>
            </div>

          </div>

          {/* Right Column: Visual Hero Terminal */}
          <div className="lg:col-span-6 flex justify-center">
            <div className="relative w-full max-w-lg">
              {/* Dynamic shadow glow beneath card */}
              <div className="absolute inset-0 rounded-xl bg-[#10B981]/5 blur-3xl -z-10 shadow-glow"></div>

              {/* Terminal Block */}
              <div
                id="hero-terminal"
                className="w-full rounded-xl border border-[#27272A] bg-[#000000] p-4 shadow-2xl relative"
              >
                {/* Mac top bar controls */}
                <div className="flex items-center justify-between border-b border-[#27272A]/70 pb-3 mb-4">
                  <div className="flex items-center gap-1.5">
                    <span className="h-3 w-3 rounded-full bg-[#EF4444] opacity-80"></span>
                    <span className="h-3 w-3 rounded-full bg-amber-500 opacity-80"></span>
                    <span className="h-3 w-3 rounded-full bg-[#10B981] opacity-80"></span>
                  </div>
                  <span className="font-mono text-[10px] text-[#A1A1AA] uppercase tracking-widest font-semibold">
                    devklean --preview
                  </span>
                  <div className="w-10"></div>
                </div>

                {/* Simulated CLI stdout */}
                <div className="space-y-3.5 font-mono text-xs">
                  {/* Step 1: scan */}
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="text-[#10B981] font-bold">$</span>
                      <span className="text-[#FAFAFA]">devklean scan</span>
                    </div>
                    <div className="text-[#A1A1AA]/80 pl-4 leading-relaxed">
                      🔍 Crawling directories ... <br />
                      Found <span className="text-amber-500 font-bold">14.2 GB</span> of unused node_modules and target folders.
                    </div>
                  </div>

                  {/* Step 2: purge */}
                  <div className="space-y-1 pt-1.5">
                    <div className="flex items-center gap-2">
                      <span className="text-[#10B981] font-bold">$</span>
                      <span className="text-[#FAFAFA]">devklean purge</span>
                    </div>
                    <div className="text-[#A1A1AA]/80 pl-4 space-y-1">
                      <div>Deleting 3 matching folders...</div>
                      <div className="flex items-center gap-1.5 font-semibold text-[#10B981]">
                        <span>[████████████████████] 100%</span>
                        <span>- 14.2 GB freed.</span>
                      </div>
                    </div>
                  </div>

                  {/* Step 3: summary */}
                  <div className="border-t border-[#27272A]/50 pt-3.5 mt-2 text-[#10B981] font-semibold text-[11px] flex justify-between">
                    <span>System Optimized Successfully</span>
                    <span>Elapsed: 0.82s</span>
                  </div>
                </div>

                {/* Interactive Launch Ribbon */}
                <div className="absolute -bottom-5 -right-3 sm:-right-5 bg-gradient-to-r from-[#10B981] to-[#059669] text-black rounded-lg py-2.5 px-4 font-sans text-xs font-bold shadow-lg shadow-[#10B981]/20 flex items-center gap-2 border border-[#10B981]/30 hover:scale-105 transition-transform cursor-pointer"
                     onClick={() => scrollToSection('calculator-section')}>
                  <span>Try Savings Calculator</span>
                  <ArrowRight className="h-3.5 w-3.5" />
                </div>

              </div>
            </div>
          </div>

        </div>

      </div>
    </section>
  );
}
