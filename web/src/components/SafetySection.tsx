import React, { useEffect, useRef, useState } from 'react';
import { Check, History, Minus, Plus, RotateCcw, Terminal, Trash2, X } from 'lucide-react';
import { useReducedMotion } from 'motion/react';

interface SafetyPoint {
  id: string;
  icon: React.ReactNode;
  title: string;
  plainSummary: string;
  technicalDetail: string;
}

const SAFETY_POINTS: SafetyPoint[] = [
  {
    id: 'trash',
    icon: <Trash2 className="h-[18px] w-[18px] shrink-0 text-[#F5F5F5]" strokeWidth={1.5} aria-hidden="true" />,
    title: 'Move selected artifacts to system trash.',
    plainSummary:
      'Cleaned folders are moved to your operating system’s Trash or Recycle Bin instead of being erased outright. Disk space is freed when you empty your trash, and recovery depends on your OS trash holding the item.',
    technicalDetail:
      'All removals route through send2trash to macOS Trash, Windows Recycle Bin, or Linux freedesktop trash. System roots, mounted drive roots, your home directory, and symbolic links are blocked by default.',
  },
  {
    id: 'confirm',
    icon: <Terminal className="h-[18px] w-[18px] shrink-0 text-[#F5F5F5]" strokeWidth={1.5} aria-hidden="true" />,
    title: 'Confirm large cleanups.',
    plainSummary:
      'With default settings, DevKlean asks before moving artifacts and requires typing DELETE when the batch reaches 1 GiB. Review the listed batch before confirming.',
    technicalDetail:
      'Standard cleanups prompt y/N. Removals meeting confirm_threshold (default 1 GiB) require typing DELETE verbatim — neither -y nor default_yes skips that check.',
  },
  {
    id: 'history',
    icon: <History className="h-[18px] w-[18px] shrink-0 text-[#F5F5F5]" strokeWidth={1.5} aria-hidden="true" />,
    title: 'Review cleanup history and recovery guidance.',
    plainSummary:
      'Past cleanups are recorded locally so you can check what was moved and when, along with plain instructions for restoring items from your system trash.',
    technicalDetail:
      'devklean history reads local deletion metadata (timestamp, size, item count, and strategy), and devklean restore prints OS-specific steps for Finder Trash, Recycle Bin, or Linux Trash.',
  },
];

const COMPRESS_STEPS = [
  { id: 'archive', label: 'Create archive', detail: 'Write sibling .tar.gz without modifying original' },
  { id: 'verify', label: 'Verify archive', detail: 'Test-extract entries and check file count' },
  { id: 'trash', label: 'Move archive to trash', detail: 'Send verified archive to OS trash' },
  { id: 'remove', label: 'Remove original folder', detail: 'Runs only after trash confirms receipt' },
] as const;

type SimPhase = 'idle' | 'running' | 'failed';

