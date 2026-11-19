export type RiskLevel = 'low' | 'medium' | 'high';

// Reclaim-safety weights mirrored from devklean.signatures.registry.RiskLevel.weight.
export const RISK_WEIGHT: Record<RiskLevel, number> = {
  low: 1.0,
  medium: 0.6,
  high: 0.2,
};

export interface WorkspaceArtifact {
  id: string;
  dirName: string;
  path: string;
  sizeMB: number;
  ecosystem: string;
  risk: RiskLevel;
  confidence: number;
  generatedBy: string;
  regenerateCommand: string;
  rationale: string;
  staleDays: number;
  lockfileConflict?: boolean;
}

export interface EcosystemItem {
  id: 'nodejs' | 'python' | 'nextjs' | 'caches';
  name: string;
  artifacts: string;
}

export interface FaqItem {
  id: string;
  question: string;
  answer: string;
}
