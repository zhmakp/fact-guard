export interface FactCheckInput {
  claim?: string;
  url?: string;
  type: 'claim' | 'url' | 'upload';
}

export interface UploadMetadata {
  source_name: string;
  source_type: 'pdf' | 'csv' | 'text';
  description?: string;
  is_trusted: boolean;
}

export interface JobProgress {
  jobId: string;
  progress: number;
  estimatedSeconds?: number;
  startedAt: Date;
}

export type Verdict = 'True' | 'False' | 'Unclear';

export interface VerdictColors {
  True: string;
  False: string;
  Unclear: string;
}

export const VERDICT_COLORS: VerdictColors = {
  True: 'var(--color-blue-green)',
  False: 'var(--color-red)',
  Unclear: 'var(--color-teal)'
};