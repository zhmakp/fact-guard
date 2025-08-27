import { useState, useCallback, useEffect, useRef } from 'react';
import { factCheckService } from '../services/factCheck';
import type { FactCheckResult } from '../types/api';
import type { FactCheckInput } from '../types/factCheck';
import useInterval from './useInterval';

interface UseFactCheckReturn {
  submitCheck: (input: FactCheckInput) => Promise<string>;
  results: FactCheckResult[];
  error: string | null;
  isLoading: boolean;
  clearError: () => void;
  addResult: (result: FactCheckResult) => void;
}

export const useFactCheck = (): UseFactCheckReturn => {
  const [results, setResults] = useState<FactCheckResult[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const [attemptCount, setAttemptCount] = useState<number | null>(0);

  const MAX_ATTEMPTS = 10;

  const timeoutRef = useRef<number | null>(null);

  const startRetrievingJobStatus = useCallback((jobId: string) => {
    // Clear any existing timeout
    if (timeoutRef.current) {
      clearInterval(timeoutRef.current);
    }
    
    // Set new timeout
    timeoutRef.current = setInterval(() => {
      fetchJobStatus(jobId);
    }, 2000);
  }, []);

  const fetchJobStatus = useCallback(async (jobId: string) => {
    console.log('Fetching job status for jobId:', jobId);
    try {
      const status = await factCheckService.getJobStatus(jobId);

      if (attemptCount ?? 0 >= MAX_ATTEMPTS) {
        clearInterval(timeoutRef.current!);
      }

      if (status.status === 'completed' && status.result) {
        setResults(prev => [status.result!, ...prev]);
      } else if (status.status === 'failed' && status.error) {
        setError(status.error);
      } else {
        setAttemptCount((prev) => (prev ?? 0) + 1);
        return;
      }

      setIsLoading(false);
      clearInterval(timeoutRef.current!);
    } catch (error) {
      console.error('Error fetching job status:', error);
    }
  }, [attemptCount]);

  const submitCheck = async (input: FactCheckInput): Promise<string> => {
    setIsLoading(true);
    setError(null);

    try {
      const response = await factCheckService.submitCheck(input);
      startRetrievingJobStatus(response.job_id);
      return response.job_id;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to submit fact-check';
      setError(errorMessage);
      throw new Error(errorMessage);
    }
  };

  const addResult = useCallback((result: FactCheckResult) => {
    setResults(prev => [result, ...prev]);
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    submitCheck,
    results,
    error,
    isLoading,
    clearError,
    addResult
  };
};