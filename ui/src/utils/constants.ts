export const APP_CONFIG = {
  name: 'Fact Guard',
  version: '1.0.0',
  description: 'Local-first fact-checking assistant'
};

export const API_CONFIG = {
  baseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000,
  maxRetries: 3
};

export const JOB_POLLING = {
  interval: 2000, // 2 seconds
  maxAttempts: 150 // 5 minutes max
};

export const UPLOAD_LIMITS = {
  maxFileSize: 10 * 1024 * 1024, // 10MB
  allowedTypes: ['pdf', 'csv', 'txt'],
  maxFiles: 10
};

export const UI_CONFIG = {
  toastDuration: 4000,
  cardAnimationDuration: 300,
  debounceDelay: 300
};

export const VERDICT_CONFIG = {
  colors: {
    True: '#3090A1',
    False: '#BC5148',
    Unclear: '#7BCECC'
  },
  thresholds: {
    high: 80,
    medium: 60,
    low: 40
  }
};

export const MICROCOPY = {
  inputPlaceholder: "Enter a claim to fact-check or paste a URL...",
  uploadPrompt: "or upload a document",
  checkingClaim: "Checking your claim...",
  processingUpload: "Processing your document...",
  noResults: "No results found",
  tryAgain: "Try a different claim or check your connection"
};