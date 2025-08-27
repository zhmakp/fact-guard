import React from 'react';
import styled from 'styled-components';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  onClick?: () => void;
}

const StyledCard = styled.div<{ $hover: boolean; $clickable: boolean }>`
  background: var(--color-surface);
  border-radius: 12px;
  box-shadow: var(--shadow-md);
  padding: 24px;
  transition: all 0.3s ease;
  cursor: ${props => props.$clickable ? 'pointer' : 'default'};
  
  ${props => props.$hover && `
    &:hover {
      transform: translateY(-2px) scale(1.01);
      box-shadow: var(--shadow-xl);
    }
  `}
  
  @media (max-width: 768px) {
    padding: 16px;
  }
`;

export const Card: React.FC<CardProps> = ({
  children,
  className,
  hover = false,
  onClick,
  ...props
}) => {
  return (
    <StyledCard
      className={className}
      $hover={hover}
      $clickable={!!onClick}
      onClick={onClick}
      {...props}
    >
      {children}
    </StyledCard>
  );
};