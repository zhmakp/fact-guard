import { useCallback, useState } from 'react';
import { UI_CONFIG } from '../utils/constants';
import type { Toast } from '../types/ui';

interface UseToastReturn {
  toasts: Toast[];
  showToast: (message: string, type: Toast['type'], duration?: number) => string;
  dismissToast: (id: string) => void;
  clearToasts: () => void;
}

export const useToast = (): UseToastReturn => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const showToast = useCallback((
    message: string, 
    type: Toast['type'], 
    duration: number = UI_CONFIG.toastDuration
  ): string => {
    const id = `toast-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    const newToast: Toast = {
      id,
      message,
      type,
      duration,
      timestamp: new Date()
    };

    setToasts(prev => [...prev, newToast]);

    // Auto-dismiss after duration
    if (duration > 0) {
      setTimeout(() => {
        dismissToast(id);
      }, duration);
    }

    return id;
  }, []);

  const dismissToast = useCallback((id: string) => {
    setToasts(prev => prev.filter(toast => toast.id !== id));
  }, []);

  const clearToasts = useCallback(() => {
    setToasts([]);
  }, []);

  return {
    toasts,
    showToast,
    dismissToast,
    clearToasts
  };
};