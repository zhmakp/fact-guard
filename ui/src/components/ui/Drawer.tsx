import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import { X, Plus, Trash2, Globe, FileText, Newspaper, BookOpen } from 'lucide-react';
import { Button } from './Button';
import { Input } from './Input';
import { libraryService, type LibrarySource } from '../../services/library';

interface DrawerProps {
  isOpen: boolean;
  onClose: () => void;
}

const Overlay = styled.div<{ $isOpen: boolean }>`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
  opacity: ${props => props.$isOpen ? 1 : 0};
  visibility: ${props => props.$isOpen ? 'visible' : 'hidden'};
  transition: all 0.3s ease;
`;

const DrawerContainer = styled.div<{ $isOpen: boolean }>`
  position: fixed;
  top: 0;
  right: 0;
  width: 400px;
  height: 100vh;
  background: var(--color-bg-primary);
  box-shadow: var(--shadow-xl);
  z-index: 1001;
  transform: translateX(${props => props.$isOpen ? '0' : '100%'});
  transition: transform 0.3s ease;
  display: flex;
  flex-direction: column;

  @media (max-width: 768px) {
    width: 100vw;
  }
`;

const Header = styled.div`
  display: flex;
  align-items: center;
  justify-content: between;
  padding: 24px;
  border-bottom: 1px solid var(--color-border);
  gap: 16px;
`;

const Title = styled.h2`
  margin: 0;
  flex: 1;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-primary);
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 8px;
  border-radius: 4px;
  transition: all 0.2s ease;

  &:hover {
    background: var(--color-bg-secondary);
    color: var(--color-text-primary);
  }
`;

const Content = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 32px;
`;

const Section = styled.div`
  display: flex;
  flex-direction: column;
  gap: 16px;
`;

const SectionTitle = styled.h3`
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-text-primary);
`;

const AddSourceForm = styled.div`
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  background: var(--color-bg-secondary);
  border-radius: 8px;
  border: 1px solid var(--color-border);
`;

const FormRow = styled.div`
  display: flex;
  gap: 8px;
  align-items: flex-end;
`;

const SelectWrapper = styled.div`
  flex: 1;
`;

const Select = styled.select`
  width: 100%;
  padding: 12px;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  background: var(--color-bg-primary);
  color: var(--color-text-primary);
  font-size: 0.875rem;
  transition: border-color 0.2s ease;

  &:focus {
    outline: none;
    border-color: var(--color-blue-green);
  }
`;

const SourceList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 300px;
  overflow-y: auto;
`;

const SourceItem = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: var(--color-bg-secondary);
  border-radius: 6px;
  border: 1px solid var(--color-border);
`;

const SourceIcon = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  color: var(--color-blue-green);
`;

const SourceInfo = styled.div`
  flex: 1;
  min-width: 0;
`;

const SourceName = styled.div`
  font-weight: 500;
  color: var(--color-text-primary);
  font-size: 0.875rem;
`;

const SourceUrl = styled.div`
  font-size: 0.75rem;
  color: var(--color-text-secondary);
  word-break: break-all;
`;

const DeleteButton = styled.button`
  background: none;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s ease;

  &:hover {
    background: var(--color-red);
    color: white;
  }
`;

const getSourceIcon = (type: string) => {
  switch (type) {
    case 'webpage': return <Globe size={16} />;
    case 'news': return <Newspaper size={16} />;
    case 'paper': return <BookOpen size={16} />;
    default: return <FileText size={16} />;
  }
};

export const Drawer: React.FC<DrawerProps> = ({ isOpen, onClose }) => {
  const [sources, setSources] = useState<LibrarySource[]>([]);
  const [loading, setLoading] = useState(false);
  const [newSource, setNewSource] = useState({
    name: '',
    url: '',
    type: 'webpage'
  });

  useEffect(() => {
    if (isOpen) {
      loadSources();
    }
  }, [isOpen]);

  const loadSources = async () => {
    setLoading(true);
    try {
      const data = await libraryService.getSources();
      setSources(data);
    } catch (error) {
      console.error('Failed to load sources:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddSource = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!newSource.name.trim() || !newSource.url.trim()) {
      return;
    }

    try {
      await libraryService.addSource({
        source_name: newSource.name,
        source_url: newSource.url,
        source_type: newSource.type as 'paper' | 'webpage' | 'news' | 'user_upload'
      });
      
      setNewSource({ name: '', url: '', type: 'webpage' });
      await loadSources();
    } catch (error) {
      console.error('Failed to add source:', error);
    }
  };

  const handleDeleteSource = async (sourceName: string) => {
    try {
      await libraryService.deleteSource(sourceName);
      await loadSources();
    } catch (error) {
      console.error('Failed to delete source:', error);
    }
  };

  return (
    <>
      <Overlay $isOpen={isOpen} onClick={onClose} />
      <DrawerContainer $isOpen={isOpen}>
        <Header>
          <Title>Settings</Title>
          <CloseButton onClick={onClose}>
            <X size={20} />
          </CloseButton>
        </Header>
        
        <Content>
          <Section>
            <SectionTitle>Add Trusted Source</SectionTitle>
            <AddSourceForm>
              <Input
                placeholder="Source name (e.g., Reuters)"
                value={newSource.name}
                onChange={(e) => setNewSource(prev => ({ ...prev, name: e.target.value }))}
              />
              <Input
                placeholder="Source URL (e.g., https://reuters.com)"
                value={newSource.url}
                onChange={(e) => setNewSource(prev => ({ ...prev, url: e.target.value }))}
              />
              <FormRow>
                <SelectWrapper>
                  <Select
                    value={newSource.type}
                    onChange={(e) => setNewSource(prev => ({ ...prev, type: e.target.value }))}
                  >
                    <option value="webpage">Website</option>
                    <option value="news">News Source</option>
                    <option value="paper">Academic Paper</option>
                  </Select>
                </SelectWrapper>
                <Button onClick={handleAddSource} disabled={!newSource.name.trim() || !newSource.url.trim()}>
                  <Plus size={16} />
                  Add
                </Button>
              </FormRow>
            </AddSourceForm>
          </Section>

          <Section>
            <SectionTitle>Trusted Sources ({sources.length})</SectionTitle>
            {loading ? (
              <div>Loading sources...</div>
            ) : (
              <SourceList>
                {sources.map((source, index) => (
                  <SourceItem key={`${source.source_name}-${index}`}>
                    <SourceIcon>
                      {getSourceIcon(source.source_type)}
                    </SourceIcon>
                    <SourceInfo>
                      <SourceName>{source.source_name}</SourceName>
                      <SourceUrl>{source.source_url}</SourceUrl>
                    </SourceInfo>
                    <DeleteButton
                      onClick={() => handleDeleteSource(source.source_name)}
                      title="Remove source"
                    >
                      <Trash2 size={16} />
                    </DeleteButton>
                  </SourceItem>
                ))}
              </SourceList>
            )}
          </Section>
        </Content>
      </DrawerContainer>
    </>
  );
};