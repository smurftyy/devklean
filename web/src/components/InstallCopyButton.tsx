import React, { useEffect, useRef, useState } from 'react';
import { Copy } from 'lucide-react';
import { INSTALL_COMMAND } from '../data';

interface InstallCopyButtonProps {
  className?: string;
}

export default function InstallCopyButton({ className = '' }: InstallCopyButtonProps) {
  const [status, setStatus] = useState<'idle' | 'copied' | 'error'>('idle');
  const timer = useRef<number | undefined>(undefined);
  useEffect(() => () => window.clearTimeout(timer.current), []);

  const handleCopy = async () => {
    window.clearTimeout(timer.current);
    try {
      await navigator.clipboard.writeText(INSTALL_COMMAND);
      setStatus('copied');
      timer.current = window.setTimeout(() => setStatus('idle'), 2000);
    } catch {
      setStatus('error');
    }
  };

  return (
    <div className="w-full sm:w-auto">
      <button
        type="button"
        onClick={handleCopy}
        aria-label={`Copy installation command: ${INSTALL_COMMAND}`}
        className={`inline-flex min-h-[44px] max-w-full items-center justify-between gap-3 rounded-[6px] bg-[#F5F5F5] px-4 py-2.5 font-mono text-[13px] font-medium text-[#111111] hover:bg-[#E2E2E2] active:bg-[#D4D4D4] ${className}`}
      >
        <span>{INSTALL_COMMAND}</span>
        <span className="inline-flex shrink-0 items-center gap-1.5" aria-hidden="true">
          <span className="w-[6ch] text-right font-sans text-[11px]">{status === 'copied' ? 'Copied' : 'Copy'}</span>
          <Copy className="h-4 w-4 shrink-0" />
        </span>
      </button>
      <div role="status" aria-atomic="true" className={status === 'error' ? 'max-w-[38ch] text-left font-sans text-[13px] leading-relaxed text-[#CECECE]' : 'sr-only'}>
        {status === 'copied' && 'Installation command copied.'}
        {status === 'error' && <p className="mt-2">Couldn’t copy. Select and copy this command: <code className="select-all font-mono text-[#F5F5F5]">{INSTALL_COMMAND}</code></p>}
      </div>
    </div>
  );
}
