import React from 'react';
import { motion } from 'motion/react';
import { GitBranch, Info } from 'lucide-react';
import { STORY_BEATS } from '../data';

export default function StorySection() {
  return (
    <section id="story-section" className="w-full border-t border-[#27272A] bg-[#09090B]/60 py-20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">

        {/* Heading */}
        <div className="mb-14 text-center">
          <div className="inline-flex items-center gap-1.5 rounded-full border border-[#27272A] bg-[#18181B] px-3 py-1 font-mono text-xs font-medium text-[#10B981]">
            <GitBranch className="h-3.5 w-3.5" />
            How it grew
          </div>
          <h2 className="mt-4 text-3xl font-bold tracking-tight text-[#FAFAFA] sm:text-4xl font-sans">
            From a throwaway script to a utility.
          </h2>
        </div>

        {/* Timeline */}
        <ol className="relative grid gap-10 lg:grid-cols-4 lg:gap-6">
          {/* connecting rail — horizontal on lg, vertical on mobile */}
          <span
            aria-hidden="true"
            className="absolute left-[7px] top-2 h-[calc(100%-1rem)] w-px bg-[#27272A] lg:left-0 lg:top-[7px] lg:h-px lg:w-full"
          />

          {STORY_BEATS.map((beat, i) => (
            <motion.li
              key={beat.marker}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: '-60px' }}
              transition={{ delay: i * 0.12, duration: 0.4 }}
              className="relative pl-8 lg:pl-0 lg:pt-8"
            >
              {/* node dot */}
              <span className="absolute left-0 top-1 flex h-4 w-4 items-center justify-center rounded-full border-2 border-[#10B981] bg-[#09090B] lg:top-0">
                <span className="h-1.5 w-1.5 rounded-full bg-[#10B981]" />
              </span>

              <div className="font-mono text-xs font-bold text-[#10B981]">{beat.marker}</div>
              <h3 className="mt-1.5 font-sans text-lg font-bold text-[#FAFAFA]">{beat.title}</h3>
              <p
                className={`mt-2 font-sans text-sm leading-relaxed text-[#A1A1AA] ${
                  i === 0 ? 'italic' : ''
                }`}
              >
                {beat.body}
              </p>
            </motion.li>
          ))}
        </ol>

        {/* Grounding note */}
        <div className="mt-14 flex items-start gap-3 rounded-xl border border-[#27272A] bg-[#18181B]/50 p-5 sm:p-6">
          <Info className="mt-0.5 h-5 w-5 shrink-0 text-[#10B981]" />
          <p className="font-sans text-sm leading-relaxed text-[#A1A1AA]">
            The risk and confidence scores are a <span className="text-[#FAFAFA]">hand-maintained, deterministic
            registry</span> — not a model call and not a heuristic, as stated outright in the tool’s own source. And
            everything else shown on this page — commands, flags, sizes, the health formula — is{' '}
            <span className="text-[#FAFAFA]">real tool output, not marketing copy</span>.
          </p>
        </div>

      </div>
    </section>
  );
}
