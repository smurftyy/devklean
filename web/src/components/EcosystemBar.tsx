import React from 'react';
import { HardDrive } from 'lucide-react';
import { ECOSYSTEMS } from '../data';

// Literal classes so Tailwind's JIT actually emits them (a runtime-built
// `group-hover:${...}` string would never be scanned).
const ICON_HOVER: Record<string, string> = {
  'Node.js': 'group-hover:text-emerald-400',
  Python: 'group-hover:text-sky-400',
  'Next.js': 'group-hover:text-zinc-100',
  'Generic caches': 'group-hover:text-amber-400',
};

// Minimal monochrome brand marks (single-path, currentColor) so each ecosystem
// reads as itself rather than an identical placeholder circle.
function EcosystemIcon({ name, className }: { name: string; className?: string }) {
  switch (name) {
    case 'Node.js':
      return (
        <svg viewBox="0 0 24 24" className={className} fill="currentColor" aria-hidden="true">
          <path d="M12 21.985c-.275 0-.532-.074-.772-.202l-2.439-1.448c-.365-.203-.182-.277-.072-.314.496-.165.588-.201 1.101-.493.056-.037.129-.02.185.017l1.87 1.12c.074.036.166.036.221 0l7.319-4.237c.074-.036.11-.11.11-.202V7.768c0-.091-.036-.165-.11-.201l-7.319-4.219c-.073-.037-.165-.037-.239 0L4.257 7.566c-.073.036-.11.129-.11.201v8.457c0 .073.037.166.11.202l1.996 1.157c1.082.548 1.762-.095 1.762-.735V8.502c0-.11.091-.221.22-.221h.936c.108 0 .22.092.22.221v8.347c0 1.449-.788 2.294-2.164 2.294-.422 0-.752 0-1.688-.46l-1.925-1.099a1.55 1.55 0 01-.771-1.34V7.786c0-.55.293-1.064.771-1.339l7.316-4.237a1.617 1.617 0 011.544 0l7.317 4.237c.479.274.771.789.771 1.339v8.458c0 .549-.293 1.063-.771 1.34l-7.317 4.236c-.24.128-.516.202-.771.202z" />
        </svg>
      );
    case 'Python':
      return (
        <svg viewBox="0 0 24 24" className={className} fill="currentColor" aria-hidden="true">
          <path d="M14.25.18l.9.2.73.26.59.3.45.32.34.34.25.34.16.33.1.3.04.26.02.2-.01.13V8.5l-.05.63-.13.55-.21.46-.26.38-.3.31-.33.25-.35.19-.35.14-.33.1-.3.07-.26.04-.21.02H8.77l-.69.05-.59.14-.5.22-.41.27-.33.32-.27.35-.2.36-.15.37-.1.35-.07.32-.04.27-.02.21v3.06H3.17l-.21-.03-.28-.07-.32-.12-.35-.18-.36-.26-.36-.36-.35-.46-.32-.59-.28-.73-.21-.88-.14-1.05-.05-1.23.06-1.22.16-1.04.24-.87.32-.71.36-.57.4-.44.42-.33.42-.24.4-.16.36-.1.32-.05.24-.01h.16l.06.01h8.16v-.83H6.18l-.01-2.75-.02-.37.05-.34.11-.31.17-.28.25-.26.31-.23.38-.2.44-.18.51-.15.58-.12.64-.1.71-.06.77-.04.84-.02 1.27.05zm-6.3 1.98l-.23.33-.08.41.08.41.23.34.33.22.41.09.41-.09.33-.22.23-.34.08-.41-.08-.41-.23-.33-.33-.22-.41-.09-.41.09zm13.09 3.95l.28.06.32.12.35.18.36.27.36.35.35.47.32.59.28.73.21.88.14 1.05.05 1.23-.06 1.23-.16 1.04-.24.86-.32.71-.36.57-.4.45-.42.33-.42.24-.4.16-.36.09-.32.05-.24.02-.16-.01h-8.22v.82h5.84l.01 2.76.02.36-.05.34-.11.31-.17.29-.25.25-.31.24-.38.2-.44.17-.51.15-.58.13-.64.09-.71.07-.77.04-.84.01-1.27-.04-1.07-.14-.9-.2-.73-.25-.59-.3-.45-.33-.34-.34-.25-.34-.16-.33-.1-.3-.04-.26-.02-.2.01-.13v-5.34l.05-.64.13-.54.21-.46.26-.38.3-.32.33-.24.35-.2.35-.14.33-.1.3-.06.26-.04.21-.02.13-.01h5.84l.69-.05.59-.14.5-.21.41-.28.33-.32.27-.35.2-.36.15-.36.1-.35.07-.32.04-.28.02-.21V6.07h2.09l.14.01zm-6.47 14.25l-.23.33-.08.41.08.41.23.33.33.23.41.08.41-.08.33-.23.23-.33.08-.41-.08-.41-.23-.33-.33-.23-.41-.08-.41.08z" />
        </svg>
      );
    case 'Next.js':
      return (
        <svg viewBox="0 0 24 24" className={className} fill="currentColor" aria-hidden="true">
          <path d="M11.5725 0c-.1763 0-.3098.0013-.3584.0067-.0516.0053-.2159.021-.3636.0328-3.4088.3073-6.6017 2.1463-8.624 4.9728C1.1004 6.584.3802 8.3666.1082 10.255c-.0962.659-.108.8537-.108 1.7474s.012 1.0884.108 1.7476c.652 4.506 3.8591 8.2919 8.2087 9.6945.7789.2511 1.6.4224 2.5337.5255.3636.04 1.9354.04 2.299 0 1.6117-.1783 2.9772-.5754 4.3237-1.2582.2065-.1047.2464-.1381.2183-.1611-.0188-.0139-.8987-1.1798-1.9543-2.5896l-1.919-2.5623-2.4047-3.5583c-1.3231-1.9564-2.4117-3.556-2.4211-3.556-.0094-.0026-.0187 1.5787-.0235 3.509-.0067 3.3802-.0093 3.5162-.0516 3.596-.061.115-.108.1618-.2064.2134-.075.0374-.1408.0445-.495.0445h-.406l-.1078-.068a.4383.4383 0 01-.1572-.1712l-.0493-.1056.0053-4.703.0067-4.7054.0726-.0915c.0376-.0493.1174-.1125.1736-.1417.0962-.047.1338-.0517.5396-.0517.4787 0 .5584.0187.6827.1547.0353.0377 1.3373 1.9987 2.895 4.3608a10760.433 10760.433 0 004.7344 7.1706l1.9002 2.8782.096-.0633c.8518-.5536 1.7525-1.3418 2.4657-2.1627 1.5179-1.7429 2.4963-3.868 2.8247-6.134.0961-.6591.108-.854.108-1.7475 0-.8937-.012-1.0884-.108-1.7476-.652-4.506-3.8591-8.2919-8.2087-9.6945-.7672-.2487-1.5836-.42-2.4985-.5232-.169-.0186-1.7847-.0399-2.1434-.0184zM17.9776 7.1974c.183 0 .2534.0234.3238.0656.0916.0563.1174.1032.1174.5772v7.0206l-.9962-1.4906V7.8402c0-.4271.007-.4634.0938-.5303.0704-.0563.1877-.0891.4574-.0891z" />
        </svg>
      );
    default: // Generic caches
      return (
        <svg viewBox="0 0 24 24" className={className} fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <ellipse cx="12" cy="5" rx="9" ry="3" />
          <path d="M3 5v14a9 3 0 0 0 18 0V5" />
          <path d="M3 12a9 3 0 0 0 18 0" />
        </svg>
      );
  }
}

