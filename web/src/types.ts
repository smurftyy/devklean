export type RiskLevel = 'low' | 'medium' | 'high';

// Reclaim-safety weights, mirrored 1:1 from devklean.signatures.registry.RiskLevel.weight.
export const RISK_WEIGHT: Record<RiskLevel, number> = {
  low: 1.0,
  medium: 0.6,
  high: 0.2,
};

// A cleanable directory found in the demo workspace, carrying the same fields
// `devklean analyze`/`explain` read verbatim from the artifact-signature registry.
export interface DemoProject {
  id: string;
  dirName: string;
  path: string;
  sizeMB: number;
  ecosystem: string;
  risk: RiskLevel;
  confidence: number; // 0.0 - 1.0, maintainer-assigned
  generatedBy: string;
  regenerateCommand: string;
  rationale: string;
  staleDays: number;
  lockfileConflict?: boolean;
}

export interface Feature {
  id: string;
  command: string;
  title: string;
  description: string;
  sampleOutput: string;
}

export interface Ecosystem {
  name: string;
  artifacts: string;
  accent: string; // tailwind text color class
}

export interface StoryBeat {
  marker: string;
  title: string;
  body: string;
}
