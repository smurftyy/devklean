import React from 'react';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import CommandWalkthrough from './components/CommandWalkthrough';
import SafetySection from './components/SafetySection';
import CalculatorSection from './components/CalculatorSection';
import FaqSection from './components/FaqSection';
import FooterSection from './components/FooterSection';

export default function App() {
  return (
    <div className="min-h-screen bg-[#111111] font-sans text-[#F5F5F5] antialiased">
      <Navbar />
      <main>
        <HeroSection />
        <CommandWalkthrough />
        <SafetySection />
        <CalculatorSection />
        <FaqSection />
      </main>
      <FooterSection />
    </div>
  );
}