export default function EcosystemBar() {
  return (
    <section id="ecosystem-section" className="w-full border-b border-[#27272A] bg-[#09090B]/40 py-10">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center justify-between gap-6 md:flex-row">
          {/* Section title */}
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-md border border-[#27272A] bg-[#18181B] text-[#A1A1AA]">
              <HardDrive className="h-4 w-4 text-[#10B981]" />
            </div>
            <div>
              <p className="font-mono text-xs font-bold uppercase tracking-wider text-[#A1A1AA]">
                Compatibility Layer
              </p>
              <h3 className="font-mono text-sm font-semibold text-[#FAFAFA]">
                Scans 4 Core Ecosystems
              </h3>
            </div>
          </div>

          {/* Grayscale -> Colored Grid */}
          <div className="grid w-full grid-cols-2 gap-4 sm:grid-cols-4 md:w-auto md:flex md:items-center md:gap-8">
            {ECOSYSTEMS.map((eco) => (
              <div
                key={eco.name}
                id={`eco-${eco.name.toLowerCase().replace(/[^a-z]/g, '')}`}
                className="group flex flex-col items-start rounded-lg border border-[#27272A] bg-[#18181B]/50 p-3 transition-all duration-300 md:border-0 md:bg-transparent md:p-0"
              >
                <div className="flex items-center gap-2">
                  <EcosystemIcon
                    name={eco.name}
                    className={`h-5 w-5 text-[#A1A1AA] transition-colors ${ICON_HOVER[eco.name] ?? ''}`}
                  />
                  <span className="font-mono text-sm font-semibold text-[#A1A1AA] transition-colors group-hover:text-[#FAFAFA]">
                    {eco.name}
                  </span>
                </div>
                <span className="mt-1 font-mono text-[10px] text-[#A1A1AA] transition-colors group-hover:text-[#FAFAFA]/70">
                  {eco.artifacts}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
