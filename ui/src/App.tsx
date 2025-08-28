import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import { Background } from './components/layout/Background';
import { FAB } from './components/layout/FAB';
import { Drawer } from './components/ui/Drawer';
import { Button } from './components/ui/Button';
import { Input } from './components/ui/Input';
import { Card } from './components/ui/Card';
import { Spinner } from './components/ui/Spinner';
import { useFactCheck } from './hooks/useFactCheck';
import { useToast } from './hooks/useToast';
import { validateClaim, validateUrl, detectInputType, sanitizeInput } from './utils/validation';
import { MICROCOPY } from './utils/constants';

const AppContainer = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
`;

const MainContent = styled.main`
  width: 100%;
  max-width: 800px;
  display: flex;
  flex-direction: column;
  gap: 32px;
  animation: floatUp 0.6s ease-out;
`;

const Header = styled.header`
  text-align: center;
  margin-bottom: 24px;
`;

const Title = styled.h1`
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 8px;
  background: linear-gradient(135deg, var(--color-blue-green), var(--color-teal));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  
  @media (max-width: 768px) {
    font-size: 2.5rem;
  }
`;

const Subtitle = styled.p`
  font-size: 1.2rem;
  color: var(--color-text-secondary);
  margin-bottom: 0;
`;

const InputSection = styled(Card)`
  display: flex;
  flex-direction: column;
  gap: 16px;
`;

const InputRow = styled.div`
  display: flex;
  gap: 12px;
  align-items: flex-end;
  
  @media (max-width: 768px) {
    flex-direction: column;
    align-items: stretch;
  }
`;

const InputWrapper = styled.div`
  flex: 1;
`;

const ResultsSection = styled.div`
  display: flex;
  flex-direction: column;
  gap: 16px;
`;

const LoadingCard = styled(Card)`
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px;
`;

const ToastContainer = styled.div`
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1001;
  display: flex;
  flex-direction: column;
  gap: 8px;
`;

const Toast = styled.div<{ $type: 'success' | 'error' | 'info' }>`
  padding: 12px 16px;
  border-radius: 8px;
  color: white;
  font-weight: 500;
  animation: toastSlideIn 0.3s ease-out;
  min-width: 300px;
  
  background: ${props => {
    switch (props.$type) {
      case 'success': return 'var(--color-blue-green)';
      case 'error': return 'var(--color-red)';
      default: return 'var(--color-neutral)';
    }
  }};
`;

function App() {
  const [input, setInput] = useState('');
  const [drawerOpen, setDrawerOpen] = useState(false);
  const { submitCheck, results, error, isLoading } = useFactCheck();
  const { toasts, showToast, dismissToast } = useToast();

  useEffect(() => {
    if (error) {
      showToast(error, 'error');
    }
  }, [error, showToast]);

  useEffect(() => {
    if (results.length > 0) {
      showToast('New fact-check result available!', 'success');
    }
  }, [results, showToast]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const sanitized = sanitizeInput(input);
    if (!sanitized) {
      showToast('Please enter a claim or URL to fact-check', 'error');
      return;
    }

    const inputType = detectInputType(sanitized);

    // Validate based on type
    const validation = inputType === 'url'
      ? validateUrl(sanitized)
      : validateClaim(sanitized);

    if (!validation.isValid) {
      showToast(validation.error || 'Invalid input', 'error');
      return;
    }

    await submitCheck({
      [inputType]: sanitized,
      type: inputType
    });
    showToast('Fact-check submitted successfully!', 'success');
    setInput(''); // Clear input on successful submission
  };

  return (
    <>
      <Background />
      <AppContainer>
        <MainContent>
          <Header>
            <Title>Fact Guard</Title>
            <Subtitle>Your local-first fact-checking assistant</Subtitle>
          </Header>

          <InputSection>
            <form onSubmit={handleSubmit}>
              <InputRow>
                <InputWrapper>
                  <Input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder={MICROCOPY.inputPlaceholder}
                    disabled={isLoading}
                  />
                </InputWrapper>
                <Button
                  type="submit"
                  isLoading={isLoading}
                  disabled={!input.trim()}
                >
                  {isLoading ? 'Checking...' : 'Check Claim'}
                </Button>
              </InputRow>
            </form>
          </InputSection>

          {isLoading && (
            <LoadingCard>
              <Spinner />
              <div>
                <strong>{MICROCOPY.checkingClaim}</strong>
                <p>This may take a few moments...</p>
              </div>
            </LoadingCard>
          )}

          {results.length > 0 && (
            <ResultsSection>
              <h2>Recent Results</h2>
              {results.map((result) => (
                <Card key={result.id} hover>
                  <h3>{result.compact.claim}</h3>
                  <p><strong>Verdict:</strong> {result.compact.verdict}</p>
                  <p><strong>Confidence:</strong> {result.compact.confidence}%</p>
                  <p>{result.compact.explanation}</p>
                </Card>
              ))}
            </ResultsSection>
          )}

          {error && (
            <Card>
              <p style={{ color: 'var(--color-red)' }}>Error: {error}</p>
            </Card>
          )}
        </MainContent>

        <FAB onClick={() => setDrawerOpen(true)} />
        <Drawer isOpen={drawerOpen} onClose={() => setDrawerOpen(false)} />

        <ToastContainer>
          {toasts.map((toast) => (
            <Toast
              key={toast.id}
              $type={toast.type}
              onClick={() => dismissToast(toast.id)}
            >
              {toast.message}
            </Toast>
          ))}
        </ToastContainer>
      </AppContainer>
    </>
  );
}

export default App;
