import React from 'react';
import { REPO_URL } from '../data';
import { Check, Terminal, Trash2 } from 'lucide-react';

export default function CleanupGuide() {
  return (
    <div id="cleanup" className="mt-10 scroll-mt-24 border-t border-[#333333] pt-8">
      <div className="mb-6 max-w-2xl">
        <p className="font-mono text-[11px] uppercase tracking-[0.12em] text-[#ADADAD]">From inspection to cleanup</p>
        <h3 className="mt-2 text-[24px] font-medium tracking-[-0.02em]">Preview the batch. Then decide.</h3>
        <p className="mt-2 text-[14px] leading-relaxed text-[#ADADAD]">An example workflow for macOS, Linux, and Windows. Replace <code className="font-mono text-[#F5F5F5]">./my-project</code> with your project folder. These examples don’t run commands on your computer.</p>
      </div>
      <ol className="grid gap-6 lg:grid-cols-3 lg:gap-8">
        <li className="min-w-0 border-t border-[#666666] pt-4">
          <h4 className="flex items-center gap-2 text-[15px] font-medium"><Terminal className="h-4 w-4" aria-hidden="true" />1. Preview what would move</h4>
          <code className="mt-3 block select-all break-words rounded-[6px] bg-[#191919] p-3 font-mono text-[13px] leading-relaxed">devklean clean ./my-project --dry-run</code>
          <p className="mt-3 text-[14px] leading-relaxed text-[#ADADAD]">Review the paths and sizes. This scans the project and reports the batch without changing files.</p>
        </li>
        <li className="min-w-0 border-t border-[#666666] pt-4">
          <h4 className="flex items-center gap-2 text-[15px] font-medium"><Check className="h-4 w-4" aria-hidden="true" />2. Confirm the listed batch</h4>
          <code className="mt-3 block select-all break-words rounded-[6px] bg-[#191919] p-3 font-mono text-[13px] leading-relaxed">devklean clean ./my-project</code>
          <p className="mt-3 text-[14px] leading-relaxed text-[#ADADAD]">This scans again and asks to move <strong className="font-medium text-[#F5F5F5]">all discovered artifacts</strong> under that project, respecting your exclusions. Review the fresh list before confirming.</p>
          <p className="mt-2 text-[13px] leading-relaxed text-[#ADADAD]">Defaults: y/N below 1 GiB; type DELETE at 1 GiB or more. Decline to leave the batch untouched.</p>
        </li>
        <li className="min-w-0 border-t border-[#666666] pt-4">
          <h4 className="flex items-center gap-2 text-[15px] font-medium"><Trash2 className="h-4 w-4" aria-hidden="true" />3. Review the result</h4>
          <div className="mt-3 rounded-[6px] border border-[#333333] p-3 text-[14px]">
            <p className="text-[12px] text-[#ADADAD]">Example successful outcome</p>
            <p className="mt-1 font-medium">Artifacts moved to system trash.</p>
          </div>
          <p className="mt-3 text-[14px] leading-relaxed text-[#ADADAD]">Restore items from your OS trash while they’re still there. <strong className="font-medium text-[#F5F5F5]">Empty the trash to free disk space</strong> once you’re sure you no longer need them.</p>
        </li>
      </ol>
      <p className="mt-6 border-t border-[#333333] pt-4 text-[13px] leading-relaxed text-[#ADADAD]">Want to choose individual folders? Use <code className="font-mono text-[#F5F5F5]">devklean clean ./my-project -i</code> on macOS or Linux. On Windows, use a narrower project path or <a href={`${REPO_URL}#configuration`} target="_blank" rel="noopener noreferrer" className="text-[#F5F5F5] underline underline-offset-4">configured exclusions</a> to control the batch.</p>
    </div>
  );
}
