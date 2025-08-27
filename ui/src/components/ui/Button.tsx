import React from 'react';
import styled from 'styled-components';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  children: React.ReactNode;
}

const StyledButton = styled.button<{ $variant: string; $size: string; $isLoading: boolean }>`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.2s ease;
  cursor: ${props => props.disabled || props.$isLoading ? 'not-allowed' : 'pointer'};
  opacity: ${props => props.disabled || props.$isLoading ? 0.6 : 1};
  position: relative;
  
  /* Size variants */
  ${props => {
    switch (props.$size) {
      case 'sm':
        return 'padding: 6px 12px; font-size: 14px; height: 32px;';
      case 'lg':
        return 'padding: 16px 24px; font-size: 16px; height: 48px;';
      default:
        return 'padding: 12px 20px; font-size: 14px; height: 40px;';
    }
  }}
  
  /* Color variants */
  ${props => {
    switch (props.$variant) {
      case 'primary':
        return `
          background: var(--color-blue-green);
          color: white;
          border: none;
          
          &:hover:not(:disabled) {
            background: #2a7a8a;
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
          }
          
          &:active:not(:disabled) {
            transform: translateY(0);
          }
        `;
      case 'secondary':
        return `
          background: var(--color-white);
          color: var(--color-text-primary);
          border: 1px solid var(--color-gray-200);
          
          &:hover:not(:disabled) {
            border-color: var(--color-blue-green);
            color: var(--color-blue-green);
            box-shadow: var(--shadow-sm);
          }
        `;
      case 'danger':
        return `
          background: var(--color-red);
          color: white;
          border: none;
          
          &:hover:not(:disabled) {
            background: #a04440;
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
          }
        `;
      case 'ghost':
        return `
          background: transparent;
          color: var(--color-text-secondary);
          border: none;
          
          &:hover:not(:disabled) {
            background: var(--color-gray-50);
            color: var(--color-text-primary);
          }
        `;
      default:
        return '';
    }
  }}
  
  &:focus-visible {
    outline: 2px solid var(--color-blue-green);
    outline-offset: 2px;
  }
`;

const LoadingSpinner = styled.div`
  width: 16px;
  height: 16px;
  border: 2px solid currentColor;
  border-radius: 50%;
  border-top-color: transparent;
  animation: spin 1s linear infinite;
`;

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  disabled,
  children,
  ...props
}) => {
  return (
    <StyledButton
      $variant={variant}
      $size={size}
      $isLoading={isLoading}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading && <LoadingSpinner />}
      {children}
    </StyledButton>
  );
};