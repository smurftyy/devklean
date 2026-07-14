import React, { useState } from 'react';
import { Copy, Check, ArrowRight, BookOpen } from 'lucide-react';

export default function HeroSection() {
  const [copied, setCopied] = useState(false);
  const commandText = 'pipx install devklean';

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
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">

        {/* Banner Announcement */}
        <div className="mb-8 flex justify-center lg:justify-start">
          <div className="inline-flex items-center gap-2 rounded-full border border-[#27272A] bg-[#18181B] px-3.5 py-1.5 font-mono text-xs text-[#FAFAFA]">
            <span className="flex h-2 w-2 rounded-full bg-[#10B981]"></span>
            <span className="text-[#10B981] font-semibold">v1.1.0:</span>
            <span>
              <code className="text-[#FAFAFA]">analyze</code>, <code className="text-[#FAFAFA]">explain</code>, and{' '}
              <code className="text-[#FAFAFA]">--compress</code> are here
            </span>
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
              A CLI that finds regenerable build artifacts from Node.js, Python, and Next.js, tells you exactly what each
              one is, and moves them to your system trash — never a hard delete.
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
                  className="ml-4 rounded-md p-1.5 text-[#A1A1AA] transition-colors hover:text-[#FAFAFA] hover:bg-[#27272A] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#10B981] focus-visible:ring-offset-2 focus-visible:ring-offset-[#18181B]"
                  title="Copy installation command"
                >
                  {copied ? (
                    <Check className="h-4 w-4 text-[#10B981]" />
                  ) : (
                    <Copy className="h-4 w-4 group-hover:scale-105 transition-transform" />
                  )}
                </button>
              </div>

              {/* Secondary Demo Button */}
              <button
                id="btn-hero-docs"
                onClick={() => scrollToSection('demo-section')}
                className="flex items-center justify-center gap-2 rounded-lg border border-[#27272A] bg-transparent hover:bg-[#18181B] text-[#FAFAFA] px-5 py-3.5 text-xs font-semibold font-mono w-full sm:w-auto transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#10B981] focus-visible:ring-offset-2 focus-visible:ring-offset-[#09090B]"
              >
                <BookOpen className="h-4 w-4 text-[#10B981]" />
                Interactive Demo
              </button>
            </div>

            {/* Micro proof points */}
            <div className="flex items-center justify-center lg:justify-start gap-5 pt-4 text-xs font-mono text-[#A1A1AA]">
              <div className="flex items-center gap-1.5">
                <span className="text-[#10B981] font-bold">100%</span> open-source · MIT
              </div>
              <div className="h-3 w-[1px] bg-[#27272A]"></div>
              <div className="flex items-center gap-1.5">
                <span className="text-[#10B981] font-bold">0</span> telemetry
              </div>
              <div className="h-3 w-[1px] bg-[#27272A]"></div>
              <div className="flex items-center gap-1.5">
                <span className="text-[#10B981] font-bold">trash</span>, never rm -rf
              </div>
            </div>

          </div>

          {/* Right Column: Visual Hero Terminal */}
          <div className="lg:col-span-6 flex justify-center">
            <div className="relative w-full max-w-lg">
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
                    devklean --dry-run
                  </span>
                  <div className="w-10"></div>
                </div>

                {/* Simulated CLI stdout */}
                <div className="space-y-3.5 font-mono text-xs">
                  {/* scan */}
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="text-[#10B981] font-bold">$</span>
                      <span className="text-[#FAFAFA]">devklean scan</span>
                    </div>
                    <div className="text-[#A1A1AA]/80 pl-4 leading-relaxed space-y-0.5">
                      <div>Scanning ~/projects ...</div>
                      <div>
                        <span className="text-[#FAFAFA]">node_modules</span>{' '}
                        <span className="text-amber-500">1.21 GB</span>{' '}
                        <span className="text-[#A1A1AA]/60">~/projects/web/portfolio</span>
                      </div>
                      <div>
                        <span className="text-[#FAFAFA]">env</span>{' '}
                        <span className="text-amber-500">360.0 MB</span>{' '}
                        <span className="text-[#A1A1AA]/60">~/projects/api/ingest-service</span>
                      </div>
                      <div>
                        <span className="text-[#FAFAFA]">.next</span>{' '}
                        <span className="text-amber-500">200.0 MB</span>{' '}
                        <span className="text-[#A1A1AA]/60">~/projects/web/marketing-site</span>
                      </div>
                      <div className="pt-1">
                        Found <span className="text-amber-500 font-bold">1.76 GB</span> across 3 directories.
                      </div>
                    </div>
                  </div>

                  {/* clean */}
                  <div className="space-y-1 pt-1.5">
                    <div className="flex items-center gap-2">
                      <span className="text-[#10B981] font-bold">$</span>
                      <span className="text-[#FAFAFA]">devklean clean</span>
                    </div>
                    <div className="text-[#A1A1AA]/80 pl-4 space-y-0.5">
                      <div>Delete 3 directories (~1.76 GB)?</div>
                      <div className="text-amber-500">This exceeds the 1.0 GiB safety threshold.</div>
                      <div>
                        Type <span className="text-[#FAFAFA] font-bold">DELETE</span> to confirm:{' '}
                        <span className="text-[#FAFAFA]">DELETE</span>
                      </div>
                      <div className="text-[#10B981]">✓ moved to trash — node_modules</div>
                      <div className="text-[#10B981]">✓ moved to trash — env</div>
                      <div className="text-[#10B981]">✓ moved to trash — .next</div>
                    </div>
                  </div>

                  {/* summary */}
                  <div className="border-t border-[#27272A]/50 pt-3.5 mt-2 text-[#10B981] font-semibold text-[11px]">
                    ✓ Cleaned 3 directories, freed ~1.76 GB — all recoverable from trash.
                  </div>
                </div>

                {/* Interactive Launch Ribbon */}
                <button
                  onClick={() => scrollToSection('calculator-section')}
                  className="absolute -bottom-5 -right-3 sm:-right-5 flex items-center gap-2 rounded-lg border border-[#10B981]/30 bg-gradient-to-r from-[#10B981] to-[#059669] py-2.5 px-4 font-sans text-xs font-bold text-black shadow-lg shadow-[#10B981]/20 transition-transform hover:scale-105 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#10B981] focus-visible:ring-offset-2 focus-visible:ring-offset-[#09090B]"
                >
                  <span>Try Savings Calculator</span>
                  <ArrowRight className="h-3.5 w-3.5" />
                </button>

              </div>
            </div>
          </div>

        </div>

      </div>
    </section>
  );
}
