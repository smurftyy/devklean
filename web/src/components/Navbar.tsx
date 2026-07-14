import React, { useState } from 'react';
import { Github, Twitter, Terminal, Star, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

export default function Navbar() {
  const [stars, setStars] = useState(4821);
  const [hasStarred, setHasStarred] = useState(false);
  const [showCelebration, setShowCelebration] = useState(false);

  const handleStarClick = () => {
    if (!hasStarred) {
      setStars((prev) => prev + 1);
      setHasStarred(true);
      setShowCelebration(true);
      setTimeout(() => setShowCelebration(false), 2000);
    } else {
      setStars((prev) => prev - 1);
      setHasStarred(false);
    }
  };

  return (
    <nav id="app-navbar" className="sticky top-0 z-50 w-full border-b border-[#27272A] bg-[#09090B]/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Logo */}
        <div className="flex items-center gap-2.5">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg border border-[#27272A] bg-[#18181B] text-[#10B981]">
            <Terminal className="h-5 w-5" />
          </div>
          <span className="font-mono text-lg font-bold tracking-tight text-[#FAFAFA]">
            Dev<span className="text-[#10B981]">K</span>lean
          </span>
          <span className="hidden rounded-full border border-[#10B981]/20 bg-[#10B981]/10 px-2 py-0.5 font-mono text-[10px] font-medium text-[#10B981] sm:inline-block">
            v1.2.0
          </span>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-3">
          {/* GitHub Star Button */}
          <div className="relative">
            <button
              id="btn-navbar-github-star"
              onClick={handleStarClick}
              className={`flex items-center gap-1.5 rounded-md border px-3 py-1.5 font-mono text-xs font-medium transition-all duration-200 ${
                hasStarred
                  ? 'border-[#10B981] bg-[#10B981]/10 text-[#10B981]'
                  : 'border-[#27272A] bg-[#18181B] text-[#FAFAFA] hover:bg-[#27272A]'
              }`}
            >
              <Github className="h-4 w-4" />
              <span className="hidden sm:inline">Star on GitHub</span>
              <div className="h-4 w-[1px] bg-[#27272A] mx-1"></div>
              <span className="flex items-center gap-0.5 font-semibold">
                <Star className={`h-3.5 w-3.5 fill-current ${hasStarred ? 'text-[#10B981]' : 'text-amber-400'}`} />
                {stars.toLocaleString()}
              </span>
            </button>

            {/* Micro-interaction celebration badge */}
            <AnimatePresence>
              {showCelebration && (
                <motion.div
                  initial={{ opacity: 0, y: 10, scale: 0.8 }}
                  animate={{ opacity: 1, y: -25, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.8 }}
                  className="absolute left-1/2 -translate-x-1/2 flex items-center gap-1 rounded-full bg-[#10B981] px-2.5 py-1 text-[10px] font-bold text-black shadow-lg shadow-[#10B981]/20 whitespace-nowrap"
                >
                  <Sparkles className="h-3 w-3" />
                  Starred! Thanks!
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Social Link */}
          <a
            id="link-navbar-twitter"
            href="https://x.com"
            target="_blank"
            rel="noopener noreferrer"
            className="flex h-8 w-8 items-center justify-center rounded-md border border-[#27272A] bg-[#18181B] text-[#A1A1AA] hover:bg-[#27272A] hover:text-[#FAFAFA] transition-colors"
            title="Follow DevKlean on X (Twitter)"
          >
            <Twitter className="h-4 w-4" />
          </a>
        </div>
      </div>
    </nav>
  );
}
