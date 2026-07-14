export interface SimulatedProject {
  id: string;
  name: string;
  type: 'node' | 'rust' | 'python' | 'go' | 'all';
  path: string;
  artifactSize: number; // in MB
  artifactName: 'node_modules' | 'target' | '.venv' | 'pkg/mod' | 'dist';
  filesCount: number;
}

export interface TerminalLine {
  id: string;
  type: 'input' | 'output' | 'success' | 'warning' | 'info' | 'progress';
  text: string;
  timestamp?: string;
}

export interface CommandStep {
  name: string;
  command: string;
  description: string;
  badge: string;
}
