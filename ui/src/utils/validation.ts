import { UPLOAD_LIMITS } from './constants';

export const validateClaim = (claim: string): { isValid: boolean; error?: string } => {
  if (!claim || claim.trim().length === 0) {
    return { isValid: false, error: 'Please enter a claim to fact-check' };
  }

  if (claim.trim().length < 10) {
    return { isValid: false, error: 'Claim is too short. Please provide more details.' };
  }

  if (claim.length > 1000) {
    return { isValid: false, error: 'Claim is too long. Please keep it under 1000 characters.' };
  }

  return { isValid: true };
};

export const validateUrl = (url: string): { isValid: boolean; error?: string } => {
  if (!url || url.trim().length === 0) {
    return { isValid: false, error: 'Please enter a URL' };
  }

  try {
    const urlObj = new URL(url);
    if (!['http:', 'https:'].includes(urlObj.protocol)) {
      return { isValid: false, error: 'URL must start with http:// or https://' };
    }
    return { isValid: true };
  } catch {
    return { isValid: false, error: 'Please enter a valid URL' };
  }
};

export const validateFile = (file: File): { isValid: boolean; error?: string } => {
  if (file.size > UPLOAD_LIMITS.maxFileSize) {
    const maxSizeMB = UPLOAD_LIMITS.maxFileSize / (1024 * 1024);
    return { 
      isValid: false, 
      error: `File is too large. Maximum size is ${maxSizeMB}MB` 
    };
  }

  const extension = file.name.split('.').pop()?.toLowerCase();
  if (!extension || !UPLOAD_LIMITS.allowedTypes.includes(extension)) {
    return { 
      isValid: false, 
      error: `File type not supported. Allowed types: ${UPLOAD_LIMITS.allowedTypes.join(', ')}` 
    };
  }

  return { isValid: true };
};

export const detectInputType = (input: string): 'claim' | 'url' => {
  const trimmed = input.trim();
  
  // Check if it looks like a URL
  try {
    new URL(trimmed);
    return 'url';
  } catch {
    // Not a valid URL, treat as claim
    return 'claim';
  }
};

export const sanitizeInput = (input: string): string => {
  return input.trim().replace(/\s+/g, ' ');
};