import React from 'react';
import { ScanLine, Gauge, FileSearch, Cpu, Lock } from 'lucide-react';
import { FEATURES } from '../data';

const ICONS: Record<string, React.ReactNode> = {
  scan: <ScanLine className="h-5 w-5 text-[#10B981]" />,
  analyze: <Gauge className="h-5 w-5 text-sky-400" />,
  explain: <FileSearch className="h-5 w-5 text-amber-400" />,
};

export default function FeaturesGrid() {
  return (
    <section id="features-section" className="w-full bg-[#09090B] py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">

        {/* Section Heading */}
        <div className="mb-12 text-center">
          <div className="inline-flex items-center gap-1.5 rounded-full border border-[#27272A] bg-[#18181B] px-3 py-1 font-mono text-xs font-medium text-[#10B981]">
            <Cpu className="h-3.5 w-3.5" />
            Core Capabilities
          </div>
          <h2 className="mt-4 text-3xl font-bold tracking-tight text-[#FAFAFA] sm:text-4xl font-sans">
            Understand before you delete.
          </h2>
          <p className="mx-auto mt-3 max-w-2xl text-base text-[#A1A1AA] font-sans">
            Three commands that only ever read your disk. Each one tells you more about what’s there — so the one
            command that <em>does</em> delete, <code className="font-mono text-[#FAFAFA]">clean</code>, is never a guess.
          </p>
        </div>

        {/* 3 Columns Grid */}
        <div className="grid gap-6 md:grid-cols-3">
          {FEATURES.map((feature) => (
            <div
              key={feature.id}
              id={`feature-card-${feature.id}`}
              className="group flex flex-col justify-between rounded-xl border border-[#27272A] bg-[#18181B] p-6 transition-all duration-300 hover:border-[#3F3F46]"
            >
              <div>
                {/* Icon + shared read-only marker */}
                <div className="flex items-center justify-between">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg border border-[#27272A] bg-[#09090B] shadow-inner">
                    {ICONS[feature.id]}
                  </div>
                  <span className="inline-flex items-center gap-1 rounded border border-[#10B981]/20 bg-[#10B981]/10 px-2 py-0.5 font-mono text-[10px] uppercase tracking-wider text-[#10B981]">
                    <Lock className="h-3 w-3" />
                    Read-only
                  </span>
                </div>

                {/* Command */}
                <div className="mt-6 inline-flex items-center gap-1.5 rounded bg-[#09090B] px-2.5 py-1 font-mono text-xs text-[#10B981] border border-[#27272A]/60">
                  <span className="text-[#A1A1AA]">$</span> {feature.command}
                </div>

                {/* Title & Description */}
                <h3 className="mt-4 font-sans text-xl font-bold text-[#FAFAFA]">{feature.title}</h3>
                <p className="mt-3 font-sans text-sm leading-relaxed text-[#A1A1AA]">{feature.description}</p>
              </div>

              {/* Sample output */}
              <div className="mt-6 rounded-lg border border-[#27272A] bg-black p-3">
                <div className="mb-1.5 font-mono text-[10px] uppercase tracking-wider text-[#A1A1AA]/60">
                  Sample output
                </div>
                <code className="font-mono text-xs text-[#FAFAFA]">{feature.sampleOutput}</code>
              </div>
            </div>
          ))}
        </div>

        {/* Footnote — the one command that deletes */}
        <p className="mx-auto mt-8 max-w-2xl text-center font-mono text-xs text-[#A1A1AA]/70">
          The only command that removes anything is <code className="text-[#FAFAFA]">devklean clean</code> — and even
          that moves files to your system trash, never a hard delete.
        </p>

      </div>
    </section>
  );
}
