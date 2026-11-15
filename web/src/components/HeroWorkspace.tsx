import React, { useId, useRef } from 'react';
import { useInView } from 'motion/react';
import { WORKSPACE_ARTIFACTS, formatSize } from '../data';

/** A schematic workspace, not a screenshot or a live scan of the visitor's files. */
export default function HeroWorkspace() {
  const id = useId().replace(/:/g, '');
  const sceneRef = useRef<HTMLDivElement>(null);
  const isInView = useInView(sceneRef, { once: true, amount: 0.15 });
  const paint = (name: string) => `url(#${id}-${name})`;
  const node = WORKSPACE_ARTIFACTS.find((item) => item.id === 'node_modules')!;
  const python = WORKSPACE_ARTIFACTS.find((item) => item.id === 'venv')!;
  const next = WORKSPACE_ARTIFACTS.find((item) => item.id === 'next')!;

  return (
    <div ref={sceneRef} className="hero-workspace" data-entered={isInView} aria-hidden="true">
      <svg className="hero-workspace__drawing" viewBox="0 0 1000 800" fill="none">
        <defs>
          <linearGradient id={`${id}-back`} x1="60" y1="0" x2="430" y2="430" gradientUnits="userSpaceOnUse">
            <stop stopColor="#5a5a59" /><stop offset=".38" stopColor="#292929" /><stop offset="1" stopColor="#171717" />
          </linearGradient>
          <linearGradient id={`${id}-front`} x1="70" y1="80" x2="570" y2="490" gradientUnits="userSpaceOnUse">
            <stop stopColor="#424241" /><stop offset=".38" stopColor="#2a2a29" /><stop offset="1" stopColor="#191919" />
          </linearGradient>
          <linearGradient id={`${id}-edge`} x1="0" y1="0" x2="610" y2="350" gradientUnits="userSpaceOnUse">
            <stop stopColor="#92928c" /><stop offset=".4" stopColor="#535350" /><stop offset="1" stopColor="#30302f" />
          </linearGradient>
          <linearGradient id={`${id}-paper`} x1="0" y1="0" x2="550" y2="250" gradientUnits="userSpaceOnUse">
            <stop stopColor="#bcbcb5" /><stop offset="1" stopColor="#555552" />
          </linearGradient>
          <pattern id={`${id}-grain`} width="5" height="5" patternUnits="userSpaceOnUse">
            <path d="M0 .5H1M3 3.5H4" stroke="#fff" strokeOpacity=".035" />
          </pattern>
          <filter id={`${id}-shadow`} x="-40%" y="-40%" width="190%" height="210%" colorInterpolationFilters="sRGB">
            <feDropShadow dx="-4" dy="24" stdDeviation="19" floodColor="#000" floodOpacity=".65" />
          </filter>
          <symbol id={`${id}-node`} viewBox="0 0 64 64">
            <path d="m32 3 25 14.5v29L32 61 7 46.5v-29Z" stroke="currentColor" strokeWidth="2.2" />
            <path d="M26 23v17c0 7-8 7-10 2M44 26c-2-5-13-4-13 1 0 6 15 3 15 10 0 7-13 8-16 1" stroke="currentColor" strokeWidth="2.6" strokeLinecap="round" />
          </symbol>
          {/* Colors sampled from the official Python and Node.js logo SVGs. */}
          <linearGradient id={`${id}-python-blue`} x1="0" y1="0" x2="1" y2="1">
            <stop stopColor="#5A9FD4" /><stop offset="1" stopColor="#306998" />
          </linearGradient>
          <linearGradient id={`${id}-python-yellow`} x1="0" y1="0" x2="1" y2="1">
            <stop stopColor="#FFE873" /><stop offset="1" stopColor="#FFD43B" />
          </linearGradient>
          <symbol id={`${id}-python`} viewBox="0 0 64 64">
            <path d="M31 5c-15 0-14 6-14 6v10h15v3H12S3 23 3 37s8 14 8 14h6V40s0-9 9-9h16s8 0 8-8V12s1-7-19-7Z" fill={paint('python-blue')} />
            <path d="M33 59c15 0 14-6 14-6V43H32v-3h20s9 1 9-13-8-14-8-14h-6v11s0 9-9 9H22s-8 0-8 8v11s-1 7 19 7Z" fill={paint('python-yellow')} />
            <circle cx="25" cy="13" r="2.4" fill="#FFFFFF" /><circle cx="39" cy="51" r="2.4" fill="#FFFFFF" />
          </symbol>
          <symbol id={`${id}-next`} viewBox="0 0 64 64">
            <circle cx="32" cy="32" r="28" fill="#000000" stroke="currentColor" strokeWidth="2" />
            <path d="M22 43V21l28 34M42 21v17" stroke="currentColor" strokeWidth="3.5" />
          </symbol>
        </defs>

        {/* Traces continue off-canvas: the workspace is larger than this view. */}
        <g className="hero-workspace__traces" stroke="#41413f" strokeWidth="1">
          <path d="M510-40v107a20 20 0 0 0 20 20h180M850 166h105a22 22 0 0 1 22 22v99h100M654 433h220a24 24 0 0 1 24 24v148h190M331 577v72a20 20 0 0 0 20 20h256M-80 738h300a22 22 0 0 0 22-22v-98" />
          <path d="M493 0v61a43 43 0 0 0 43 43h134M915 482v146h130" opacity=".4" />
          <circle cx="510" cy="28" r="4" fill="#111111" /><circle cx="898" cy="536" r="4" fill="#111111" />
        </g>
        <g className="hero-workspace__annotations" fontFamily="var(--font-mono)" fontSize="12" fill="#777773">
          <text x="530" y="36">~/projects/</text>
          <text x="912" y="524" transform="rotate(90 912 524)">LOCAL WORKSPACE / 001</text>
          <path d="M79 642h30m-15-15v30" stroke="#666662" />
          <text x="81" y="684">FILES STAY LOCAL.</text>
        </g>

        {/* Next.js project, tucked behind the main folder. */}
        <g className="hero-workspace__depth hero-workspace__depth--next">
          <g className="hero-workspace__next" transform="translate(638 56) rotate(12 140 100)">
            <g filter={paint('shadow')}>
              <path d="M0 28Q0 14 14 14h80l19 21h163q14 0 14 14v141q0 14-14 14H14q-14 0-14-14Z" fill={paint('back')} stroke={paint('edge')} />
              <path d="M1 72h288v119q0 13-13 13H14Q1 204 1 191Z" fill={paint('front')} stroke={paint('edge')} />
              <path d="M16 74h258" stroke="#7a7a73" strokeOpacity=".5" />
            </g>
            <use href={`#${id}-next`} x="26" y="94" width="49" height="49" color="#FFFFFF" />
            <text x="94" y="112" fontFamily="var(--font-mono)" fontSize="16" fill="#e1e1da">{next.dirName}/</text>
            <text x="94" y="135" fontFamily="var(--font-mono)" fontSize="11" fill="#aaa9a3">{formatSize(next.sizeMB)} · build output</text>
            <text x="27" y="180" fontFamily="var(--font-mono)" fontSize="10" fill="#8b8b85">~/projects/docs-site/</text>
          </g>
        </g>

        {/* The dominant folder echoes the exact stepped left edge of the brand. */}
        <g className="hero-workspace__depth hero-workspace__depth--main">
          <g className="hero-workspace__main" transform="translate(133 222) rotate(-9 310 195)">
            <g filter={paint('shadow')}>
              <path d="M35 19Q35 3 51 3h171l39 41h324q19 0 19 19v281q0 21-21 21H51q-16 0-16-16Z" fill={paint('back')} stroke={paint('edge')} strokeWidth="1.5" />
              <path d="M68 53h464q10 0 10 10v228H58V63q0-10 10-10Z" fill="#171717" stroke="#7d7d76" />
              <path d="M76 65h460v228H76Z" fill={paint('paper')} />
              <path d="M82 72h455M82 79h455M82 86h455" stroke="#d1d1c7" strokeOpacity=".4" />
              <path d="M40 103H588q18 0 18 18v254q0 20-20 20H40v-52H23v-34H40v-53H23v-34H40v-51H23v-33H40Z" fill={paint('front')} stroke={paint('edge')} strokeWidth="1.5" />
              <path d="M40 103H588q18 0 18 18" stroke="#a4a49b" strokeWidth="1.5" />
              <path d="M45 110H585" stroke="#0d0d0d" strokeWidth="2" />
              <path d="M40 117H593V375q0 13-13 13H40Z" fill={paint('grain')} />
              <path d="M58 383h520q17 0 19-16" stroke="#65655f" strokeOpacity=".5" />
            </g>
            {/* Static milled pixels: a brand detail, never a deletion animation. */}
            <g fill={paint('front')} stroke="#62625d" strokeWidth=".8">
              <path d="M-15 138H5v33h-20ZM-15 222H5v34h-20ZM-15 309H5v34h-20Z" />
              <path d="M-48 152h12v12h-12ZM-58 237h17v17h-17ZM-42 322h12v12h-12Z" />
            </g>
            <text x="90" y="31" fontFamily="var(--font-mono)" fontSize="11" letterSpacing="2" fill="#c3c3bb">DEV / WORKSPACE</text>
            <g transform="translate(76 146)">
              <path d="M0 8Q0 0 8 0h75q8 0 8 8v75q0 8-8 8H8q-8 0-8-8Z" fill="#202020" stroke="#555550" />
              <path d="M1 82V9q0-8 8-8h73" stroke="#111111" strokeWidth="2" />
              <use href={`#${id}-node`} x="16" y="14" width="60" height="60" color="#5FA04E" />
            </g>
            <text x="190" y="167" fontFamily="var(--font-mono)" fontSize="12" letterSpacing="1" fill="#a4a49c">DEPENDENCIES</text>
            <text x="188" y="206" fontFamily="var(--font-mono)" fontSize="29" fill="#e6e6df">{node.dirName}/</text>
            <text x="190" y="231" fontFamily="var(--font-mono)" fontSize="12" fill="#a4a49c">~/projects/web-app/</text>
            <path d="M76 269h482" stroke="#555550" />
            <text x="77" y="301" fontFamily="var(--font-mono)" fontSize="12" fill="#a4a49c">ARTIFACT FOOTPRINT</text>
            <text x="77" y="345" fontFamily="var(--font-sans)" fontSize="37" letterSpacing="-1" fill="#deded6">{formatSize(node.sizeMB)}</text>
            <g transform="translate(407 306)">
              <path d="M0 0h143v40H0Z" fill="#1b1b1b" stroke="#51514b" />
              <circle cx="17" cy="20" r="3" fill="#c7c7bc" />
              <text x="30" y="24" fontFamily="var(--font-mono)" fontSize="11" fill="#b5b5ab">INSPECT FIRST</text>
            </g>
          </g>
        </g>

        {/* Python folder overlaps the main object's lower edge in the same material. */}
        <g className="hero-workspace__depth hero-workspace__depth--python">
          <g className="hero-workspace__python" transform="translate(550 551) rotate(8 145 100)">
            <g filter={paint('shadow')}>
              <path d="M0 17Q0 3 14 3h83l20 23h163q14 0 14 14v154q0 14-14 14H14Q0 208 0 194Z" fill={paint('back')} stroke={paint('edge')} />
              <path d="M1 62h292v132q0 14-14 14H14Q1 208 1 194Z" fill={paint('front')} stroke={paint('edge')} />
              <path d="M14 66h265" stroke="#7b7b72" strokeOpacity=".5" />
            </g>
            <use href={`#${id}-python`} x="24" y="89" width="51" height="51" />
            <text x="95" y="107" fontFamily="var(--font-mono)" fontSize="19" fill="#e0e0d6">{python.dirName}/</text>
            <text x="95" y="131" fontFamily="var(--font-mono)" fontSize="11" fill="#aaa99f">{formatSize(python.sizeMB)} · environment</text>
            <path d="M25 157h243" stroke="#4e4e48" />
            <text x="25" y="182" fontFamily="var(--font-mono)" fontSize="11" fill="#8b8b81">~/projects/ml-api/</text>
          </g>
        </g>
      </svg>
    </div>
  );
}
