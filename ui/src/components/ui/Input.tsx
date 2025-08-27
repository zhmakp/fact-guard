import React from 'react';
import styled from 'styled-components';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
}

const InputContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 4px;
`;

const Label = styled.label`
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
`;

const StyledInput = styled.input<{ $hasError: boolean }>`
  width: 100%;
  padding: 12px 16px;
  border: 1px solid ${props => props.$hasError ? 'var(--color-red)' : 'var(--color-gray-200)'};
  border-radius: 8px;
  font-size: 16px;
  background: var(--color-white);
  color: var(--color-text-primary);
  transition: all 0.2s ease;
  
  &::placeholder {
    color: var(--color-neutral);
  }
  
  &:focus {
    outline: none;
    border-color: ${props => props.$hasError ? 'var(--color-red)' : 'var(--color-blue-green)'};
    box-shadow: 0 0 0 3px ${props => props.$hasError ? 'rgba(188, 81, 72, 0.1)' : 'var(--color-focus)'};
  }
  
  &:disabled {
    background: var(--color-gray-50);
    color: var(--color-neutral);
    cursor: not-allowed;
  }
`;

const ErrorText = styled.span`
  font-size: 12px;
  color: var(--color-red);
  margin-top: 4px;
`;

const HintText = styled.span`
  font-size: 12px;
  color: var(--color-neutral);
  margin-top: 4px;
`;

export const Input: React.FC<InputProps> = ({
  label,
  error,
  hint,
  id,
  ...props
}) => {
  const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;
  
  return (
    <InputContainer>
      {label && <Label htmlFor={inputId}>{label}</Label>}
      <StyledInput
        id={inputId}
        $hasError={!!error}
        {...props}
      />
      {error && <ErrorText>{error}</ErrorText>}
      {hint && !error && <HintText>{hint}</HintText>}
    </InputContainer>
  );
};