import React, { useState } from 'react';
import { HardDrive, RotateCcw, ShieldAlert, Sparkles, Zap, Server } from 'lucide-react';
import { motion } from 'motion/react';

export default function SavingsCalculator() {
  const [nodeCount, setNodeCount] = useState(12);
  const [rustCount, setRustCount] = useState(4);
  const [pythonCount, setPythonCount] = useState(6);

  // Typical sizes of unused build folders in Megabytes
  const NODE_TYPICAL_MB = 480; // 480MB
  const RUST_TYPICAL_MB = 2400; // 2.4GB
  const PYTHON_TYPICAL_MB = 1200; // 1.2GB

  const totalBytesMB =
    nodeCount * NODE_TYPICAL_MB +
    rustCount * RUST_TYPICAL_MB +
    pythonCount * PYTHON_TYPICAL_MB;

  const totalGB = (totalBytesMB / 1024).toFixed(1);
  
  // DevKlean speed: ~15,000 directories per second, let's simulate
  const scanTimeSeconds = ((nodeCount + rustCount + pythonCount) * 0.04 + 0.12).toFixed(2);
  const purgeTimeSeconds = ((nodeCount + rustCount + pythonCount) * 0.08 + 0.35).toFixed(2);

  const resetSliders = () => {
    setNodeCount(12);
    setRustCount(4);
    setPythonCount(6);
  };

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
              Enter your estimated local project counts below. You might be surprised by how much obsolete compiler cache is weighing down your system.
            </p>
          </div>
          <button
            id="btn-calculator-reset"
            onClick={resetSliders}
            className="mt-4 inline-flex items-center gap-1.5 rounded-md border border-[#27272A] bg-[#18181B] px-3 py-1.5 font-mono text-xs text-[#A1A1AA] hover:bg-[#27272A] hover:text-[#FAFAFA] transition-colors md:mt-0"
          >
            <RotateCcw className="h-3.5 w-3.5" />
            Reset Defaults
          </button>
        </div>

        <div className="grid gap-8 lg:grid-cols-12">
          {/* Sliders Area (8 cols on lg) */}
          <div className="space-y-6 lg:col-span-7">
            
            {/* Node Slider */}
            <div className="rounded-xl border border-[#27272A] bg-[#18181B] p-5 sm:p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <span className="flex h-2.5 w-2.5 rounded-full bg-[#10B981]"></span>
                  <span className="font-mono text-sm font-semibold text-[#FAFAFA]">Node.js Repositories</span>
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
                  className="h-1.5 w-full cursor-pointer appearance-none rounded-lg bg-[#09090B] accent-[#10B981] [&::-webkit-slider-runnable-track]:bg-[#09090B] [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-[#10B981]"
                />
                <span className="w-12 text-right font-mono text-lg font-bold text-[#FAFAFA]">
                  {nodeCount}
                </span>
              </div>
              <div className="mt-2 flex justify-between font-mono text-[11px] text-[#A1A1AA]">
                <span>0 repos</span>
                <span>Est: ~{(nodeCount * NODE_TYPICAL_MB / 1024).toFixed(1)} GB unused</span>
                <span>50 repos</span>
              </div>
            </div>

            {/* Rust Slider */}
            <div className="rounded-xl border border-[#27272A] bg-[#18181B] p-5 sm:p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <span className="flex h-2.5 w-2.5 rounded-full bg-amber-500"></span>
                  <span className="font-mono text-sm font-semibold text-[#FAFAFA]">Rust / Cargo Repositories</span>
                </div>
                <span className="font-mono text-xs text-[#A1A1AA] bg-[#09090B] px-2.5 py-1 rounded border border-[#27272A]">
                  Typical artifact: <code className="text-amber-500">target/</code>
                </span>
              </div>
              
              <div className="flex items-center gap-4">
                <input
                  id="slider-rust-count"
                  type="range"
                  min="0"
                  max="30"
                  value={rustCount}
                  onChange={(e) => setRustCount(parseInt(e.target.value))}
                  className="h-1.5 w-full cursor-pointer appearance-none rounded-lg bg-[#09090B] accent-amber-500 [&::-webkit-slider-runnable-track]:bg-[#09090B] [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-amber-500"
                />
                <span className="w-12 text-right font-mono text-lg font-bold text-[#FAFAFA]">
                  {rustCount}
                </span>
              </div>
              <div className="mt-2 flex justify-between font-mono text-[11px] text-[#A1A1AA]">
                <span>0 repos</span>
                <span>Est: ~{(rustCount * RUST_TYPICAL_MB / 1024).toFixed(1)} GB unused</span>
                <span>30 repos</span>
              </div>
            </div>

            {/* Python Slider */}
            <div className="rounded-xl border border-[#27272A] bg-[#18181B] p-5 sm:p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-2">
                  <span className="flex h-2.5 w-2.5 rounded-full bg-blue-400"></span>
                  <span className="font-mono text-sm font-semibold text-[#FAFAFA]">Python Environments</span>
                </div>
                <span className="font-mono text-xs text-[#A1A1AA] bg-[#09090B] px-2.5 py-1 rounded border border-[#27272A]">
                  Typical artifact: <code className="text-blue-400">.venv / __pycache__</code>
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
                  className="h-1.5 w-full cursor-pointer appearance-none rounded-lg bg-[#09090B] accent-blue-400 [&::-webkit-slider-runnable-track]:bg-[#09090B] [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-blue-400"
                />
                <span className="w-12 text-right font-mono text-lg font-bold text-[#FAFAFA]">
                  {pythonCount}
                </span>
              </div>
              <div className="mt-2 flex justify-between font-mono text-[11px] text-[#A1A1AA]">
                <span>0 envs</span>
                <span>Est: ~{(pythonCount * PYTHON_TYPICAL_MB / 1024).toFixed(1)} GB unused</span>
                <span>25 envs</span>
              </div>
            </div>

          </div>

          {/* Result Panel (5 cols on lg) */}
          <div className="lg:col-span-5">
            <div className="relative h-full rounded-xl border border-[#27272A] bg-black p-6 flex flex-col justify-between overflow-hidden shadow-2xl">
              {/* Subtle background glow */}
              <div className="absolute -right-20 -top-20 -z-10 h-40 w-40 rounded-full bg-[#10B981]/10 blur-3xl"></div>

              <div>
                <div className="flex items-center gap-2 font-mono text-xs font-semibold text-[#10B981] bg-[#10B981]/10 px-3 py-1 rounded-md border border-[#10B981]/20 w-fit">
                  <Sparkles className="h-3.5 w-3.5" />
                  Calculated Saving Opportunity
                </div>

                {/* Big space saved text */}
                <div className="mt-8">
                  <span className="font-mono text-6xl font-extrabold tracking-tight text-[#FAFAFA] sm:text-7xl">
                    {totalGB}
                  </span>
                  <span className="font-mono text-2xl font-bold text-[#10B981] ml-2">GB</span>
                </div>
                <p className="mt-2 font-sans text-sm text-[#A1A1AA]">
                  Of unreferenced artifacts, log archives, and pre-compiled object files currently sitting dormant on your hard drive.
                </p>

                {/* Speed spec list */}
                <div className="mt-6 space-y-3.5 border-t border-[#27272A] pt-6 font-mono text-xs">
                  <div className="flex justify-between items-center text-[#A1A1AA]">
                    <span className="flex items-center gap-1.5">
                      <Zap className="h-3.5 w-3.5 text-[#10B981]" />
                      Estimated Scan Time:
                    </span>
                    <span className="text-[#FAFAFA] font-bold">{scanTimeSeconds}s</span>
                  </div>
                  <div className="flex justify-between items-center text-[#A1A1AA]">
                    <span className="flex items-center gap-1.5">
                      <Server className="h-3.5 w-3.5 text-blue-400" />
                      Estimated Purge Duration:
                    </span>
                    <span className="text-[#FAFAFA] font-bold">{purgeTimeSeconds}s</span>
                  </div>
                  <div className="flex justify-between items-center text-[#A1A1AA]">
                    <span className="flex items-center gap-1.5">
                      <ShieldAlert className="h-3.5 w-3.5 text-amber-500" />
                      Accidental Deletion Risk:
                    </span>
                    <span className="text-emerald-400 font-bold">0.00%</span>
                  </div>
                </div>
              </div>

              <div className="mt-8 rounded-lg bg-[#18181B] border border-[#27272A] p-4 text-center">
                <span className="block font-mono text-[10px] text-[#A1A1AA]">PRO-TIP</span>
                <p className="mt-1 font-sans text-xs text-[#FAFAFA] leading-relaxed">
                  Run <code className="text-[#10B981]">devklean scan --all</code> once a month to keep your developer drive responsive and light.
                </p>
              </div>

            </div>
          </div>
        </div>

      </div>
    </section>
  );
}
