import { EcosystemItem, FaqItem, WorkspaceArtifact } from './types';

export const REPO_URL = 'https://github.com/smurftyy/devklean';
export const DOCS_URL = 'https://github.com/smurftyy/devklean#readme';
export const ISSUES_URL = 'https://github.com/smurftyy/devklean/issues';
export const LICENSE_URL = 'https://github.com/smurftyy/devklean/blob/main/LICENSE';
export const INSTALL_COMMAND = 'pipx install devklean';

export function formatSize(mb: number): string {
  return mb >= 1024 ? `${(mb / 1024).toFixed(2)} GB` : `${mb.toFixed(1)} MB`;
}

export const ECOSYSTEM_ITEMS: EcosystemItem[] = [
  { id: 'nodejs', name: 'Node.js', artifacts: 'node_modules' },
  { id: 'python', name: 'Python', artifacts: '.venv · venv · __pycache__' },
  { id: 'nextjs', name: 'Next.js', artifacts: '.next' },
  { id: 'caches', name: 'Build caches', artifacts: 'dist · .cache' },
];

// Illustrative workspace matching the four core directory types in the hero
// and walkthrough. Signature metadata mirrors src/devklean/signatures/registry.py.
export const WORKSPACE_ARTIFACTS: WorkspaceArtifact[] = [
  {
    id: 'node_modules',
    dirName: 'node_modules',
    path: '~/projects/web-app/node_modules',
    sizeMB: 1270,
    ecosystem: 'Node.js (npm/yarn/pnpm)',
    risk: 'low',
    confidence: 0.98,
    generatedBy: 'npm install / yarn install / pnpm install, from package.json and a lockfile',
    regenerateCommand: 'npm install (or yarn install / pnpm install, matching your lockfile)',
    rationale:
      "Directory name is npm/Node's own convention; contents are fully reproducible from package.json plus a lockfile.",
    staleDays: 34,
    lockfileConflict: true,
  },
  {
    id: 'venv',
    dirName: '.venv',
    path: '~/projects/ml-api/.venv',
    sizeMB: 418,
    ecosystem: 'Python (venv)',
    risk: 'low',
    confidence: 0.95,
    generatedBy: 'python -m venv, populated via pip from a requirements/lock file',
    regenerateCommand: 'python -m venv .venv && .venv/bin/pip install -r requirements.txt',
    rationale:
      'Standard virtualenv layout (pyvenv.cfg, bin/lib); reproducible from a requirements file, though the exact install set depends on which file was originally used.',
    staleDays: 62,
  },
  {
    id: 'next',
    dirName: '.next',
    path: '~/projects/docs-site/.next',
    sizeMB: 212,
    ecosystem: 'Next.js',
    risk: 'low',
    confidence: 0.95,
    generatedBy: "next build / next dev, from the project's Next.js source",
    regenerateCommand: 'next build (or next dev, which regenerates dev artifacts on the fly)',
    rationale:
      "Directory name is Next.js's own build-output convention; reproducible from source via the Next.js CLI.",
    staleDays: 12,
  },
  {
    id: 'dist',
    dirName: 'dist',
    path: '~/projects/cli-core/dist',
    sizeMB: 48.4,
    ecosystem: 'Generic build tooling (bundler/compiler output)',
    risk: 'medium',
    confidence: 0.7,
    generatedBy: 'whatever build step the project defines (webpack, tsc, vite, build.sh, ...)',
    regenerateCommand: 'run the project’s documented build command (e.g. npm run build)',
    rationale:
      "'dist' is a widely shared convention across many toolchains rather than one tool's signature — usually build output, but devklean cannot prove which build command produced it.",
    staleDays: 19,
  },
];

export const FAQ_ITEMS: FaqItem[] = [
  {
    id: 'safe',
    question: 'Is it safe for active projects?',
    answer:
      'scan, analyze, and explain are read-only and never modify or delete files. Standard clean confirms the entire discovered batch under your chosen project path, respecting exclusions. It sends those directories to your operating system trash rather than running rm -rf, refuses protected system paths and symlinks by default, and, with default settings, requires typing DELETE for batches at or above 1 GiB. Active projects may need dependencies reinstalled or build files regenerated after cleanup.',
  },
  {
    id: 'exclude',
    question: 'Can I exclude folders?',
    answer:
      'Yes. Add a project-level .devklean.toml (discovered by walking up from your current directory) or a global ~/.config/devklean/config.toml. You can exclude directory names via exclude = [...] or list specific paths and folder names under [ignore].',
  },
  {
    id: 'install',
    question: 'How do I install it?',
    answer:
      'DevKlean is pure Python (3.8+) published on PyPI. With pipx already installed, run pipx install devklean for an isolated CLI install, or pip install devklean into an activated Python virtual environment. Then run devklean scan inside a project folder for a read-only first look. Add the optional zstd extra via pip install "devklean[zstd]" if you want Zstandard compressed cleanup.',
  },
  {
    id: 'windows',
    question: 'Does it work on Windows?',
    answer:
      'Yes. All core commands — scan, clean, analyze, explain, history, doctor, and restore — run on Windows, macOS, and Linux, using the Recycle Bin on Windows. The only exception is interactive TUI selection (devklean clean -i), which is Linux and macOS only because it uses Python’s curses module.',
  },
];
