import React from 'react';
import styled, { keyframes } from 'styled-components';

interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  color?: string;
  className?: string;
}

const spin = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

const StyledSpinner = styled.div<{ $size: string; $color: string }>`
  ${props => {
    switch (props.$size) {
      case 'sm':
        return 'width: 16px; height: 16px; border-width: 2px;';
      case 'lg':
        return 'width: 32px; height: 32px; border-width: 3px;';
      default:
        return 'width: 24px; height: 24px; border-width: 2px;';
    }
  }}
  
  border: solid ${props => props.$color};
  border-top-color: transparent;
  border-radius: 50%;
  animation: ${spin} 1s linear infinite;
`;

export const Spinner: React.FC<SpinnerProps> = ({
  size = 'md',
  color = 'var(--color-blue-green)',
  className
}) => {
  return (
    <StyledSpinner
      $size={size}
      $color={color}
      className={className}
    />
  );
};