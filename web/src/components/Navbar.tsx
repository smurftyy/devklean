import React, { useState } from 'react';
import { Github, Menu, X } from 'lucide-react';
import { DOCS_URL, REPO_URL } from '../data';
import DevKleanBrand from './DevKleanBrand';

export default function Navbar() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 w-full border-b border-[#333333] bg-[#111111]">
      <div className="mx-auto flex h-16 max-w-[1200px] items-center justify-between px-5 md:px-6 lg:px-8">
        {/* Left: pixel-dissolving folder brand lockup */}
        <a
          href="#top"
          aria-label="DevKlean home"
          className="inline-flex min-h-[44px] items-center text-[#F5F5F5] transition-opacity hover:opacity-85"
        >
          <DevKleanBrand variant="lockup" size="nav" />
        </a>

        {/* Desktop navigation */}
        <nav aria-label="Primary" className="hidden items-center gap-7 md:flex">
          <a
            href="#walkthrough"
            className="inline-flex min-h-[44px] items-center font-sans text-[14px] text-[#ADADAD] transition-colors hover:text-[#F5F5F5]"
          >
            How it works
          </a>
          <a
            href="#safety"
            className="inline-flex min-h-[44px] items-center font-sans text-[14px] text-[#ADADAD] transition-colors hover:text-[#F5F5F5]"
          >
            Safety
          </a>
          <a
            href={DOCS_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex min-h-[44px] items-center font-sans text-[14px] text-[#ADADAD] transition-colors hover:text-[#F5F5F5]"
          >
            Docs
          </a>
        </nav>

        {/* Right: restrained GitHub action + mobile menu button */}
        <div className="flex items-center gap-1">
          <a
            href={REPO_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex min-h-[44px] items-center gap-1.5 rounded-[6px] px-2.5 font-sans text-[14px] text-[#F5F5F5] transition-colors hover:bg-[#242424]"
          >
            <Github className="h-4 w-4 shrink-0" strokeWidth={1.6} aria-hidden="true" />
            <span className="hidden sm:inline">View on GitHub</span><span className="sm:hidden">GitHub</span>
            <span className="ml-1 text-[#ADADAD]" aria-hidden="true">
              ↗
            </span>
          </a>

          <button
            type="button"
            onClick={() => setMobileOpen((prev) => !prev)}
            aria-expanded={mobileOpen}
            aria-label={mobileOpen ? 'Close navigation menu' : 'Open navigation menu'}
            className="inline-flex min-h-[44px] min-w-[44px] items-center justify-center rounded-[6px] text-[#F5F5F5] transition-colors hover:bg-[#242424] md:hidden"
          >
            {mobileOpen ? (
              <X className="h-[18px] w-[18px]" strokeWidth={1.6} aria-hidden="true" />
            ) : (
              <Menu className="h-[18px] w-[18px]" strokeWidth={1.6} aria-hidden="true" />
            )}
          </button>
        </div>
      </div>

      {/* Mobile navigation drawer */}
      {mobileOpen && (
        <nav
          aria-label="Mobile"
          className="border-t border-[#333333] bg-[#111111] px-5 py-2 md:hidden"
        >
          <div className="flex flex-col divide-y divide-[#333333]">
            <a
              href="#walkthrough"
              onClick={() => setMobileOpen(false)}
              className="flex min-h-[44px] items-center font-sans text-[14px] text-[#F5F5F5]"
            >
              How it works
            </a>
            <a
              href="#safety"
              onClick={() => setMobileOpen(false)}
              className="flex min-h-[44px] items-center font-sans text-[14px] text-[#F5F5F5]"
            >
              Safety
            </a>
            <a
              href={DOCS_URL}
              target="_blank"
              rel="noopener noreferrer"
              onClick={() => setMobileOpen(false)}
              className="flex min-h-[44px] items-center justify-between font-sans text-[14px] text-[#F5F5F5]"
            >
              <span>Docs</span>
              <span className="text-[#ADADAD]" aria-hidden="true">
                ↗
              </span>
            </a>
          </div>
        </nav>
      )}
    </header>
  );
}
