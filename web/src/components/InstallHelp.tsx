import React from 'react';

export default function InstallHelp() {
  return (
    <details className="mt-2 w-full max-w-[44ch] text-left font-sans text-[13px] leading-relaxed text-[#ADADAD]">
      <summary className="min-h-[44px] cursor-pointer py-3 text-[#F5F5F5] underline decoration-[#666666] underline-offset-4">
        Installation help
      </summary>
      <div className="space-y-3 border-l border-[#666666] pl-4 pb-2">
        <p>Requires Python 3.8+. The recommended command uses pipx. Run it in your terminal.</p>
        <p>If pipx is missing, follow the <a className="text-[#F5F5F5] underline underline-offset-4" href="https://pipx.pypa.io/stable/installation/" target="_blank" rel="noopener noreferrer">pipx setup guide ↗</a>. You can also run <code className="select-all font-mono text-[#F5F5F5]">pip install devklean</code> inside an activated Python virtual environment.</p>
        <p>Then open a project folder in your terminal and run <code className="select-all font-mono text-[#F5F5F5]">devklean scan</code>. This first scan is read-only.</p>
      </div>
    </details>
  );
}