export default function SafetySection() {
  const shouldReduceMotion = useReducedMotion();
  const [openTechIds, setOpenTechIds] = useState<Record<string, boolean>>({});
  const [compressOpen, setCompressOpen] = useState(false);

  // Sample failure simulation state inside optional --compress disclosure
  const [simPhase, setSimPhase] = useState<SimPhase>('idle');
  const [simStep, setSimStep] = useState<number>(COMPRESS_STEPS.length); // 0..4
  const [simAnnouncement, setSimAnnouncement] = useState('');
  const timersRef = useRef<number[]>([]);

  const clearTimers = () => {
    timersRef.current.forEach((id) => window.clearTimeout(id));
    timersRef.current = [];
  };

  useEffect(() => {
    return () => clearTimers();
  }, []);

  const toggleTech = (id: string) => {
    setOpenTechIds((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const runFailureSimulation = () => {
    clearTimers();
    if (shouldReduceMotion) {
      setSimPhase('failed');
      setSimStep(2);
      setSimAnnouncement('Simulation stopped at step 3 (Move archive to trash). Original folder retained.');
      return;
    }

    setSimPhase('running');
    setSimStep(0);
    setSimAnnouncement('Running sample failure simulation.');

    timersRef.current.push(
      window.setTimeout(() => setSimStep(1), 160),
      window.setTimeout(() => setSimStep(2), 340),
      window.setTimeout(() => {
        setSimPhase('failed');
        setSimAnnouncement('Stopped — original retained. Step 4 did not run.');
      }, 520),
    );
  };

  const resetSimulation = () => {
    clearTimers();
    setSimPhase('idle');
    setSimStep(COMPRESS_STEPS.length);
    setSimAnnouncement('Simulation reset to normal verified order.');
  };

  return (
    <section id="safety" className="w-full scroll-mt-16 border-b border-[#333333] bg-[#111111] py-14 md:py-20">
      <div className="mx-auto max-w-[1200px] px-5 md:px-6 lg:px-8">
        <div className="grid gap-10 lg:grid-cols-12 lg:gap-12">
          {/* Narrow heading column */}
          <div className="lg:col-span-4">
            <h2 className="font-sans text-[32px] font-medium leading-[1.1] tracking-[-0.025em] text-[#F5F5F5] md:text-[42px]">
              Cleanup with a safety net.
            </h2>
            <p className="mt-4 font-sans text-[16px] leading-[1.6] text-[#ADADAD]">
              Plain, reversible defaults and explicit confirmation before folders leave your workspace.
            </p>
          </div>

          {/* Wider divided explanations column */}
          <div className="border-t border-[#333333] lg:col-span-8">
            {SAFETY_POINTS.map((point) => {
              const isTechOpen = !!openTechIds[point.id];
              return (
                <div key={point.id} className="border-b border-[#333333] py-6">
                  <div className="flex items-start gap-3.5">
                    <div className="mt-0.5">{point.icon}</div>
                    <div className="min-w-0 flex-1">
                      <h3 className="font-sans text-[17px] font-medium leading-[1.4] text-[#F5F5F5]">
                        {point.title}
                      </h3>
                      <p className="mt-2 max-w-[64ch] font-sans text-[15px] leading-[1.6] text-[#CECECE]">
                        {point.plainSummary}
                      </p>

                      <button
                        type="button"
                        onClick={() => toggleTech(point.id)}
                        aria-expanded={isTechOpen}
                        aria-controls={`safety-tech-${point.id}`}
                        aria-label={`${isTechOpen ? 'Hide' : 'Show'} technical details: ${point.title}`}
                        className="mt-2 inline-flex min-h-[44px] items-center gap-1.5 font-sans text-[13px] text-[#ADADAD] transition-colors hover:text-[#F5F5F5]"
                      >
                        {isTechOpen ? (
                          <Minus className="h-3.5 w-3.5" strokeWidth={1.6} aria-hidden="true" />
                        ) : (
                          <Plus className="h-3.5 w-3.5" strokeWidth={1.6} aria-hidden="true" />
                        )}
                        <span>{isTechOpen ? 'Hide technical details' : 'Technical details'}</span>
                      </button>

                      {isTechOpen && (
                        <p
                          id={`safety-tech-${point.id}`}
                          className="mt-1 max-w-[64ch] border-l border-[#333333] pl-3.5 font-sans text-[14px] leading-[1.6] text-[#ADADAD]"
                        >
                          {point.technicalDetail}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}

            {/* Optional compressed cleanup row + explicit simulation */}
            <div className="border-b border-[#333333]">
              <button
                type="button"
                onClick={() => setCompressOpen((prev) => !prev)}
                aria-expanded={compressOpen}
                aria-controls="compress-details"
                className="flex min-h-[58px] w-full items-center justify-between gap-4 py-4 text-left transition-colors hover:text-[#F5F5F5]"
              >
                <span className="font-sans text-[15px] text-[#CECECE] transition-colors hover:text-[#F5F5F5]">
                  Optional compressed cleanup (<code className="font-mono text-[13px] text-[#F5F5F5]">--compress</code>)
                </span>
                <span className="inline-flex h-6 w-6 shrink-0 items-center justify-center text-[#ADADAD]">
                  {compressOpen ? (
                    <Minus className="h-4 w-4" strokeWidth={1.6} aria-hidden="true" />
                  ) : (
                    <Plus className="h-4 w-4" strokeWidth={1.6} aria-hidden="true" />
                  )}
                </span>
              </button>

              {compressOpen && (
                <div id="compress-details" className="pb-6">
                  <p className="max-w-[64ch] font-sans text-[15px] leading-[1.6] text-[#CECECE]">
                    When <code className="font-mono text-[13px] text-[#F5F5F5]">--compress</code> is used on directories
                    at or above 10 MiB, DevKlean archives and verifies the folder first, moves the archive to trash,
                    and removes the original folder only at the end. Restoring a compressed item from trash requires
                    extracting the archive manually.
                  </p>

                  {/* Explicit failure simulation */}
                  <div className="mt-5 overflow-hidden rounded-[8px] border border-[#333333] bg-[#191919]">
                    <div className="flex flex-col justify-between gap-3 border-b border-[#333333] px-4 py-3 sm:flex-row sm:items-center">
                      <div>
                        <p className="font-sans text-[13px] font-medium text-[#F5F5F5]">
                          Sample failure simulation
                        </p>
                        <p className="font-sans text-[13px] text-[#ADADAD]">
                          Illustrative sequence showing what happens if trashing the archive fails.
                        </p>
                      </div>

                      <div className="flex flex-wrap items-center gap-2">
                        <button
                          type="button"
                          onClick={runFailureSimulation}
                          disabled={simPhase === 'running'}
                          className="inline-flex min-h-[44px] items-center justify-center rounded-[6px] border border-[#333333] bg-[#111111] px-3.5 py-2 font-sans text-[13px] font-medium text-[#F5F5F5] transition-colors hover:bg-[#242424] disabled:cursor-not-allowed disabled:text-[#ADADAD]"
                        >
                          {simPhase === 'running' ? 'Running simulation…' : 'Simulate failure'}
                        </button>

                        {simPhase !== 'idle' && (
                          <button
                            type="button"
                            onClick={resetSimulation}
                            className="inline-flex min-h-[44px] items-center gap-1.5 rounded-[6px] px-3 py-2 font-sans text-[13px] text-[#ADADAD] transition-colors hover:bg-[#242424] hover:text-[#F5F5F5]"
                          >
                            <RotateCcw className="h-3.5 w-3.5" strokeWidth={1.6} aria-hidden="true" />
                            <span>Reset</span>
                          </button>
                        )}
                      </div>
                    </div>

                    <ol className="divide-y divide-[#333333]">
                      {COMPRESS_STEPS.map((step, index) => {
                        let state: 'done' | 'failed' | 'skipped' | 'pending' = 'done';
                        if (simPhase === 'running') {
                          state = index < simStep ? 'done' : index === simStep ? 'pending' : 'skipped';
                        } else if (simPhase === 'failed') {
                          state = index < 2 ? 'done' : index === 2 ? 'failed' : 'skipped';
                        }

                        return (
                          <li
                            key={step.id}
                            className="flex items-start justify-between gap-4 px-4 py-3"
                          >
                            <div className="min-w-0">
                              <div className="font-sans text-[14px] font-medium text-[#F5F5F5]">
                                {index + 1}. {step.label}
                              </div>
                              <div className="mt-0.5 font-mono text-[12px] text-[#ADADAD]">{step.detail}</div>
                            </div>

                            <span className="inline-flex shrink-0 items-center gap-1.5 font-mono text-[12px] text-[#F5F5F5]">
                              {state === 'done' && (
                                <>
                                  <Check className="h-3.5 w-3.5" strokeWidth={1.8} aria-hidden="true" />
                                  <span>Done</span>
                                </>
                              )}
                              {state === 'failed' && (
                                <>
                                  <X className="h-3.5 w-3.5" strokeWidth={1.8} aria-hidden="true" />
                                  <span>Failed</span>
                                </>
                              )}
                              {state === 'skipped' && <span className="text-[#ADADAD]">Not run</span>}
                              {state === 'pending' && <span className="text-[#ADADAD]">Running</span>}
                            </span>
                          </li>
                        );
                      })}
                    </ol>

                    <div className="border-t border-[#333333] bg-[#111111] px-4 py-3 font-sans text-[14px] text-[#F5F5F5]">
                      {simPhase === 'failed' ? (
                        <span>Stopped — original retained. Step 4 never ran, so the folder stays untouched.</span>
                      ) : simPhase === 'running' ? (
                        <span className="text-[#ADADAD]">Simulating step-by-step execution…</span>
                      ) : (
                        <span className="text-[#CECECE]">
                          Normal order: original folder is removed only after all prior steps succeed.
                        </span>
                      )}
                    </div>

                    <div className="sr-only" aria-live="polite" aria-atomic="true">
                      {simAnnouncement}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
