import { useState, useCallback } from 'react';
import { uploadService } from '../services/upload';
import type { UploadMetadata } from '../types/factCheck';
import { validateFile } from '../utils/validation';

interface UseUploadReturn {
  upload: (file: File, metadata: UploadMetadata) => Promise<string>;
  progress: number;
  isUploading: boolean;
  error: string | null;
  clearError: () => void;
}

export const useUpload = (): UseUploadReturn => {
  const [progress, setProgress] = useState<number>(0);
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const upload = useCallback(async (file: File, metadata: UploadMetadata): Promise<string> => {
    // Validate file first
    const validation = validateFile(file);
    if (!validation.isValid) {
      setError(validation.error || 'Invalid file');
      throw new Error(validation.error);
    }

    setIsUploading(true);
    setProgress(0);
    setError(null);

    try {
      // Simulate upload progress (in a real implementation, this would track actual upload progress)
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          const next = prev + Math.random() * 30;
          return next > 90 ? 90 : next;
        });
      }, 200);

      const response = await uploadService.uploadFile(file, metadata);
      
      clearInterval(progressInterval);
      setProgress(100);
      
      return response.upload_id;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Upload failed';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setIsUploading(false);
      // Reset progress after a short delay
      setTimeout(() => setProgress(0), 1000);
    }
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    upload,
    progress,
    isUploading,
    error,
    clearError
  };
};