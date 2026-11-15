import React from 'react';
import { ArrowDown, ArrowRight, ShieldCheck } from 'lucide-react';
import InstallCopyButton from './InstallCopyButton';
import InstallHelp from './InstallHelp';
import HeroWorkspace from './HeroWorkspace';
import useHeroMotion from './useHeroMotion';
import './HeroSection.css';

export default function HeroSection() {
  const heroRef = useHeroMotion();

  return (
    <section ref={heroRef} id="top" className="devklean-hero" aria-labelledby="hero-title">
      <div className="hero-workbench" aria-hidden="true" />
      <div className="hero-content">
        <div className="hero-copy">
          <p className="hero-eyebrow"><span />A cleanup CLI for developers</p>
          <h1 id="hero-title">
            <span className="hero-title-line"><span>Your projects</span></span>{' '}
            <span className="hero-title-line"><span>leave things</span></span>{' '}
            <span className="hero-title-line hero-title-line--muted"><span>behind.</span></span>
          </h1>
          <p className="hero-description">
            Dependencies, caches, build files. They add up.
            DevKlean helps you inspect what can be regenerated,
            then deliberately move artifacts to your system trash.
          </p>
          <div id="install" className="hero-install">
            <p className="hero-install__label">Start locally. Inspect first.</p>
            <InstallCopyButton className="hero-install__button w-full sm:w-auto" />
            <div className="hero-install__meta">
              <span>Python 3.8+</span><span aria-hidden="true">/</span><span>macOS · Linux · Windows</span>
            </div>
            <InstallHelp />
          </div>
          <a className="hero-explore" href="#walkthrough">Explore the workflow <ArrowDown size={15} aria-hidden="true" /></a>
        </div>
      </div>
      <HeroWorkspace />
      <div className="hero-bottom">
        <p className="hero-trust"><ShieldCheck size={15} aria-hidden="true" />Open source<span>·</span>Local only<span>·</span>No telemetry</p>
        <p className="hero-scene-caption">Illustrative workspace <span>/</span> Nothing removed</p>
      </div>
      <div className="hero-process">
        <div className="hero-process__inner">
          <p className="hero-process__intro">YOUR WORKSPACE. YOUR CALL.</p>
          <ol aria-label="Cleanup workflow">
            <li><span>01</span>Inspect<ArrowRight className="hero-process__arrow" size={14} aria-hidden="true" /></li>
            <li><span>02</span>Review<ArrowRight className="hero-process__arrow" size={14} aria-hidden="true" /></li>
            <li><span>03</span>Confirm<ArrowRight className="hero-process__arrow" size={14} aria-hidden="true" /></li>
            <li><span>04</span>System trash</li>
          </ol>
        </div>
      </div>
    </section>
  );
}
