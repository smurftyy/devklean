import React, { useState } from 'react';
import { Zap, Shield, Code, ChevronDown, ChevronUp, Terminal, Cpu, CheckCircle } from 'lucide-react';
import { FEATURES } from '../data';
import { motion, AnimatePresence } from 'motion/react';

export default function FeaturesGrid() {
  const [activeSpecs, setActiveSpecs] = useState<string | null>(null);

  const toggleSpecs = (id: string) => {
    if (activeSpecs === id) {
      setActiveSpecs(null);
    } else {
      setActiveSpecs(id);
    }
  };

  const renderIcon = (id: string) => {
    switch (id) {
      case 'lightning-fast':
        return <Zap className="h-5 w-5 text-[#10B981]" />;
      case 'interactive-safe':
        return <Shield className="h-5 w-5 text-amber-500" />;
      case 'multi-language':
        default:
        return <Code className="h-5 w-5 text-blue-400" />;
    }
  };

  const getBorderColor = (id: string) => {
    if (activeSpecs === id) {
      if (id === 'lightning-fast') return 'border-[#10B981]';
      if (id === 'interactive-safe') return 'border-amber-500';
      return 'border-blue-500';
    }
    return 'border-[#27272A] hover:border-[#3F3F46]';
  };

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
            Engineered for speed, built for safety.
          </h2>
          <p className="mx-auto mt-3 max-w-2xl text-base text-[#A1A1AA] font-sans">
            Clean up old builds, untracked testing logs, and deep nested virtual environments 
            without breaking active production dependencies.
          </p>
        </div>

        {/* 3 Columns Grid */}
        <div className="grid gap-6 md:grid-cols-3">
          {FEATURES.map((feature) => {
            const isSpecsOpen = activeSpecs === feature.id;
            return (
              <div
                key={feature.id}
                id={`feature-card-${feature.id}`}
                className={`group flex flex-col justify-between rounded-xl border bg-[#18181B] p-6 transition-all duration-300 ${getBorderColor(
                  feature.id
                )}`}
              >
                <div>
                  {/* Badge & Icon Row */}
                  <div className="flex items-center justify-between">
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg border border-[#27272A] bg-[#09090B] shadow-inner">
                      {renderIcon(feature.id)}
                    </div>
                    <span className="font-mono text-[10px] uppercase tracking-wider text-[#A1A1AA] bg-[#09090B] px-2.5 py-0.5 rounded border border-[#27272A]">
                      {feature.badge}
                    </span>
                  </div>

                  {/* Title & Description */}
                  <h3 className="mt-6 font-sans text-xl font-bold text-[#FAFAFA]">
                    {feature.title}
                  </h3>
                  <p className="mt-3 font-sans text-sm leading-relaxed text-[#A1A1AA]">
                    {feature.description}
                  </p>
                </div>

                {/* Spec Button / Expandable */}
                <div className="mt-6 border-t border-[#27272A]/60 pt-4">
                  <button
                    id={`btn-feature-specs-${feature.id}`}
                    onClick={() => toggleSpecs(feature.id)}
                    className="flex w-full items-center justify-between font-mono text-xs text-[#A1A1AA] hover:text-[#FAFAFA] transition-colors"
                  >
                    <span className="flex items-center gap-1.5">
                      <Terminal className="h-3.5 w-3.5" />
                      {isSpecsOpen ? 'Hide Tech Specs' : 'View Tech Specs'}
                    </span>
                    {isSpecsOpen ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
                  </button>

                  <AnimatePresence>
                    {isSpecsOpen && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="overflow-hidden"
                      >
                        <div className="mt-3 rounded-lg bg-[#000000] border border-[#27272A] p-3 font-mono text-xs text-[#A1A1AA]">
                          <div className="flex items-center gap-1.5 text-[#10B981] mb-1.5 font-semibold">
                            <CheckCircle className="h-3.5 w-3.5" />
                            Verified Output:
                          </div>
                          <p className="text-[#A1A1AA] text-[11px] leading-relaxed">
                            {feature.details}
                          </p>
                          <div className="mt-2 text-[10px] text-[#A1A1AA]/50 border-t border-[#27272A]/50 pt-1.5 flex justify-between">
                            <span>Status: STABLE</span>
                            <span>Engine v1.2</span>
                          </div>
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              </div>
            );
          })}
        </div>

      </div>
    </section>
  );
}
