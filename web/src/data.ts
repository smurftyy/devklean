import { DemoProject, Feature, Ecosystem, StoryBeat } from './types';

// The four ecosystems devklean's scanner actually recognizes, sourced from
// devklean.config.defaults.DEFAULT_TARGETS / the signature registry.
export const ECOSYSTEMS: Ecosystem[] = [
  { name: 'Node.js', artifacts: 'node_modules', accent: 'text-emerald-400' },
  { name: 'Python', artifacts: 'venv · .venv · env · __pycache__', accent: 'text-sky-400' },
  { name: 'Next.js', artifacts: '.next', accent: 'text-zinc-100' },
  { name: 'Generic caches', artifacts: 'dist · .cache', accent: 'text-amber-400' },
];

// Phase 3 — the three read-only commands that make up devklean's differentiated
// layer. `clean` is the only command that deletes; these three never do.
export const FEATURES: Feature[] = [
  {
    id: 'scan',
    command: 'devklean scan',
    title: 'Scan',
    description:
      'Walks your workspace, finds cleanable directories, and reports each one’s size. It never deletes — it only shows you what is there.',
    sampleOutput: 'node_modules   612.0 MB',
  },
  {
    id: 'analyze',
    command: 'devklean analyze',
    title: 'Analyze',
    description:
      'Cross-references every match against the artifact-signature registry — risk tier, confidence, staleness — and reports a 0–100 workspace-health score. Unrecognized directories get no fabricated verdict.',
    sampleOutput: 'workspace health   82/100',
  },
  {
    id: 'explain',
    command: 'devklean explain PATH',
    title: 'Explain',
    description:
      'Looks up a single directory: what generates it, how to regenerate it, its risk tier and confidence, and the reasoning behind the call — straight from the registry entry.',
    sampleOutput: '.next → Next.js · low risk',
  },
];

// Phase 4 — the demo workspace. Every field below is copied verbatim from
// src/devklean/signatures/registry.py so the analyze/explain steps show real
// registry data, not invented verdicts.
export const DEMO_PROJECTS: DemoProject[] = [
  {
    id: 'node',
    dirName: 'node_modules',
    path: '~/projects/web/portfolio',
    sizeMB: 1240,
    ecosystem: 'Node.js (npm/yarn/pnpm)',
    risk: 'low',
    confidence: 0.98,
    generatedBy: 'npm install / yarn install / pnpm install, from package.json and a lockfile',
    regenerateCommand: 'npm install',
    rationale:
      "Directory name is npm/Node's own convention; contents are fully reproducible from package.json plus a lockfile.",
    staleDays: 34,
    lockfileConflict: true,
  },
  {
    id: 'env',
    dirName: 'env',
    path: '~/projects/api/ingest-service',
    sizeMB: 360,
    ecosystem: 'Python (venv, legacy naming)',
    risk: 'medium',
    confidence: 0.75,
    generatedBy: 'python -m venv, populated via pip from a requirements/lock file',
    regenerateCommand: 'python -m venv env && env/bin/pip install -r requirements.txt',
    rationale:
      "'env' is a less specific convention than venv/.venv and is sometimes used for unrelated environment-variable directories, so the match is less certain.",
    staleDays: 96,
  },
  {
    id: 'next',
    dirName: '.next',
    path: '~/projects/web/marketing-site',
    sizeMB: 200,
    ecosystem: 'Next.js',
    risk: 'low',
    confidence: 0.95,
    generatedBy: 'next build / next dev, from the project’s Next.js source',
    regenerateCommand: 'next build',
    rationale:
      "Directory name is Next.js's own build-output convention; reproducible from source via the Next.js CLI.",
    staleDays: 12,
  },
];

// Phase 6 — the four factual beats of the project's evolution. Beat 1 is the
// maintainer's own words; beats 2–4 are drawn straight from CHANGELOG.md with
// no invented motivation.
export const STORY_BEATS: StoryBeat[] = [
  {
    marker: 'devclean.py',
    title: 'The script',
    body:
      '“It started as a simple script — I just wanted to get rid of dev junk without doing it by hand. A cool little Python script, basically. It grew from there into an actual utility.”',
  },
  {
    marker: 'v1.0.0',
    title: 'First PyPI release',
    body: 'Packaged and published to PyPI: scan and clean, with every deletion routed to the system trash.',
  },
  {
    marker: 'v1.0.2',
    title: 'Terminal hardening',
    body: 'Adopted click.echo across the console layer, fixing Unicode and Windows terminal handling.',
  },
  {
    marker: 'v1.1.0',
    title: 'A layer that reasons',
    body: 'Added analyze and explain, backed by the artifact-signature registry, plus --compress for archiving large artifacts before trashing them.',
  },
];
