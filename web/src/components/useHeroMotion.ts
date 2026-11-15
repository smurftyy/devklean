import { useEffect, useRef } from 'react';

/** Pointer-driven depth only on fine-pointer devices; no idle animation loop. */
export default function useHeroMotion() {
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    const hero = ref.current;
    if (!hero) return;
    const allowed = window.matchMedia('(prefers-reduced-motion: no-preference) and (hover: hover) and (pointer: fine) and (min-width: 1000px)');
    let frame = 0;
    let x = 0;
    let y = 0;

    const reset = () => {
      window.cancelAnimationFrame(frame);
      frame = 0;
      hero.style.removeProperty('--workspace-x');
      hero.style.removeProperty('--workspace-y');
      hero.style.removeProperty('--workspace-tilt');
    };
    const paint = () => {
      hero.style.setProperty('--workspace-x', `${x * 10}px`);
      hero.style.setProperty('--workspace-y', `${y * 7}px`);
      hero.style.setProperty('--workspace-tilt', `${x * 0.6}deg`);
      frame = 0;
    };
    const move = (event: PointerEvent) => {
      if (!allowed.matches || event.pointerType !== 'mouse') return;
      const rect = hero.getBoundingClientRect();
      x = Math.max(-1, Math.min(1, ((event.clientX - rect.left) / rect.width - 0.5) * 2));
      y = Math.max(-1, Math.min(1, ((event.clientY - rect.top) / rect.height - 0.5) * 2));
      if (!frame) frame = window.requestAnimationFrame(paint);
    };
    hero.addEventListener('pointermove', move);
    hero.addEventListener('pointerleave', reset);
    window.addEventListener('blur', reset);
    window.addEventListener('scroll', reset, { passive: true });
    allowed.addEventListener('change', reset);
    return () => {
      reset();
      hero.removeEventListener('pointermove', move);
      hero.removeEventListener('pointerleave', reset);
      window.removeEventListener('blur', reset);
      window.removeEventListener('scroll', reset);
      allowed.removeEventListener('change', reset);
    };
  }, []);

  return ref;
}
