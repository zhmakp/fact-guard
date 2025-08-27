import React from 'react';
import styled from 'styled-components';
import { Search, CheckCircle, FileText } from 'lucide-react';

const BackgroundContainer = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  overflow: hidden;
`;

const GradientBackground = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(-45deg, var(--color-cream), #f0f9ff, var(--color-cream), #fef7ed);
  background-size: 400% 400%;
  animation: gradientFlow 15s ease infinite;
`;

const FloatingIcon = styled.div<{ $delay: number; $x: string; $y: string }>`
  position: absolute;
  left: ${props => props.$x};
  top: ${props => props.$y};
  opacity: 0.1;
  color: var(--color-blue-green);
  animation: floatIcons 6s ease-in-out infinite;
  animation-delay: ${props => props.$delay}s;
  pointer-events: none;
`;

const FloatingIcons: React.FC = () => {
  const icons = [
    { Icon: Search, x: '10%', y: '20%', delay: 0 },
    { Icon: CheckCircle, x: '80%', y: '15%', delay: 1 },
    { Icon: FileText, x: '15%', y: '70%', delay: 2 },
    { Icon: Search, x: '85%', y: '60%', delay: 3 },
    { Icon: CheckCircle, x: '5%', y: '50%', delay: 4 },
    { Icon: FileText, x: '75%', y: '80%', delay: 5 },
  ];

  return (
    <>
      {icons.map(({ Icon, x, y, delay }, index) => (
        <FloatingIcon key={index} $x={x} $y={y} $delay={delay}>
          <Icon size={32} />
        </FloatingIcon>
      ))}
    </>
  );
};

export const Background: React.FC = () => {
  return (
    <BackgroundContainer>
      <GradientBackground />
      <FloatingIcons />
    </BackgroundContainer>
  );
};