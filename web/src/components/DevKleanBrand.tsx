import React from 'react';

interface DevKleanBrandProps {
  variant?: 'icon' | 'lockup';
  size?: 'nav' | 'footer';
  label?: string;
  className?: string;
}

const SIZE_CLASSES = {
  nav: {
    icon: 'h-6 w-6',
    wordmark: 'text-[15px]',
    gap: 'gap-2.5',
  },
  footer: {
    icon: 'h-5 w-5',
    wordmark: 'text-[14px]',
    gap: 'gap-2',
  },
};

export default function DevKleanBrand({
  variant = 'lockup',
  size = 'nav',
  label,
  className = '',
}: DevKleanBrandProps) {
  const styles = SIZE_CLASSES[size];
  const isLockup = variant === 'lockup';

  const mark = (
    <svg
      viewBox="3 7 25 18"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={`${styles.icon} shrink-0`}
      aria-hidden={isLockup || !label ? true : undefined}
      role={!isLockup && label ? 'img' : undefined}
      aria-label={!isLockup && label ? label : undefined}
    >
      {/* Secondary folder layer + trailing pixels */}
      <path d="M10 8H15L17 10H25C25.8284 10 26.5 10.6716 26.5 11.5V13.5H10V8Z" fill="#ADADAD" />
      <rect x="6" y="8" width="2" height="2" fill="#ADADAD" />
      <rect x="4" y="13.5" width="2" height="2" fill="#ADADAD" />
      <rect x="4.5" y="19.5" width="2" height="2" fill="#ADADAD" />
      {/* Main folder body + dissolving left-edge pixels */}
      <path d="M11.5 12H25C25.8284 12 26.5 12.6716 26.5 13.5V22.5C26.5 23.3284 25.8284 24 25 24H11.5V12Z" fill="#F5F5F5" />
      <rect x="9.5" y="12" width="2" height="2.5" fill="#F5F5F5" />
      <rect x="9.5" y="16.5" width="2" height="3" fill="#F5F5F5" />
      <rect x="9.5" y="21.5" width="2" height="2.5" fill="#F5F5F5" />
      <rect x="7" y="11.5" width="2" height="2" fill="#F5F5F5" />
      <rect x="7" y="16" width="2" height="2" fill="#F5F5F5" />
      <rect x="7" y="22" width="2" height="2" fill="#F5F5F5" />
    </svg>
  );

  if (!isLockup) {
    return mark;
  }

  return (
    <span className={`inline-flex items-center ${styles.gap} ${className}`}>
      {mark}
      <span className={`font-sans font-medium tracking-[-0.015em] text-[#F5F5F5] ${styles.wordmark}`}>
        DevKlean
      </span>
    </span>
  );
}
