import { useState, useEffect, useCallback, useRef } from 'react';
import { factCheckService } from '../services/factCheck';
import type { FactCheckResult, JobStatusResponse } from '../types/api';
import { JOB_POLLING } from '../utils/constants';

interface UseJobPollingOptions {
  jobId: string;
  onComplete: (result: FactCheckResult) => void;
  onError: (error: string) => void;
  interval?: number;
}

interface UseJobPollingReturn {
  status: string;
  progress: number;
  isPolling: boolean;
  stopPolling: () => void;
}

export const useJobPolling = ({
  jobId,
  onComplete,
  onError,
  interval = JOB_POLLING.interval
}: UseJobPollingOptions): UseJobPollingReturn => {
  const [status, setStatus] = useState<string>('queued');
  const [progress, setProgress] = useState<number>(0);
  const [isPolling, setIsPolling] = useState<boolean>(false);
  const [attempts, setAttempts] = useState<number>(0);
  
  const intervalRef = useRef<number | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  const stopPolling = useCallback(() => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    setIsPolling(false);
  }, []);

  const pollJobStatus = useCallback(async () => {
    if (attempts >= JOB_POLLING.maxAttempts) {
      onError('Job polling timed out');
      stopPolling();
      return;
    }

    try {
      abortControllerRef.current = new AbortController();
      const jobStatus: JobStatusResponse = await factCheckService.getJobStatus(jobId);
      
      setStatus(jobStatus.status);
      setProgress(jobStatus.progress || 0);
      setAttempts(prev => prev + 1);

      if (jobStatus.status === 'completed' && jobStatus.result) {
        onComplete(jobStatus.result);
        stopPolling();
      } else if (jobStatus.status === 'failed') {
        onError(jobStatus.error || 'Job failed');
        stopPolling();
      }
    } catch (err) {
      if (err instanceof Error && err.name === 'AbortError') {
        return; // Polling was cancelled, ignore
      }
      
      setAttempts(prev => prev + 1);
      if (attempts >= JOB_POLLING.maxAttempts - 1) {
        onError('Failed to check job status');
        stopPolling();
      }
    }
  }, [jobId, onComplete, onError, attempts, stopPolling]);

  useEffect(() => {
    if (jobId && !isPolling) {
      setIsPolling(true);
      setAttempts(0);
      
      // Start polling immediately
      pollJobStatus();
      
      // Then poll at intervals
      intervalRef.current = setInterval(pollJobStatus, interval);
    }

    return () => {
      stopPolling();
    };
  }, [jobId, interval, pollJobStatus, isPolling, stopPolling]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopPolling();
    };
  }, [stopPolling]);

  return {
    status,
    progress,
    isPolling,
    stopPolling
  };
};