export interface Toast {
  id: string;
  message: string;
  type: 'success' | 'error' | 'info';
  duration?: number;
  timestamp: Date;
}

export interface UIState {
  drawerOpen: boolean;
  toasts: Toast[];
  theme: 'light';
}

export interface UserSettings {
  trustedSources: string[];
  blockedSources: string[];
  minimumConfidence: number;
  autoDetectClaimType: boolean;
}

export type CardAction = 'save' | 'export' | 'share' | 'details';

export interface ButtonVariant {
  primary: string;
  secondary: string;
  danger: string;
  ghost: string;
}

export interface ButtonSize {
  sm: string;
  md: string;
  lg: string;
}