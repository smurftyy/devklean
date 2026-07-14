import React from 'react';
import { Github, Terminal } from 'lucide-react';

const REPO_URL = 'https://github.com/smurftyy/devklean';
const X_URL = 'https://x.com/Xanes_007';

export default function Navbar() {
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
            v1.1.0
          </span>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-3">
          {/* GitHub repository link */}
          <a
            id="link-navbar-github"
            href={REPO_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 rounded-md border border-[#27272A] bg-[#18181B] px-3 py-1.5 font-mono text-xs font-medium text-[#FAFAFA] transition-colors hover:bg-[#27272A] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#10B981] focus-visible:ring-offset-2 focus-visible:ring-offset-[#09090B]"
          >
            <Github className="h-4 w-4" />
            <span className="hidden sm:inline">View on GitHub</span>
          </a>

          {/* X (Twitter) link */}
          <a
            id="link-navbar-x"
            href={X_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="flex h-8 w-8 items-center justify-center rounded-md border border-[#27272A] bg-[#18181B] text-[#A1A1AA] transition-colors hover:bg-[#27272A] hover:text-[#FAFAFA] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#10B981] focus-visible:ring-offset-2 focus-visible:ring-offset-[#09090B]"
            title="Follow the maintainer on X"
          >
            {/* X logo (no dedicated lucide glyph) */}
            <svg viewBox="0 0 24 24" className="h-3.5 w-3.5 fill-current" aria-hidden="true">
              <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
            </svg>
          </a>
        </div>
      </div>
    </nav>
  );
}
