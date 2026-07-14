import { SimulatedProject, CommandStep } from './types';

export const SIMULATED_PROJECTS: SimulatedProject[] = [
  {
    id: '1',
    name: 'react-portfolio-app',
    type: 'node',
    path: '~/projects/web/react-portfolio-app',
    artifactSize: 480,
    artifactName: 'node_modules',
    filesCount: 28410
  },
  {
    id: '2',
    name: 'rust-blockchain-node',
    type: 'rust',
    path: '~/projects/crypto/rust-blockchain-node',
    artifactSize: 8420,
    artifactName: 'target',
    filesCount: 142050
  },
  {
    id: '3',
    name: 'ml-price-predictor',
    type: 'python',
    path: '~/projects/ai/ml-price-predictor',
    artifactSize: 2150,
    artifactName: '.venv',
    filesCount: 18920
  },
  {
    id: '4',
    name: 'nextjs-saas-dashboard',
    type: 'node',
    path: '~/projects/saas/nextjs-saas-dashboard',
    artifactSize: 350,
    artifactName: 'node_modules',
    filesCount: 19450
  },
  {
    id: '5',
    name: 'raytracer-engine',
    type: 'rust',
    path: '~/projects/graphics/raytracer-engine',
    artifactSize: 2800,
    artifactName: 'target',
    filesCount: 38400
  }
];

export const COMMAND_STEPS: CommandStep[] = [
  {
    name: 'Install',
    command: 'npm install -g devklean',
    description: 'Install globally via npm or fetch the standalone Rust/Go executable directly from GitHub releases.',
    badge: 'Step 1'
  },
  {
    name: 'Scan',
    command: 'devklean scan',
    description: 'Recursively search your workspace for build artifacts. Reviews folders without modifying anything.',
    badge: 'Step 2'
  },
  {
    name: 'Purge',
    command: 'devklean purge',
    description: 'Interactively select which projects to clean. Safely release gigabytes of disk space instantly.',
    badge: 'Step 3'
  }
];

export const FEATURES = [
  {
    id: 'lightning-fast',
    title: 'Lightning Fast',
    description: 'Built on a core asynchronous directory walker. Scans hundreds of thousands of directories in milliseconds without blocking your system.',
    badge: 'Rust Engine',
    details: 'Leverages thread pool processing to scan massive nested monorepos in under a second.'
  },
  {
    id: 'interactive-safe',
    title: 'Interactive & Safe',
    description: 'Review every directory, its size, and last active date before purging. Safe defaults prevent deletion of active project builds.',
    badge: 'Dry-Run Guard',
    details: 'Includes a preview dry-run mode and customizable excludes (.gitignore, .npmignore) to secure essential code.'
  },
  {
    id: 'multi-language',
    title: 'Multi-Language Ecosystem',
    description: 'Supports deep artifact identification across popular runtimes and packages. Cleans node_modules, target, .venv, and __pycache__.',
    badge: 'Universal CLI',
    details: 'One unified tool with intelligent detection that adjusts patterns according to the detected project type.'
  }
];

export const ECOSYSTEMS = [
  { name: 'Node.js', icon: 'Javascript', label: 'node_modules & dist', color: 'text-emerald-400' },
  { name: 'Rust Cargo', icon: 'Rust', label: 'target & registry', color: 'text-amber-500' },
  { name: 'Python venv', icon: 'Python', label: '.venv, venv & __pycache__', color: 'text-blue-400' },
  { name: 'Go Build', icon: 'Go', label: 'pkg/mod & build cache', color: 'text-sky-400' }
];

export const REVIEWS = [
  {
    quote: "DevKlean reclaimed 45GB of space on my MacBook Pro in under 12 seconds. It's now part of my weekly cron routine.",
    author: "Sarah Jenkins",
    role: "Senior Software Engineer, Vercel",
    avatar: "SJ"
  },
  {
    quote: "I used to write custom bash scripts to find nested node_modules. DevKlean replaces all of them with a lightning-fast, safe interactive interface.",
    author: "Alex Rivera",
    role: "Open Source Maintainer",
    avatar: "AR"
  },
  {
    quote: "The interactive multi-select is amazing. I can clean up rust cargo builds from 3 months ago while keeping my active projects compiled.",
    author: "Linus Lindqvist",
    role: "Rust Contributor",
    avatar: "LL"
  }
];
