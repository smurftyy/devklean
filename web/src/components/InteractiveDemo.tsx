import React, { useEffect, useState } from 'react';
import { Terminal, RotateCcw, ChevronDown, ArrowDown, ScanLine, Gauge, FileSearch } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { DEMO_PROJECTS } from '../data';
import { DemoProject, RiskLevel, RISK_WEIGHT } from '../types';

type Step = 'scan' | 'analyze' | 'explain';

const STEPS: { id: Step; label: string; command: string; blurb: string; icon: React.ReactNode }[] = [
  { id: 'scan', label: 'Scan', command: 'devklean scan', blurb: 'Find cleanable directories and their sizes.', icon: <ScanLine className="h-4 w-4" /> },
  { id: 'analyze', label: 'Analyze', command: 'devklean analyze', blurb: 'Add risk, confidence, and a health score.', icon: <Gauge className="h-4 w-4" /> },
  { id: 'explain', label: 'Explain', command: 'devklean explain', blurb: 'Open any row for the full reasoning.', icon: <FileSearch className="h-4 w-4" /> },
];

const RISK_STYLES: Record<RiskLevel, string> = {
  low: 'text-emerald-400 border-emerald-400/30 bg-emerald-400/10',
  medium: 'text-amber-400 border-amber-400/30 bg-amber-400/10',
  high: 'text-red-400 border-red-400/30 bg-red-400/10',
};

// Workspace-health score via the exact formula in devklean.signatures.health:
// round(100 * sum(size*risk_weight) / total) - 10*lockfile_conflicts, clamped.
function computeHealth(projects: DemoProject[]): number {
  const total = projects.reduce((s, p) => s + p.sizeMB, 0);
  if (total === 0) return 100;
  const weighted = projects.reduce((s, p) => s + p.sizeMB * RISK_WEIGHT[p.risk], 0);
  const conflicts = projects.filter((p) => p.lockfileConflict).length;
  const raw = Math.round((100 * weighted) / total) - 10 * conflicts;
  return Math.max(0, Math.min(100, raw));
}

function fmtSize(mb: number): string {
  return mb >= 1024 ? `${(mb / 1024).toFixed(2)} GB` : `${mb.toFixed(1)} MB`;
}

