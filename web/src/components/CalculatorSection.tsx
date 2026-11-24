import React, { useState } from 'react';
import { Minus, Plus } from 'lucide-react';

const DEFAULTS = {
  node: '12',
  next: '4',
  python: '6',
};

// Illustrative per-directory sizes (MB); these are not measurements.
const ASSUMPTIONS = [
  { id: 'node', label: 'Dependency directories', artifact: 'node_modules', perDirectoryMB: 480 },
  { id: 'next', label: 'Next.js build directories', artifact: '.next', perDirectoryMB: 250 },
  { id: 'python', label: 'Python environments', artifact: '.venv or venv', perDirectoryMB: 1200 },
] as const;

export default function CalculatorSection() {
  const [counts, setCounts] = useState(DEFAULTS);
  const [showAssumptions, setShowAssumptions] = useState(false);

  const totalMB =
    Number(counts.node) * ASSUMPTIONS[0].perDirectoryMB +
    Number(counts.next) * ASSUMPTIONS[1].perDirectoryMB +
    Number(counts.python) * ASSUMPTIONS[2].perDirectoryMB;

  const formattedResult =
    totalMB >= 1024 ? `${(totalMB / 1024).toFixed(1)} GB` : `${totalMB} MB`;

  const updateCount = (key: keyof typeof DEFAULTS, nextValue: string) => {
    const parsed = Number(nextValue);
    const clamped = nextValue === '' ? '' : String(Number.isFinite(parsed) ? Math.max(0, Math.min(999, Math.floor(parsed))) : 0);
    setCounts((prev) => ({ ...prev, [key]: clamped }));
  };

  const reset = () => setCounts(DEFAULTS);

  return (
    <section id="calculator" className="w-full scroll-mt-16 border-b border-[#333333] bg-[#111111] py-14 md:py-20">
      <div className="mx-auto max-w-[1200px] px-5 md:px-6 lg:px-8">
        <div className="mb-10 max-w-xl">
          <h2 className="font-sans text-[32px] font-medium leading-[1.1] tracking-[-0.025em] text-[#F5F5F5] md:text-[42px]">
            How much space could artifacts occupy?
          </h2>
          <p className="mt-3 font-sans text-[16px] leading-[1.6] text-[#ADADAD]">
            Estimate your artifact footprint by directory type. A Next.js project can have both a dependency directory and a build directory; count each in its own row.
          </p>
        </div>

        {/* One compact calculator panel */}
        <div className="overflow-hidden rounded-[8px] border border-[#333333] bg-[#191919]">
          <div className="grid lg:grid-cols-12">
            {/* Three labeled numeric inputs */}
            <div className="divide-y divide-[#333333] lg:col-span-7">
              {ASSUMPTIONS.map((item) => {
                const value = Number(counts[item.id]);
                const inputId = `calc-${item.id}`;
                return (
                  <div
                    key={item.id}
                    className="flex flex-col justify-between gap-3 px-4 py-4 sm:flex-row sm:items-center sm:px-6"
                  >
                    <div>
                      <label htmlFor={inputId} className="block font-sans text-[15px] font-medium text-[#F5F5F5]">
                        {item.label}
                      </label>
                      <span className="font-mono text-[12px] text-[#ADADAD]">{item.artifact}</span>
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        type="button"
                        onClick={() => updateCount(item.id, String(value - 1))}
                        disabled={value <= 0}
                        aria-label={`Decrease ${item.label}`}
                        className="inline-flex h-[44px] w-[44px] items-center justify-center rounded-[6px] border border-[#333333] bg-[#111111] text-[#ADADAD] transition-colors hover:bg-[#242424] hover:text-[#F5F5F5] disabled:cursor-not-allowed disabled:opacity-40"
                      >
                        <Minus className="h-4 w-4" strokeWidth={1.6} aria-hidden="true" />
                      </button>

                      <input
                        id={inputId}
                        type="number"
                        inputMode="numeric"
                        min={0}
                        max={999}
                        value={counts[item.id]}
                        onChange={(e) => updateCount(item.id, e.target.value)}
                        onBlur={() => { if (counts[item.id] === '') updateCount(item.id, '0'); }}
                        className="h-[44px] w-20 rounded-[6px] border border-[#333333] bg-[#111111] px-3 text-center font-mono text-[15px] tabular-nums text-[#F5F5F5] focus:border-[#F5F5F5] focus:outline-none"
                      />

                      <button
                        type="button"
                        onClick={() => updateCount(item.id, String(value + 1))}
                        disabled={value >= 999}
                        aria-label={`Increase ${item.label}`}
                        className="inline-flex h-[44px] w-[44px] items-center justify-center rounded-[6px] border border-[#333333] bg-[#111111] text-[#ADADAD] transition-colors hover:bg-[#242424] hover:text-[#F5F5F5] disabled:cursor-not-allowed disabled:opacity-40"
                      >
                        <Plus className="h-4 w-4" strokeWidth={1.6} aria-hidden="true" />
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Adjacent estimated result */}
            <div className="flex flex-col justify-between border-t border-[#333333] bg-[#191919] px-4 py-6 sm:px-6 lg:col-span-5 lg:border-t-0 lg:border-l">
              <div>
                <p className="font-mono text-[11px] uppercase tracking-[0.12em] text-[#ADADAD]">
                  Illustrative footprint
                </p>

                <div role="status" aria-atomic="true" className="mt-4 font-sans text-[44px] font-medium leading-none tracking-[-0.03em] tabular-nums text-[#F5F5F5] sm:text-[52px]">
                  <span className="sr-only">Estimated artifact footprint: </span>{formattedResult}
                </div>

                <p className="mt-3 font-sans text-[14px] leading-[1.6] text-[#ADADAD]">
                  Across {Number(counts.node) + Number(counts.next) + Number(counts.python)} artifact directories. Actual sizes vary. This is not a measurement of your computer or a promise of recoverable space.
                </p>
              </div>

              <div className="mt-6">
                <a href="#install" className="mb-3 inline-flex min-h-[44px] items-center text-[14px] font-medium text-[#F5F5F5] underline underline-offset-4">Install and scan your actual projects →</a>
                <p className="mb-4 text-[13px] leading-relaxed text-[#ADADAD]">Standard cleanup moves artifacts to trash. Emptying the trash frees disk space.</p>
                <div className="flex flex-wrap items-center justify-between gap-2 border-t border-[#333333] pt-3">
                  <button
                    type="button"
                    onClick={() => setShowAssumptions((prev) => !prev)}
                    aria-expanded={showAssumptions}
                    aria-controls="calculator-assumptions"
                    className="inline-flex min-h-[44px] items-center font-sans text-[13px] text-[#F5F5F5] underline decoration-[#333333] underline-offset-4 transition-colors hover:decoration-[#F5F5F5]"
                  >
                    {showAssumptions ? 'Hide assumptions' : 'View assumptions'}
                  </button>

                  <button
                    type="button"
                    onClick={reset}
                    className="inline-flex min-h-[44px] items-center rounded-[6px] px-2.5 font-mono text-[12px] text-[#ADADAD] transition-colors hover:bg-[#242424] hover:text-[#F5F5F5] disabled:cursor-not-allowed disabled:opacity-40"
                  >
                    Reset
                  </button>
                </div>

                {showAssumptions && (
                  <div
                    id="calculator-assumptions"
                    className="mt-2 border-t border-[#333333] pt-3 font-mono text-[12px] leading-[1.7] text-[#ADADAD]"
                  >
                    <div>Dependencies: 480 MB / directory · Next.js builds: 250 MB / directory</div>
                    <div>Python: 1,200 MB / environment · Actual sizes vary by dependencies.</div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
