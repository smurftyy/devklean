/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import EcosystemBar from './components/EcosystemBar';
import FeaturesGrid from './components/FeaturesGrid';
import SavingsCalculator from './components/SavingsCalculator';
import InteractiveDemo from './components/InteractiveDemo';
import Footer from './components/Footer';
import { REVIEWS } from './data';
import { Quote, MessageSquare, ShieldAlert, Sparkles } from 'lucide-react';

export default function App() {
  return (
    <div className="min-h-screen bg-[#09090B] text-[#FAFAFA] font-sans antialiased overflow-x-hidden">
      {/* 1. Header Navigation */}
      <Navbar />

      {/* 2. Primary Hero Segment */}
      <HeroSection />

      {/* 3. Compatibilities / Ecosystem bar */}
      <EcosystemBar />

      {/* 4. Core Capabilities (3-col) */}
      <FeaturesGrid />

      {/* 5. Custom Dynamic Space Savings Calculator */}
      <SavingsCalculator />

      {/* 6. Step-by-Step Command Workflow Simulation */}
      <InteractiveDemo />

      {/* 7. Testimonials & Social Proof Grid */}
      <section id="reviews-section" className="w-full bg-[#09090B]/40 py-20 border-t border-[#27272A]">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          
          <div className="mb-14 text-center">
            <div className="inline-flex items-center gap-1.5 rounded-full border border-[#27272A] bg-[#18181B] px-3 py-1 font-mono text-xs font-medium text-[#10B981]">
              <MessageSquare className="h-3.5 w-3.5" />
              Community Response
            </div>
            <h2 className="mt-4 text-3xl font-bold tracking-tight text-[#FAFAFA] sm:text-4xl">
              Trusted by performance-obsessed devs.
            </h2>
            <p className="mx-auto mt-3 max-w-xl text-sm text-[#A1A1AA]">
              See how other systems engineers, site reliability experts, and frontend architects keep their storage pipelines light and fully optimized.
            </p>
          </div>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {REVIEWS.map((review, i) => (
              <div
                key={i}
                id={`review-card-${i}`}
                className="relative rounded-xl border border-[#27272A] bg-[#18181B] p-6 hover:border-[#3F3F46] transition-colors flex flex-col justify-between"
              >
                <div>
                  <Quote className="h-8 w-8 text-[#10B981]/25 mb-4" />
                  <p className="font-sans text-sm italic leading-relaxed text-[#FAFAFA]">
                    "{review.quote}"
                  </p>
                </div>

                <div className="mt-6 flex items-center gap-3 border-t border-[#27272A]/55 pt-4">
                  <div className="flex h-9 w-9 items-center justify-center rounded-full bg-[#10B981]/10 border border-[#10B981]/20 font-mono text-xs font-bold text-[#10B981]">
                    {review.avatar}
                  </div>
                  <div>
                    <h4 className="font-sans text-xs font-bold text-[#FAFAFA]">
                      {review.author}
                    </h4>
                    <p className="font-sans text-[10px] text-[#A1A1AA]">
                      {review.role}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>

        </div>
      </section>

      {/* 8. Extra FAQ / Security Segment for conversion trust */}
      <section id="faq-section" className="w-full bg-black py-20 border-t border-[#27272A]">
        <div className="mx-auto max-w-4xl px-4 sm:px-6">
          <div className="mb-12 text-center">
            <h2 className="text-2xl font-bold tracking-tight text-[#FAFAFA] font-sans">
              Frequently Asked Questions
            </h2>
          </div>

          <div className="space-y-6">
            <div className="rounded-lg border border-[#27272A] bg-[#18181B] p-5">
              <h4 className="font-mono text-xs font-bold text-[#10B981] uppercase mb-1.5">
                Is DevKlean safe to run on active coding workspaces?
              </h4>
              <p className="font-sans text-xs text-[#A1A1AA] leading-relaxed">
                Absolutely. DevKlean utilizes an advanced dry-run process by default. It parses configurations like <code className="text-[#FAFAFA] bg-black px-1.5 py-0.5 rounded text-[11px]">.gitignore</code> and active file states, ensuring we only mark artifacts for purging that have been dormant. You always review a summary of folders before authorizing deletion.
              </p>
            </div>

            <div className="rounded-lg border border-[#27272A] bg-[#18181B] p-5">
              <h4 className="font-mono text-xs font-bold text-[#10B981] uppercase mb-1.5">
                How does the traversal engine achieve such high scan speeds?
              </h4>
              <p className="font-sans text-xs text-[#A1A1AA] leading-relaxed">
                The traversal daemon is constructed entirely using asynchronous multi-threaded workers. It reads files concurrently using native OS system loops rather than slow single-threaded Javascript array filters, letting it crawl massive nested monorepos in under a second.
              </p>
            </div>

            <div className="rounded-lg border border-[#27272A] bg-[#18181B] p-5">
              <h4 className="font-mono text-xs font-bold text-[#10B981] uppercase mb-1.5">
                Can I customize which build folders get searched?
              </h4>
              <p className="font-sans text-xs text-[#A1A1AA] leading-relaxed">
                Yes. Create a lightweight local <code className="text-[#FAFAFA] bg-black px-1.5 py-0.5 rounded text-[11px]">.devkleanrc</code> configuration file or pass specific directories directly using the CLI parameter like <code className="text-[#10B981] bg-black px-1.5 py-0.5 rounded text-[11px]">devklean scan --exclude ./my-custom-build</code>.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 9. Minimalist Footer */}
      <Footer />
    </div>
  );
}
