import React, { useState, useEffect, useRef } from 'react';
import { Terminal, Play, RotateCcw, CheckCircle, Flame, Copy, Check } from 'lucide-react';
import { COMMAND_STEPS, SIMULATED_PROJECTS } from '../data';
import { CommandStep } from '../types';

export default function InteractiveDemo() {
  const [activeStepIndex, setActiveStepIndex] = useState(0);
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);
  
  // Terminal simulation states
  const [terminalLines, setTerminalLines] = useState<string[]>([]);
  const [isSimulating, setIsSimulating] = useState(false);
  const [simulationProgress, setSimulationProgress] = useState(0);
  const terminalBottomRef = useRef<HTMLDivElement>(null);

  // Install Lines
  const installSequence = [
    '# Initiating global CLI package installation...',
    'npm install -g devklean',
    ' ',
    'fetch metadata: https://registry.npmjs.org/devklean',
    'resolved dependency tree in 184ms',
    ' ',
    'dependencies added:',
    '  + devklean-cli-core@1.2.0 (compiled native rust binary)',
    '  + devklean-analyzer@1.0.4',
    ' ',
    '✔ devklean globally registered. Type `devklean --help` to start.',
  ];

  // Scan Lines
  const scanSequence = [
    '# Scanning workspace for build artifacts and virtual environments...',
    'devklean scan',
    ' ',
    '🔍 Traversing directories starting from current working directory...',
    'Analyzing: ~/projects/web-app/node_modules ...',
    'Analyzing: ~/projects/rust-service/target ...',
    'Analyzing: ~/projects/python-model/.venv ...',
    ' ',
    '--- SCAN RESULTS SUMMARY ---',
    '⚡ Completed traversal in 480ms (124,540 directories parsed)',
    ' ',
    'ID   PATH                                   TYPE          SIZE     FILES',
    '1    ~/projects/web/react-portfolio-app     node_modules  480.0 MB  28,410',
    '2    ~/projects/crypto/rust-blockchain-node target/       8.22 GB  142,050',
    '3    ~/projects/ai/ml-price-predictor       .venv/        2.10 GB   18,920',
    '4    ~/projects/saas/nextjs-saas-dashboard  node_modules  350.0 MB  19,450',
    '5    ~/projects/graphics/raytracer-engine   target/       2.73 GB   38,400',
    ' ',
    '⚠ TOTAL POTENTIAL RECLAIMABLE STORAGE: 14.23 GB',
    '👉 Run `devklean purge` to interactively clean these workspace folders.',
  ];

  // Purge sequence requires special timing
  const runInstallationSimulation = () => {
    setIsSimulating(true);
    setTerminalLines([]);
    setSimulationProgress(0);
    
    let currentLine = 0;
    const interval = setInterval(() => {
      if (currentLine < installSequence.length) {
        setTerminalLines(prev => [...prev, installSequence[currentLine]]);
        currentLine++;
      } else {
        clearInterval(interval);
        setIsSimulating(false);
      }
    }, 180);
  };

  const runScanningSimulation = () => {
    setIsSimulating(true);
    setTerminalLines([]);
    setSimulationProgress(0);

    let currentLine = 0;
    const interval = setInterval(() => {
      if (currentLine < scanSequence.length) {
        setTerminalLines(prev => [...prev, scanSequence[currentLine]]);
        currentLine++;
      } else {
        clearInterval(interval);
        setIsSimulating(false);
      }
    }, 120);
  };

  const runPurgingSimulation = () => {
    setIsSimulating(true);
    setTerminalLines([]);
    setSimulationProgress(0);

    const lines = [
      '# Launching interactive artifact purge routine...',
      'devklean purge',
      ' ',
      '⏳ Loading candidate directory registry...',
      'Found 5 directories matching prune thresholds (14.23 GB total)',
      ' ',
      '✔ Selected all 5 directories for removal.',
      '⚠ WARNING: This action cannot be undone. Reclaiming 14.23 GB.',
      'Proceed with deletion? [y/N] y',
      ' ',
      'Purging artifacts...',
    ];

    let currentLine = 0;
    const interval = setInterval(() => {
      if (currentLine < lines.length) {
        setTerminalLines(prev => [...prev, lines[currentLine]]);
        currentLine++;
      } else {
        clearInterval(interval);
        
        // Start Progress Bar Animation
        let progress = 0;
        const progressInterval = setInterval(() => {
          if (progress <= 100) {
            setSimulationProgress(progress);
            progress += 10;
          } else {
            clearInterval(progressInterval);
            
            // Append final success messages
            setTerminalLines(prev => [
              ...prev,
              ' ',
              '✔ [1/5] Purged: ~/projects/web/react-portfolio-app/node_modules (480.0 MB)',
              '✔ [2/5] Purged: ~/projects/crypto/rust-blockchain-node/target (8.22 GB)',
              '✔ [3/5] Purged: ~/projects/ai/ml-price-predictor/.venv (2.10 GB)',
              '✔ [4/5] Purged: ~/projects/saas/nextjs-saas-dashboard/node_modules (350.0 MB)',
              '✔ [5/5] Purged: ~/projects/graphics/raytracer-engine/target (2.73 GB)',
              ' ',
              '🔥 PURGE SEQUENCE COMPLETED SUCCESSFULLY',
              '✨ TOTAL SPACE RECLAIMED: 14.23 Gigabytes',
              '⏱ Elapsed process duration: 1.48 seconds',
              '🎉 Your local disk is now 14.23 GB lighter. Keep it klean!'
            ]);
            setIsSimulating(false);
          }
        }, 100);
      }
    }, 150);
  };

  const handleStepClick = (index: number) => {
    if (isSimulating) return;
    setActiveStepIndex(index);
    if (index === 0) runInstallationSimulation();
    if (index === 1) runScanningSimulation();
    if (index === 2) runPurgingSimulation();
  };

  const triggerActiveSimulation = () => {
    if (isSimulating) return;
    if (activeStepIndex === 0) runInstallationSimulation();
    if (activeStepIndex === 1) runScanningSimulation();
    if (activeStepIndex === 2) runPurgingSimulation();
  };

  useEffect(() => {
    // Initial run
    runInstallationSimulation();
  }, []);

  useEffect(() => {
    if (terminalBottomRef.current) {
      terminalBottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [terminalLines, simulationProgress]);

  const copyToClipboard = (text: string, index: number) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  return (
    <section id="demo-section" className="w-full border-t border-[#27272A] bg-[#09090B]/80 py-24">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        
        {/* Title */}
        <div className="mb-16 text-center">
          <div className="inline-flex items-center gap-1.5 rounded-full border border-[#27272A] bg-[#18181B] px-3 py-1 font-mono text-xs font-medium text-[#10B981]">
            <Terminal className="h-3.5 w-3.5" />
            Interactive Workflow
          </div>
          <h2 className="mt-4 text-3xl font-bold tracking-tight text-[#FAFAFA] sm:text-4xl font-sans">
            Three simple commands. Ultimate control.
          </h2>
          <p className="mx-auto mt-3 max-w-2xl text-base text-[#A1A1AA] font-sans">
            Review DevKlean's simple CLI api. Click on each card below to execute its corresponding command inside our mock browser emulator.
          </p>
        </div>

        {/* Split Screen Grid */}
        <div className="grid gap-10 lg:grid-cols-12 items-start">
          
          {/* Left Side: Step cards */}
          <div className="space-y-4 lg:col-span-5">
            {COMMAND_STEPS.map((step, idx) => {
              const isActive = activeStepIndex === idx;
              return (
                <div
                  key={idx}
                  id={`demo-step-card-${idx}`}
                  onClick={() => handleStepClick(idx)}
                  className={`group relative cursor-pointer rounded-xl border p-5 transition-all duration-300 ${
                    isActive
                      ? 'border-[#10B981] bg-[#18181B] shadow-lg shadow-[#10B981]/5'
                      : 'border-[#27272A] bg-[#18181B]/50 hover:border-[#3F3F46] hover:bg-[#18181B]'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className={`font-mono text-xs font-bold uppercase tracking-widest ${isActive ? 'text-[#10B981]' : 'text-[#A1A1AA]'}`}>
                      {step.badge}
                    </span>
                    <button
                      id={`btn-copy-demo-cmd-${idx}`}
                      onClick={(e) => {
                        e.stopPropagation();
                        copyToClipboard(step.command, idx);
                      }}
                      className="rounded border border-[#27272A] bg-black p-1.5 text-[#A1A1AA] hover:text-[#FAFAFA] hover:border-[#3F3F46] transition-colors"
                      title="Copy command to clipboard"
                    >
                      {copiedIndex === idx ? <Check className="h-3.5 w-3.5 text-[#10B981]" /> : <Copy className="h-3.5 w-3.5" />}
                    </button>
                  </div>

                  <h3 className="mt-3 font-sans text-lg font-bold text-[#FAFAFA]">
                    {step.name}
                  </h3>
                  
                  <div className="mt-2.5 inline-flex items-center gap-1.5 rounded bg-black px-2.5 py-1 font-mono text-xs text-[#10B981] border border-[#27272A]/50">
                    <span className="text-[#A1A1AA]">$</span> {step.command}
                  </div>

                  <p className="mt-3 font-sans text-xs leading-relaxed text-[#A1A1AA]">
                    {step.description}
                  </p>

                  {/* Active Indicator Bar */}
                  {isActive && (
                    <div className="absolute left-0 top-1/4 h-1/2 w-1 rounded-r-full bg-[#10B981]"></div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Right Side: Simulated Terminal Block */}
          <div className="lg:col-span-7">
            <div className="rounded-xl border border-[#27272A] bg-[#000000] p-4 font-mono text-xs shadow-2xl relative">
              
              {/* Terminal Window Top Bar */}
              <div className="flex items-center justify-between border-b border-[#27272A] pb-3 mb-4">
                <div className="flex items-center gap-1.5">
                  <div className="h-3 w-3 rounded-full bg-red-500"></div>
                  <div className="h-3 w-3 rounded-full bg-yellow-500"></div>
                  <div className="h-3 w-3 rounded-full bg-green-500"></div>
                </div>
                <div className="flex items-center gap-1.5 text-[11px] text-[#A1A1AA] font-semibold">
                  <Terminal className="h-3.5 w-3.5 text-[#10B981]" />
                  devklean - v1.2.0 (bash)
                </div>
                <div className="flex items-center gap-2">
                  <button
                    id="btn-terminal-run-again"
                    onClick={triggerActiveSimulation}
                    disabled={isSimulating}
                    className={`flex items-center gap-1 rounded border border-[#27272A] bg-[#18181B] px-2 py-0.5 text-[10px] text-[#A1A1AA] hover:text-[#FAFAFA] hover:border-[#3F3F46] transition-colors ${
                      isSimulating ? 'opacity-50 cursor-not-allowed' : ''
                    }`}
                    title="Restart this step simulation"
                  >
                    <RotateCcw className="h-3 w-3" />
                    Restart
                  </button>
                </div>
              </div>

              {/* Terminal body */}
              <div className="h-[360px] overflow-y-auto px-1 space-y-1.5 scrollbar-thin select-all">
                {terminalLines.map((line, i) => {
                  const safeLine = line || '';
                  let textClass = 'text-[#A1A1AA]';
                  if (safeLine.startsWith('#')) {
                    textClass = 'text-[#A1A1AA]/50 italic';
                  } else if (safeLine.startsWith('✔') || safeLine.includes('SUCCESSFULLY') || safeLine.startsWith('✨')) {
                    textClass = 'text-[#10B981]';
                  } else if (safeLine.startsWith('🔍') || safeLine.startsWith('Analyzing')) {
                    textClass = 'text-[#A1A1AA]/80';
                  } else if (safeLine.startsWith('⚠')) {
                    textClass = 'text-amber-500';
                  } else if (safeLine.startsWith('npm install') || safeLine.startsWith('devklean')) {
                    textClass = 'text-[#FAFAFA] font-bold';
                  } else if (safeLine.startsWith('---')) {
                    textClass = 'text-[#27272A]';
                  }

                  return (
                    <div key={i} className={`leading-relaxed whitespace-pre-wrap ${textClass}`}>
                      {safeLine.startsWith('npm install') || safeLine.startsWith('devklean') ? (
                        <span className="text-[#10B981] mr-1.5">$</span>
                      ) : null}
                      {safeLine}
                    </div>
                  );
                })}

                {/* Simulated Progress Bar for Purging */}
                {activeStepIndex === 2 && simulationProgress > 0 && (
                  <div className="space-y-1 mt-2.5">
                    <div className="flex items-center justify-between text-[#10B981] text-[11px] font-bold">
                      <span>Purge Progress:</span>
                      <span>{simulationProgress}%</span>
                    </div>
                    <div className="h-3 w-full bg-[#18181B] rounded overflow-hidden border border-[#27272A]">
                      <div
                        className="h-full bg-[#10B981] transition-all duration-100 ease-out"
                        style={{ width: `${simulationProgress}%` }}
                      ></div>
                    </div>
                  </div>
                )}

                {/* Flashing terminal cursor at the end when idle */}
                {!isSimulating && (
                  <div className="flex items-center gap-1.5 text-[#10B981] mt-2">
                    <span>$</span>
                    <span className="h-4 w-1.5 bg-[#10B981] animate-cursor-blink"></span>
                  </div>
                )}

                <div ref={terminalBottomRef}></div>
              </div>

            </div>
          </div>

        </div>

      </div>
    </section>
  );
}
