export interface JobResponse {
  job_id: string;
  status: 'queued' | 'running' | 'completed' | 'failed';
  estimated_seconds?: number;
}

export interface JobStatusResponse {
  job_id: string;
  status: 'queued' | 'running' | 'completed' | 'failed';
  result?: FactCheckResult;
  error?: string;
  progress?: number;
}

export interface FactCheckResult {
  id: string;
  timestamp: string;
  compact: CompactResult;
  full: DetailedResult;
}

export interface CompactResult {
  claim: string;
  verdict: 'True' | 'False' | 'Unclear';
  confidence: number;
  explanation: string;
  top_sources: Source[];
}

export interface DetailedResult {
  claim: string;
  verdict: 'True' | 'False' | 'Unclear';
  confidence: number;
  detailed_explanation: string;
  reasoning_steps: string[];
  all_sources: Source[];
  contradictory_info?: string;
  limitations?: string;
}

export interface Source {
  name: string;
  url: string;
  excerpt: string;
  type: 'paper' | 'webpage' | 'news' | 'user_upload';
}

export interface UploadResponse {
  upload_id: string;
  filename: string;
  size: number;
  chunks_processed: number;
  status: string;
}

export interface ApiError {
  detail: string;
}