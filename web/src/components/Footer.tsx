import React from 'react';
import { Github, Bug, Terminal, Shield } from 'lucide-react';

const REPO_URL = 'https://github.com/smurftyy/devklean';
const ISSUES_URL = 'https://github.com/smurftyy/devklean/issues';
const PROFILE_URL = 'https://github.com/smurftyy';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  const linkClass =
    'hover:text-[#FAFAFA] flex items-center gap-1.5 transition-colors rounded-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#10B981] focus-visible:ring-offset-2 focus-visible:ring-offset-black';

  return (
    <footer id="app-footer" className="w-full border-t border-[#27272A] bg-black py-12">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">

        <div className="grid gap-8 md:grid-cols-4 mb-10">
          {/* Logo Column */}
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center gap-2">
              <div className="flex h-7 w-7 items-center justify-center rounded bg-[#10B981]/10 border border-[#10B981]/20 text-[#10B981]">
                <Terminal className="h-4 w-4" />
              </div>
              <span className="font-mono text-sm font-bold tracking-tight text-[#FAFAFA]">
                Dev<span className="text-[#10B981]">K</span>lean
              </span>
            </div>
            <p className="font-sans text-xs text-[#A1A1AA] max-w-sm leading-relaxed">
              A lightweight, open-source command-line tool for engineers who want to reclaim local storage without
              risking anything they can’t regenerate.
            </p>
            <div className="flex items-center gap-2 font-mono text-[10px] text-[#A1A1AA]">
              <Shield className="h-3.5 w-3.5 text-[#10B981]" />
              <span>Zero telemetry. Everything stays on your machine.</span>
            </div>
          </div>

          {/* Links Column 1 */}
          <div>
            <h4 className="font-mono text-xs font-bold text-[#FAFAFA] uppercase tracking-wider mb-3">
              On this page
            </h4>
            <ul className="space-y-2 font-sans text-xs text-[#A1A1AA]">
              <li>
                <a href="#features-section" className="rounded-sm transition-colors hover:text-[#FAFAFA] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#10B981] focus-visible:ring-offset-2 focus-visible:ring-offset-black">
                  Commands
                </a>
              </li>
              <li>
                <a href="#calculator-section" className="rounded-sm transition-colors hover:text-[#FAFAFA] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#10B981] focus-visible:ring-offset-2 focus-visible:ring-offset-black">
                  Space Savings Calculator
                </a>
              </li>
              <li>
                <a href="#demo-section" className="rounded-sm transition-colors hover:text-[#FAFAFA] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#10B981] focus-visible:ring-offset-2 focus-visible:ring-offset-black">
                  Interactive Demo
                </a>
              </li>
              <li>
                <a href="#safety-section" className="rounded-sm transition-colors hover:text-[#FAFAFA] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#10B981] focus-visible:ring-offset-2 focus-visible:ring-offset-black">
                  Safety Net
                </a>
              </li>
            </ul>
          </div>

          {/* Links Column 2 */}
          <div>
            <h4 className="font-mono text-xs font-bold text-[#FAFAFA] uppercase tracking-wider mb-3">
              Project
            </h4>
            <ul className="space-y-2 font-sans text-xs text-[#A1A1AA]">
              <li>
                <a href={REPO_URL} target="_blank" rel="noreferrer" className={linkClass}>
                  <Github className="h-3.5 w-3.5" />
                  GitHub Repository
                </a>
              </li>
              <li>
                <a href={ISSUES_URL} target="_blank" rel="noreferrer" className={linkClass}>
                  <Bug className="h-3.5 w-3.5" />
                  Report an Issue
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom copyright segment */}
        <div className="border-t border-[#27272A]/40 pt-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="font-mono text-[11px] text-[#A1A1AA]">
            &copy; {currentYear} DevKlean. Released under the MIT License.
          </p>
          <div className="flex items-center gap-1.5 font-mono text-[11px] text-[#A1A1AA]">
            <span>Designed &amp; engineered by</span>
            <a
              href={PROFILE_URL}
              target="_blank"
              rel="noreferrer"
              className="font-semibold text-[#FAFAFA] transition-colors hover:text-[#10B981] rounded-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#10B981] focus-visible:ring-offset-2 focus-visible:ring-offset-black"
            >
              @smurftyy
            </a>
          </div>
        </div>

      </div>
    </footer>
  );
}
