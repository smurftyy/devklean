import React from 'react';
import { Github } from 'lucide-react';
import { DOCS_URL, ISSUES_URL, LICENSE_URL, REPO_URL } from '../data';
import DevKleanBrand from './DevKleanBrand';
import InstallCopyButton from './InstallCopyButton';
import InstallHelp from './InstallHelp';

export default function FooterSection() {
  return (
    <footer className="w-full bg-[#111111]">
      {/* Closing statement */}
      <div className="mx-auto max-w-[1200px] px-5 py-14 md:px-6 md:py-20 lg:px-8">
        <div className="flex flex-col items-center text-center">
          <h2 className="max-w-[680px] font-sans text-[34px] font-medium leading-[1.08] tracking-[-0.03em] text-[#F5F5F5] md:text-[52px]">
            Make room for what you’re building.
          </h2>
          <div className="mt-8 w-full max-w-[350px] sm:w-auto sm:max-w-none">
            <InstallCopyButton className="w-full sm:w-auto sm:min-w-[272px]" />
            <InstallHelp />
          </div>
        </div>
      </div>

      {/* Compact footer */}
      <div className="border-t border-[#333333]">
        <div className="mx-auto flex max-w-[1200px] flex-col justify-between gap-4 px-5 py-6 sm:flex-row sm:items-center md:px-6 lg:px-8">
          <div className="flex items-center gap-3 font-mono text-[12px] text-[#ADADAD]">
            <DevKleanBrand variant="lockup" size="footer" />
            <span aria-hidden="true">·</span>
            <span>MIT License</span>
          </div>

          <nav aria-label="Footer" className="flex flex-wrap items-center gap-x-6 gap-y-1">
            <a
              href={REPO_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex min-h-[44px] items-center gap-1.5 font-sans text-[13px] text-[#ADADAD] transition-colors hover:text-[#F5F5F5]"
            >
              <Github className="h-4 w-4 shrink-0" strokeWidth={1.6} aria-hidden="true" />
              GitHub
            </a>
            <a
              href={DOCS_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex min-h-[44px] items-center font-sans text-[13px] text-[#ADADAD] transition-colors hover:text-[#F5F5F5]"
            >
              Documentation
            </a>
            <a
              href={ISSUES_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex min-h-[44px] items-center font-sans text-[13px] text-[#ADADAD] transition-colors hover:text-[#F5F5F5]"
            >
              Issues
            </a>
            <a
              href={LICENSE_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex min-h-[44px] items-center font-sans text-[13px] text-[#ADADAD] transition-colors hover:text-[#F5F5F5]"
            >
              License
            </a>
          </nav>
        </div>
      </div>
    </footer>
  );
}
