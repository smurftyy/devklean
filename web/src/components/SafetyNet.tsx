import React, { useEffect, useState } from 'react';
import { motion } from 'motion/react';
import { ShieldCheck, Check, X, Trash2, KeyRound, History } from 'lucide-react';

// The real --compress ordering from devklean.deletion (archive → verify → trash
// the archive → confirm → only then remove the original). A failure at ANY step
// leaves the source directory completely untouched.
const PIPELINE = [
  { title: 'Archive', detail: 'directory → sibling .tar.gz' },
  { title: 'Verify', detail: 'test-extract every entry + checksum' },
  { title: 'Trash archive', detail: 'send the .tar.gz to the OS trash' },
  { title: 'Confirm', detail: 'archive is safely in trash' },
  { title: 'Remove original', detail: 'only now is the source deleted' },
];

const FAIL_AT = 2; // step 3 (0-indexed): archive can't reach the trash

type NodeStatus = 'ok' | 'fail' | 'skipped';

export default function SafetyNet() {
  const [failMode, setFailMode] = useState(false);
  const [runId, setRunId] = useState(0);

  // Replay the staggered reveal whenever the mode is toggled.
  useEffect(() => setRunId((n) => n + 1), [failMode]);

  const statusFor = (i: number): NodeStatus => {
    if (!failMode) return 'ok';
    if (i < FAIL_AT) return 'ok';
    if (i === FAIL_AT) return 'fail';
    return 'skipped';
  };

  return (
    <section id="safety-section" className="w-full border-t border-[#27272A] bg-[#09090B] py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">

        {/* Heading */}
        <div className="mb-12 text-center">
          <div className="inline-flex items-center gap-1.5 rounded-full border border-[#27272A] bg-[#18181B] px-3 py-1 font-mono text-xs font-medium text-[#10B981]">
            <ShieldCheck className="h-3.5 w-3.5" />
            The Safety Net
          </div>
          <h2 className="mt-4 text-3xl font-bold tracking-tight text-[#FAFAFA] sm:text-4xl font-sans">
            Built to fail safe.
          </h2>
          <p className="mx-auto mt-3 max-w-2xl text-base text-[#A1A1AA] font-sans">
            When you compress before trashing, devklean removes the original <em>last</em>. If anything goes wrong
            before that, your directory is left exactly where it was.
          </p>
        </div>

        {/* Pipeline */}
        <div className="rounded-2xl border border-[#27272A] bg-[#18181B]/40 p-6 sm:p-8">
          <div className="mb-6 flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
            <h3 className="font-mono text-sm font-semibold text-[#FAFAFA]">
              <span className="text-[#10B981]">devklean clean --compress</span> · ordered for safety
            </h3>
            <button
              id="btn-simulate-failure"
              onClick={() => setFailMode((v) => !v)}
              className={`inline-flex items-center gap-1.5 rounded-md border px-3 py-1.5 font-mono text-xs transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-[#09090B] ${
                failMode
                  ? 'border-red-400/40 bg-red-400/10 text-red-400 focus-visible:ring-red-400'
                  : 'border-[#27272A] bg-[#18181B] text-[#A1A1AA] hover:text-[#FAFAFA] hover:border-[#3F3F46] focus-visible:ring-[#10B981]'
              }`}
            >
              {failMode ? <X className="h-3.5 w-3.5" /> : <ShieldCheck className="h-3.5 w-3.5" />}
              {failMode ? 'Reset to success' : 'Simulate a failure'}
            </button>
          </div>

          {/* Nodes */}
          <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-5">
            {PIPELINE.map((node, i) => {
              const status = statusFor(i);
              const styles =
                status === 'ok'
                  ? 'border-[#10B981]/40 bg-[#10B981]/[0.06]'
                  : status === 'fail'
                    ? 'border-red-400/50 bg-red-400/[0.07]'
                    : 'border-[#27272A] bg-[#0d0d0f] opacity-50';
              return (
                <motion.div
                  key={`${runId}-${i}`}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: status === 'skipped' ? 0.5 : 1, y: 0 }}
                  transition={{ delay: i * 0.18, duration: 0.35 }}
                  className={`relative rounded-xl border p-4 ${styles}`}
                >
                  <div className="mb-2 flex items-center justify-between">
                    <span className="font-mono text-[10px] uppercase tracking-wider text-[#A1A1AA]/60">
                      Step {i + 1}
                    </span>
                    <span
                      className={`flex h-5 w-5 items-center justify-center rounded-full ${
                        status === 'ok'
                          ? 'bg-[#10B981]/15 text-[#10B981]'
                          : status === 'fail'
                            ? 'bg-red-400/15 text-red-400'
                            : 'bg-[#27272A] text-[#52525B]'
                      }`}
                    >
                      {status === 'fail' ? <X className="h-3 w-3" /> : status === 'ok' ? <Check className="h-3 w-3" /> : '·'}
                    </span>
                  </div>
                  <div className="font-sans text-sm font-bold text-[#FAFAFA]">{node.title}</div>
                  <div className="mt-1 font-mono text-[10px] leading-relaxed text-[#A1A1AA]">{node.detail}</div>
                </motion.div>
              );
            })}
          </div>

          {/* Outcome banner */}
          <motion.div
            key={`banner-${runId}`}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: PIPELINE.length * 0.18 + 0.1 }}
            className={`mt-6 rounded-lg border p-4 font-mono text-xs ${
              failMode
                ? 'border-red-400/30 bg-red-400/[0.06] text-red-300'
                : 'border-[#10B981]/30 bg-[#10B981]/[0.06] text-[#10B981]'
            }`}
          >
            {failMode ? (
              <>
                <span className="font-bold">Step 3 failed → pipeline halts.</span> Steps 4–5 never run, and the original
                directory is left <span className="font-bold text-[#FAFAFA]">completely untouched</span>.
              </>
            ) : (
              <>
                <span className="font-bold">All five steps passed.</span> The archive is safely in trash and the
                original is removed — recoverable from trash if you need it back.
              </>
            )}
          </motion.div>
        </div>

        {/* Supporting cards */}
        <div className="mt-8 grid gap-6 md:grid-cols-3">
          <SafetyCard
            icon={<Trash2 className="h-5 w-5 text-[#10B981]" />}
            title="Trash, not delete"
            body="Every removal routes through send2trash to your OS's native trash — Recycle Bin, Finder Trash, or the freedesktop trash. Never rm -rf, so a mistake is always recoverable."
          />
          <SafetyCard
            icon={<KeyRound className="h-5 w-5 text-amber-400" />}
            title="The DELETE gate"
            body="Any deletion ≥ 1 GiB requires you to type DELETE, by hand. It is not skippable by -y / --yes — only a --dry-run bypasses it."
          />
          <SafetyCard
            icon={<History className="h-5 w-5 text-sky-400" />}
            title="restore & history"
            body="restore walks you through per-OS recovery from the trash devklean doesn't own. history logs every past cleanup — timestamp, size, item count, and strategy."
          />
        </div>

      </div>
    </section>
  );
}

function SafetyCard({ icon, title, body }: { icon: React.ReactNode; title: string; body: string }) {
  return (
    <div className="rounded-xl border border-[#27272A] bg-[#18181B] p-6">
      <div className="flex h-10 w-10 items-center justify-center rounded-lg border border-[#27272A] bg-[#09090B] shadow-inner">
        {icon}
      </div>
      <h3 className="mt-4 font-sans text-base font-bold text-[#FAFAFA]">{title}</h3>
      <p className="mt-2 font-sans text-sm leading-relaxed text-[#A1A1AA]">{body}</p>
    </div>
  );
}