// Eased count-up that replays whenever `resetKey` changes.
function useCountUp(target: number, duration: number, resetKey: unknown): number {
  const [val, setVal] = useState(0);
  useEffect(() => {
    let raf = 0;
    const start = performance.now();
    const tick = (now: number) => {
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3);
      setVal(target * eased);
      if (t < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [target, duration, resetKey]);
  return val;
}

export default function InteractiveDemo() {
  const [step, setStep] = useState<Step>('scan');
  const [runId, setRunId] = useState(0);
  const [openRow, setOpenRow] = useState<string | null>(DEMO_PROJECTS[0].id);
  const [replaying, setReplaying] = useState(false);

  const totalSize = DEMO_PROJECTS.reduce((s, p) => s + p.sizeMB, 0);
  const health = computeHealth(DEMO_PROJECTS);

  // Both replay from 0 on any step/run change; each is only shown in its step.
  const scanTotal = useCountUp(totalSize, 1000, `${step}-${runId}`);
  const healthCount = useCountUp(health, 1100, `${step}-${runId}`);

  // Briefly lock the Restart control while the entrance animation plays, with a
  // real disabled treatment (not opacity-only).
  useEffect(() => {
    setReplaying(true);
    const t = setTimeout(() => setReplaying(false), 1050);
    return () => clearTimeout(t);
  }, [step, runId]);

  const activeCmd = STEPS.find((s) => s.id === step)!.command;

  const selectStep = (s: Step) => {
    if (s === step) return;
    setStep(s);
    if (s === 'explain') setOpenRow(DEMO_PROJECTS[0].id);
  };

  // Health ring geometry
  const R = 34;
  const C = 2 * Math.PI * R;
  const dashOffset = C * (1 - healthCount / 100);

  return (
    <section id="demo-section" className="w-full border-t border-[#27272A] bg-[#09090B]/80 py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">

        {/* Title */}
        <div className="mb-16 text-center">
          <div className="inline-flex items-center gap-1.5 rounded-full border border-[#27272A] bg-[#18181B] px-3 py-1 font-mono text-xs font-medium text-[#10B981]">
            <Terminal className="h-3.5 w-3.5" />
            Interactive Demo
          </div>
          <h2 className="mt-4 text-3xl font-bold tracking-tight text-[#FAFAFA] sm:text-4xl font-sans">
            Scan, then analyze, then explain.
          </h2>
          <p className="mx-auto mt-3 max-w-2xl text-base text-[#A1A1AA] font-sans">
            The same workspace, seen through three read-only commands. Pick one — nothing here deletes anything.
          </p>
        </div>

        <div className="grid gap-10 lg:grid-cols-12 items-start">

          {/* Left: step selectors */}
          <div className="space-y-4 lg:col-span-5">
            {STEPS.map((s) => {
              const isActive = s.id === step;
              return (
                <button
                  key={s.id}
                  id={`demo-step-card-${s.id}`}
                  onClick={() => selectStep(s.id)}
                  className={`group relative w-full rounded-xl border p-5 text-left transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#10B981] focus-visible:ring-offset-2 focus-visible:ring-offset-[#09090B] ${
                    isActive
                      ? 'border-[#10B981] bg-[#18181B] shadow-lg shadow-[#10B981]/5'
                      : 'border-[#27272A] bg-[#18181B]/50 hover:border-[#3F3F46] hover:bg-[#18181B]'
                  }`}
                >
                  <div className="flex items-center gap-2">
                    <span className={isActive ? 'text-[#10B981]' : 'text-[#A1A1AA]'}>{s.icon}</span>
                    <h3 className="font-sans text-lg font-bold text-[#FAFAFA]">{s.label}</h3>
                  </div>
                  <div className="mt-2.5 inline-flex items-center gap-1.5 rounded bg-black px-2.5 py-1 font-mono text-xs text-[#10B981] border border-[#27272A]/50">
                    <span className="text-[#A1A1AA]">$</span> {s.command}
                  </div>
                  <p className="mt-3 font-sans text-xs leading-relaxed text-[#A1A1AA]">{s.blurb}</p>
                  {isActive && <div className="absolute left-0 top-1/4 h-1/2 w-1 rounded-r-full bg-[#10B981]"></div>}
                </button>
              );
            })}
          </div>

          {/* Right: terminal panel */}
          <div className="lg:col-span-7">
            <div className="rounded-xl border border-[#27272A] bg-black p-4 font-mono text-xs shadow-2xl">
              {/* Window chrome */}
              <div className="flex items-center justify-between border-b border-[#27272A] pb-3 mb-4">
                <div className="flex items-center gap-1.5">
                  <div className="h-3 w-3 rounded-full bg-red-500"></div>
                  <div className="h-3 w-3 rounded-full bg-yellow-500"></div>
                  <div className="h-3 w-3 rounded-full bg-green-500"></div>
                </div>
                <div className="flex items-center gap-1.5 text-[11px] text-[#A1A1AA] font-semibold">
                  <Terminal className="h-3.5 w-3.5 text-[#10B981]" />
                  devklean — v1.1.0
                </div>
                <button
                  id="btn-terminal-restart"
                  onClick={() => setRunId((n) => n + 1)}
                  disabled={replaying}
                  className={`flex items-center gap-1 rounded border px-2 py-0.5 text-[10px] transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#10B981] ${
                    replaying
                      ? 'cursor-not-allowed border-[#1c1c1f] bg-[#111113] text-[#3F3F46]'
                      : 'border-[#27272A] bg-[#18181B] text-[#A1A1AA] hover:text-[#FAFAFA] hover:border-[#3F3F46]'
                  }`}
                  title="Replay this step"
                >
                  <RotateCcw className="h-3 w-3" />
                  Restart
                </button>
              </div>

              {/* Command line */}
              <div className="mb-3 flex items-center gap-2">
                <span className="text-[#10B981] font-bold">$</span>
                <span className="text-[#FAFAFA]">{activeCmd}</span>
              </div>

              {/* Body */}
              <div className="min-h-[360px]">
                {/* scan header row */}
                {step !== 'explain' && (
                  <div className="mb-2 flex items-center justify-between text-[10px] uppercase tracking-wider text-[#A1A1AA]/50">
                    <span>Directory</span>
                    <span>{step === 'scan' ? 'Size' : 'Risk · Confidence'}</span>
                  </div>
                )}

                <AnimatePresence mode="wait">
                  <motion.div key={`${step}-${runId}`} className="space-y-2">
                    {DEMO_PROJECTS.map((p, i) => {
                      const isOpen = step === 'explain' && openRow === p.id;
                      return (
                        <motion.div
                          key={p.id}
                          initial={{ opacity: 0, y: 8 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: i * 0.12, duration: 0.35 }}
                          className={`rounded-lg border ${
                            isOpen ? 'border-[#10B981]/40 bg-[#10B981]/[0.03]' : 'border-[#27272A] bg-[#0d0d0f]'
                          }`}
                        >
                          {/* Row header */}
                          <button
                            onClick={() => step === 'explain' && setOpenRow(isOpen ? null : p.id)}
                            className={`flex w-full items-center justify-between gap-3 px-3 py-2.5 text-left ${
                              step === 'explain'
                                ? 'cursor-pointer focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#10B981] rounded-lg'
                                : 'cursor-default'
                            }`}
                          >
                            <div className="min-w-0">
                              <div className="truncate text-[#FAFAFA]">{p.dirName}</div>
                              <div className="truncate text-[10px] text-[#A1A1AA]/60">{p.path}</div>
                            </div>

                            {/* Right side varies by step */}
                            {step === 'scan' && <span className="shrink-0 text-amber-500">{fmtSize(p.sizeMB)}</span>}

                            {step === 'analyze' && (
                              <motion.div
                                initial={{ scale: 0.6, opacity: 0 }}
                                animate={{ scale: 1, opacity: 1 }}
                                transition={{ type: 'spring', stiffness: 500, damping: 22, delay: 0.25 + i * 0.12 }}
                                className="flex shrink-0 items-center gap-2"
                              >
                                <span className={`rounded border px-1.5 py-0.5 text-[10px] font-semibold ${RISK_STYLES[p.risk]}`}>
                                  {p.risk} risk
                                </span>
                                <span className="text-[10px] text-[#A1A1AA]">{Math.round(p.confidence * 100)}%</span>
                              </motion.div>
                            )}

                            {step === 'explain' && (
                              <ChevronDown
                                className={`h-4 w-4 shrink-0 text-[#A1A1AA] transition-transform ${isOpen ? 'rotate-180' : ''}`}
                              />
                            )}
                          </button>

                          {/* Explain detail */}
                          <AnimatePresence initial={false}>
                            {isOpen && (
                              <motion.div
                                initial={{ height: 0, opacity: 0 }}
                                animate={{ height: 'auto', opacity: 1 }}
                                exit={{ height: 0, opacity: 0 }}
                                transition={{ duration: 0.28 }}
                                className="overflow-hidden"
                              >
                                <dl className="space-y-2 border-t border-[#27272A] px-3 py-3 text-[11px]">
                                  <Field label="ecosystem" value={p.ecosystem} />
                                  <Field label="generated by" value={p.generatedBy} />
                                  <Field label="regenerate" value={<code className="text-[#10B981]">{p.regenerateCommand}</code>} />
                                  <Field
                                    label="risk · confidence"
                                    value={
                                      <span>
                                        <span className={`rounded border px-1.5 py-0.5 font-semibold ${RISK_STYLES[p.risk]}`}>
                                          {p.risk}
                                        </span>{' '}
                                        · {Math.round(p.confidence * 100)}% confidence
                                      </span>
                                    }
                                  />
                                  <Field label="staleness" value={`${p.staleDays} days since last activity`} />
                                  <Field label="rationale" value={<span className="text-[#A1A1AA]">{p.rationale}</span>} />
                                </dl>
                              </motion.div>
                            )}
                          </AnimatePresence>
                        </motion.div>
                      );
                    })}
                  </motion.div>
                </AnimatePresence>

                {/* Step summary footer inside terminal */}
                <div className="mt-4 border-t border-[#27272A] pt-3">
                  {step === 'scan' && (
                    <div className="text-[#A1A1AA]">
                      Found <span className="font-bold text-amber-500">{fmtSize(scanTotal)}</span> across{' '}
                      {DEMO_PROJECTS.length} directories.{' '}
                      <span className="text-[#A1A1AA]/60">Nothing deleted — this is a read-only scan.</span>
                    </div>
                  )}

                  {step === 'analyze' && (
                    <div className="flex items-center gap-4">
                      {/* Health gauge */}
                      <div className="relative h-[84px] w-[84px] shrink-0">
                        <svg viewBox="0 0 84 84" className="h-full w-full -rotate-90">
                          <circle cx="42" cy="42" r={R} fill="none" stroke="#27272A" strokeWidth="7" />
                          <circle
                            cx="42"
                            cy="42"
                            r={R}
                            fill="none"
                            stroke="#10B981"
                            strokeWidth="7"
                            strokeLinecap="round"
                            strokeDasharray={C}
                            strokeDashoffset={dashOffset}
                          />
                        </svg>
                        <div className="absolute inset-0 flex flex-col items-center justify-center">
                          <span className="text-lg font-bold text-[#FAFAFA]">{Math.round(healthCount)}</span>
                          <span className="text-[8px] uppercase tracking-wider text-[#A1A1AA]/60">health</span>
                        </div>
                      </div>
                      <div className="text-[11px] leading-relaxed text-[#A1A1AA]">
                        <div>
                          Workspace health <span className="font-bold text-[#FAFAFA]">{health}/100</span>, weighted by each
                          artifact’s reclaim-safety and size.
                        </div>
                        <div className="mt-1 text-[#A1A1AA]/70">
                          1 lockfile conflict flagged in <code className="text-[#FAFAFA]">portfolio</code> (−10). Every
                          verdict comes from a fixed registry — never an inference.
                        </div>
                      </div>
                    </div>
                  )}

                  {step === 'explain' && (
                    <div className="text-[#A1A1AA]">
                      Each field is looked up verbatim from the artifact-signature registry. An unrecognized directory
                      gets <span className="text-[#FAFAFA]">no fabricated verdict</span> at all.
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Closing handoff into Safety Net */}
            <a
              href="#safety-section"
              className="group mt-4 flex items-center justify-between gap-3 rounded-lg border border-[#27272A] bg-[#18181B]/60 px-4 py-3 transition-colors hover:border-[#3F3F46] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#10B981] focus-visible:ring-offset-2 focus-visible:ring-offset-[#09090B]"
            >
              <span className="font-mono text-xs text-[#A1A1AA]">
                <span className="text-[#10B981]">$ devklean clean</span> moves what you just explained to the OS trash.
              </span>
              <ArrowDown className="h-4 w-4 shrink-0 text-[#10B981] transition-transform group-hover:translate-y-0.5" />
            </a>
          </div>

        </div>
      </div>
    </section>
  );
}

function Field({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div className="flex flex-col gap-0.5 sm:flex-row sm:gap-3">
      <dt className="w-32 shrink-0 text-[10px] uppercase tracking-wider text-[#A1A1AA]/50">{label}</dt>
      <dd className="text-[#FAFAFA]">{value}</dd>
    </div>
  );
}
