import React, { useState } from 'react';
import { HardDrive, RotateCcw, Trash2, ShieldCheck, Eye, Sparkles } from 'lucide-react';

export default function SavingsCalculator() {
  const [nodeCount, setNodeCount] = useState(12);
  const [nextCount, setNextCount] = useState(4);
  const [pythonCount, setPythonCount] = useState(6);

  // Rough per-project sizes for the *user's own* estimate — not a claim about
  // the tool. Kept deliberately conservative.
  const NODE_TYPICAL_MB = 480;
  const NEXT_TYPICAL_MB = 250;
  const PYTHON_TYPICAL_MB = 1200;

  const totalBytesMB = nodeCount * NODE_TYPICAL_MB + nextCount * NEXT_TYPICAL_MB + pythonCount * PYTHON_TYPICAL_MB;
  const totalGB = (totalBytesMB / 1024).toFixed(1);

  const resetSliders = () => {
    setNodeCount(12);
    setNextCount(4);
    setPythonCount(6);
  };

  const sliderClass = (accent: string) =>
    `h-1.5 w-full cursor-pointer appearance-none rounded-lg bg-[#09090B] ${accent} [&::-webkit-slider-runnable-track]:bg-[#09090B] [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:rounded-full focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-[#18181B]`;

  return (
    <section id="calculator-section" className="w-full border-t border-[#27272A] bg-[#09090B] py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">

        {/* Header */}
        <div className="mb-12 text-center md:text-left md:flex md:items-end md:justify-between">
          <div>
            <div className="inline-flex items-center gap-1.5 rounded-full border border-[#27272A] bg-[#18181B] px-3 py-1 font-mono text-xs font-medium text-[#10B981]">
              <HardDrive className="h-3.5 w-3.5" />
              Interactive Analytics
            </div>
            <h2 className="mt-4 text-3xl font-bold tracking-tight text-[#FAFAFA] sm:text-4xl font-sans">
              How much disk space are you wasting?
            </h2>
            <p className="mt-2 max-w-2xl text-base text-[#A1A1AA] font-sans">
              Estimate your local project counts below. Build artifacts add up fast — and every one of them is
              regenerable from source.
            </p>
          </div>
          <button
            id="btn-calculator-reset"
            onClick={resetSliders}
            className="mt-4 inline-flex items-center gap-1.5 rounded-md border border-[#27272A] bg-[#18181B] px-3 py-1.5 font-mono text-xs text-[#A1A1AA] transition-colors hover:bg-[#27272A] hover:text-[#FAFAFA] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#10B981] focus-visible:ring-offset-2 focus-visible:ring-offset-[#09090B] md:mt-0"
          >
            <RotateCcw className="h-3.5 w-3.5" />
            Reset Defaults
          </button>
        </div>

        <div className="grid gap-8 lg:grid-cols-12">
          {/* Sliders Area */}
          <div className="space-y-6 lg:col-span-7">

            {/* Node Slider */}
            <div className="rounded-xl border border-[#27272A] bg-[#18181B] p-5 sm:p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <span className="flex h-2.5 w-2.5 rounded-full bg-[#10B981]"></span>
                  <span className="font-mono text-sm font-semibold text-[#FAFAFA]">Node.js Projects</span>
                </div>
                <span className="font-mono text-xs text-[#A1A1AA] bg-[#09090B] px-2.5 py-1 rounded border border-[#27272A]">
                  Typical artifact: <code className="text-[#10B981]">node_modules</code>
                </span>
              </div>
              <div className="flex items-center gap-4">
                <input
                  id="slider-node-count"
                  type="range"
                  min="0"
                  max="50"
                  value={nodeCount}
                  onChange={(e) => setNodeCount(parseInt(e.target.value))}
                  className={sliderClass('accent-[#10B981] [&::-webkit-slider-thumb]:bg-[#10B981] focus-visible:ring-[#10B981]')}
                />
                <span className="w-12 text-right font-mono text-lg font-bold text-[#FAFAFA]">{nodeCount}</span>
              </div>
              <div className="mt-2 flex justify-between font-mono text-[11px] text-[#A1A1AA]">
                <span>0 projects</span>
                <span>Est: ~{(nodeCount * NODE_TYPICAL_MB / 1024).toFixed(1)} GB</span>
                <span>50 projects</span>
              </div>
            </div>

            {/* Next.js Slider */}
            <div className="rounded-xl border border-[#27272A] bg-[#18181B] p-5 sm:p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <span className="flex h-2.5 w-2.5 rounded-full bg-zinc-200"></span>
                  <span className="font-mono text-sm font-semibold text-[#FAFAFA]">Next.js Projects</span>
                </div>
                <span className="font-mono text-xs text-[#A1A1AA] bg-[#09090B] px-2.5 py-1 rounded border border-[#27272A]">
                  Typical artifact: <code className="text-zinc-100">.next</code>
                </span>
              </div>
              <div className="flex items-center gap-4">
                <input
                  id="slider-next-count"
                  type="range"
                  min="0"
                  max="30"
                  value={nextCount}
                  onChange={(e) => setNextCount(parseInt(e.target.value))}
                  className={sliderClass('accent-zinc-200 [&::-webkit-slider-thumb]:bg-zinc-200 focus-visible:ring-zinc-200')}
                />
                <span className="w-12 text-right font-mono text-lg font-bold text-[#FAFAFA]">{nextCount}</span>
              </div>
              <div className="mt-2 flex justify-between font-mono text-[11px] text-[#A1A1AA]">
                <span>0 projects</span>
                <span>Est: ~{(nextCount * NEXT_TYPICAL_MB / 1024).toFixed(1)} GB</span>
                <span>30 projects</span>
              </div>
            </div>

            {/* Python Slider */}
            <div className="rounded-xl border border-[#27272A] bg-[#18181B] p-5 sm:p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <span className="flex h-2.5 w-2.5 rounded-full bg-sky-400"></span>
                  <span className="font-mono text-sm font-semibold text-[#FAFAFA]">Python Environments</span>
                </div>
                <span className="font-mono text-xs text-[#A1A1AA] bg-[#09090B] px-2.5 py-1 rounded border border-[#27272A]">
                  Typical artifact: <code className="text-sky-400">.venv / __pycache__</code>
                </span>
              </div>
              <div className="flex items-center gap-4">
                <input
                  id="slider-python-count"
                  type="range"
                  min="0"
                  max="25"
                  value={pythonCount}
                  onChange={(e) => setPythonCount(parseInt(e.target.value))}
                  className={sliderClass('accent-sky-400 [&::-webkit-slider-thumb]:bg-sky-400 focus-visible:ring-sky-400')}
                />
                <span className="w-12 text-right font-mono text-lg font-bold text-[#FAFAFA]">{pythonCount}</span>
              </div>
              <div className="mt-2 flex justify-between font-mono text-[11px] text-[#A1A1AA]">
                <span>0 envs</span>
                <span>Est: ~{(pythonCount * PYTHON_TYPICAL_MB / 1024).toFixed(1)} GB</span>
                <span>25 envs</span>
              </div>
            </div>

          </div>

          {/* Result Panel */}
          <div className="lg:col-span-5">
            <div className="relative h-full rounded-xl border border-[#27272A] bg-black p-6 flex flex-col justify-between overflow-hidden shadow-2xl">
              <div>
                <div className="flex items-center gap-2 font-mono text-xs font-semibold text-[#10B981] bg-[#10B981]/10 px-3 py-1 rounded-md border border-[#10B981]/20 w-fit">
                  <Sparkles className="h-3.5 w-3.5" />
                  Estimated Reclaimable
                </div>

                {/* Big space saved text */}
                <div className="mt-8">
                  <span className="font-mono text-6xl font-extrabold tracking-tight text-[#FAFAFA] sm:text-7xl">
                    {totalGB}
                  </span>
                  <span className="font-mono text-2xl font-bold text-[#10B981] ml-2">GB</span>
                </div>
                <p className="mt-2 font-sans text-sm text-[#A1A1AA]">
                  Of regenerable build artifacts — dependency trees, virtual environments, and compiled output — sitting
                  on your drive.
                </p>

                {/* Truthful facts about how devklean handles it */}
                <div className="mt-6 space-y-3.5 border-t border-[#27272A] pt-6 font-mono text-xs">
                  <div className="flex items-center gap-2 text-[#A1A1AA]">
                    <Trash2 className="h-3.5 w-3.5 text-[#10B981] shrink-0" />
                    <span>Sent to your system trash — not <code className="text-[#FAFAFA]">rm -rf</code>.</span>
                  </div>
                  <div className="flex items-center gap-2 text-[#A1A1AA]">
                    <ShieldCheck className="h-3.5 w-3.5 text-amber-400 shrink-0" />
                    <span>Anything ≥ 1 GiB requires typing <code className="text-[#FAFAFA]">DELETE</code>.</span>
                  </div>
                  <div className="flex items-center gap-2 text-[#A1A1AA]">
                    <Eye className="h-3.5 w-3.5 text-sky-400 shrink-0" />
                    <span><code className="text-[#FAFAFA]">scan</code> and <code className="text-[#FAFAFA]">analyze</code> never delete a thing.</span>
                  </div>
                </div>
              </div>

              <div className="mt-8 rounded-lg bg-[#18181B] border border-[#27272A] p-4">
                <span className="block font-mono text-[10px] text-[#A1A1AA]">PRO-TIP</span>
                <p className="mt-1 font-sans text-xs text-[#FAFAFA] leading-relaxed">
                  Run <code className="text-[#10B981]">devklean analyze --verbose</code> to see the workspace-health
                  score and the exact formula behind it — no deletions, just the report.
                </p>
              </div>

            </div>
          </div>
        </div>

      </div>
    </section>
  );
}
