import React from 'react';
import styled from 'styled-components';
import { Settings } from 'lucide-react';

interface FABProps {
  onClick: () => void;
}

const StyledFAB = styled.button`
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 56px;
  height: 56px;
  background: var(--color-blue-green);
  color: white;
  border: none;
  border-radius: 50%;
  box-shadow: var(--shadow-lg);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  transition: all 0.3s ease;
  
  &:hover {
    transform: scale(1.1);
    box-shadow: var(--shadow-xl);
    background: #2a7a8a;
  }
  
  &:active {
    transform: scale(1.05);
  }
  
  &:focus-visible {
    outline: 2px solid var(--color-blue-green);
    outline-offset: 4px;
  }
  
  @media (max-width: 768px) {
    bottom: 20px;
    right: 20px;
    width: 48px;
    height: 48px;
  }
`;

export const FAB: React.FC<FABProps> = ({ onClick }) => {
  return (
    <StyledFAB onClick={onClick} aria-label="Open settings">
      <Settings size={24} />
    </StyledFAB>
  );
};