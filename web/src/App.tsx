import React from 'react';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import EcosystemBar from './components/EcosystemBar';
import SavingsCalculator from './components/SavingsCalculator';
import FeaturesGrid from './components/FeaturesGrid';
import InteractiveDemo from './components/InteractiveDemo';
import SafetyNet from './components/SafetyNet';
import StorySection from './components/StorySection';
import Footer from './components/Footer';

const FAQS = [
  {
    q: 'Is it safe to run on active projects?',
    a: (
      <>
        <code className="rounded bg-black px-1.5 py-0.5 text-[11px] text-[#FAFAFA]">scan</code>,{' '}
        <code className="rounded bg-black px-1.5 py-0.5 text-[11px] text-[#FAFAFA]">analyze</code>, and{' '}
        <code className="rounded bg-black px-1.5 py-0.5 text-[11px] text-[#FAFAFA]">explain</code> never delete
        anything. When you do run <code className="rounded bg-black px-1.5 py-0.5 text-[11px] text-[#FAFAFA]">clean</code>,
        it moves items to your system trash — and anything ≥ 1&nbsp;GiB requires typing{' '}
        <code className="rounded bg-black px-1.5 py-0.5 text-[11px] text-[#FAFAFA]">DELETE</code>. See the Safety Net
        above for the full picture.
      </>
    ),
  },
  {
    q: 'Can I control which folders it looks at?',
    a: (
      <>
        Yes — through config, not a CLI flag. Add a project{' '}
        <code className="rounded bg-black px-1.5 py-0.5 text-[11px] text-[#FAFAFA]">.devklean.toml</code> (found by
        walking up from your current directory) or a global{' '}
        <code className="rounded bg-black px-1.5 py-0.5 text-[11px] text-[#FAFAFA]">~/.config/devklean/config.toml</code>,
        and set <code className="rounded bg-black px-1.5 py-0.5 text-[11px] text-[#10B981]">exclude = [...]</code> or{' '}
        an <code className="rounded bg-black px-1.5 py-0.5 text-[11px] text-[#10B981]">[ignore]</code> section with{' '}
        <code className="rounded bg-black px-1.5 py-0.5 text-[11px] text-[#FAFAFA]">paths</code> /{' '}
        <code className="rounded bg-black px-1.5 py-0.5 text-[11px] text-[#FAFAFA]">directories</code>.
      </>
    ),
  },
  {
    q: 'How do I install it?',
    a: (
      <>
        devklean is on PyPI — pure Python, no compiled binary.{' '}
        <code className="rounded bg-black px-1.5 py-0.5 text-[11px] text-[#10B981]">pipx install devklean</code> is
        recommended (isolated), or{' '}
        <code className="rounded bg-black px-1.5 py-0.5 text-[11px] text-[#10B981]">pip install devklean</code> into the
        current environment.
      </>
    ),
  },
  {
    q: 'Does it work on Windows?',
    a: (
      <>
        Yes. Every core command — <code className="rounded bg-black px-1.5 py-0.5 text-[11px] text-[#FAFAFA]">scan</code>,{' '}
        <code className="rounded bg-black px-1.5 py-0.5 text-[11px] text-[#FAFAFA]">clean</code>,{' '}
        <code className="rounded bg-black px-1.5 py-0.5 text-[11px] text-[#FAFAFA]">analyze</code>, and the rest — works
        on Linux, macOS, and Windows. The only exception is interactive mode (
        <code className="rounded bg-black px-1.5 py-0.5 text-[11px] text-[#FAFAFA]">-i</code>), which is Linux/macOS only.
      </>
    ),
  },
];

export default function App() {
  return (
    <div className="min-h-screen bg-[#09090B] text-[#FAFAFA] font-sans antialiased overflow-x-hidden">
      <Navbar />
      <HeroSection />
      <EcosystemBar />
      <SavingsCalculator />
      <FeaturesGrid />
      <InteractiveDemo />
      <SafetyNet />
      <StorySection />

      {/* FAQ */}
      <section id="faq-section" className="w-full bg-black py-20 border-t border-[#27272A]">
        <div className="mx-auto max-w-4xl px-4 sm:px-6">
          <div className="mb-12 text-center">
            <h2 className="text-2xl font-bold tracking-tight text-[#FAFAFA] font-sans">Frequently Asked Questions</h2>
          </div>

          <div className="space-y-6">
            {FAQS.map((faq, i) => (
              <div key={i} className="rounded-lg border border-[#27272A] bg-[#18181B] p-5">
                <h4 className="mb-1.5 font-mono text-xs font-bold uppercase text-[#10B981]">{faq.q}</h4>
                <p className="font-sans text-xs leading-relaxed text-[#A1A1AA]">{faq.a}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
