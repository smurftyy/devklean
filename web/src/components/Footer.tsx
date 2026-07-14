import React from 'react';
import { Github, Bug, Heart, Terminal, Shield } from 'lucide-react';

export default function Footer() {
  const currentYear = new Date().getFullYear();

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
              An lightweight, blazing-fast terminal daemon utility developed for active engineers who need to reclaim local storage without risking critical program builds.
            </p>
            <div className="flex items-center gap-2 font-mono text-[10px] text-[#A1A1AA]">
              <Shield className="h-3.5 w-3.5 text-[#10B981]" />
              <span>Zero telemetry. Completely local data lifecycle.</span>
            </div>
          </div>

          {/* Links Column 1 */}
          <div>
            <h4 className="font-mono text-xs font-bold text-[#FAFAFA] uppercase tracking-wider mb-3">
              Resources
            </h4>
            <ul className="space-y-2 font-sans text-xs text-[#A1A1AA]">
              <li>
                <a href="#hero-section" className="hover:text-[#FAFAFA] transition-colors">
                  Installation CLI
                </a>
              </li>
              <li>
                <a href="#calculator-section" className="hover:text-[#FAFAFA] transition-colors">
                  Space Savings Calculator
                </a>
              </li>
              <li>
                <a href="#demo-section" className="hover:text-[#FAFAFA] transition-colors">
                  Interactive Sandbox CLI
                </a>
              </li>
            </ul>
          </div>

          {/* Links Column 2 */}
          <div>
            <h4 className="font-mono text-xs font-bold text-[#FAFAFA] uppercase tracking-wider mb-3">
              Project Repo
            </h4>
            <ul className="space-y-2 font-sans text-xs text-[#A1A1AA]">
              <li>
                <a href="https://github.com" target="_blank" rel="noreferrer" className="hover:text-[#FAFAFA] flex items-center gap-1.5 transition-colors">
                  <Github className="h-3.5 w-3.5" />
                  GitHub Repository
                </a>
              </li>
              <li>
                <a href="https://github.com" target="_blank" rel="noreferrer" className="hover:text-[#FAFAFA] flex items-center gap-1.5 transition-colors">
                  <Bug className="h-3.5 w-3.5" />
                  Report An Issue
                </a>
              </li>
              <li>
                <a href="https://github.com" target="_blank" rel="noreferrer" className="hover:text-[#FAFAFA] flex items-center gap-1.5 transition-colors">
                  <Heart className="h-3.5 w-3.5 text-red-500" />
                  Become a Sponsor
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom copyright segment */}
        <div className="border-t border-[#27272A]/40 pt-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="font-mono text-[11px] text-[#A1A1AA]">
            &copy; {currentYear} DevKlean. Published under the Apache-2.0 License.
          </p>
          <div className="flex items-center gap-1.5 font-mono text-[11px] text-[#A1A1AA]">
            <span>Designed & Engineered by</span>
            <span className="font-semibold text-[#FAFAFA] hover:text-[#10B981] transition-colors cursor-pointer">
              @oladapooloyede185
            </span>
          </div>
        </div>

      </div>
    </footer>
  );
}
