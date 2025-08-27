import re
from typing import List
from app.config import settings


class TextChunker:
    def __init__(self):
        self.chunk_size = settings.chunk_size
        self.overlap = settings.chunk_overlap
    
    def chunk_text(self, text: str) -> List[str]:
        """Chunk text into overlapping segments"""
        if not text.strip():
            return []
        
        # Clean the text
        text = self._clean_text(text)
        
        # Try sentence-aware chunking first
        sentences = self._split_into_sentences(text)
        chunks = self._create_sentence_chunks(sentences)
        
        # If chunks are still too large, fall back to token-based splitting
        final_chunks = []
        for chunk in chunks:
            if len(chunk.split()) <= self.chunk_size:
                final_chunks.append(chunk)
            else:
                # Split large chunks further
                sub_chunks = self._token_based_split(chunk)
                final_chunks.extend(sub_chunks)
        
        return final_chunks
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove excessive newlines but keep paragraph breaks
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting (could be enhanced with nlp libraries)
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _create_sentence_chunks(self, sentences: List[str]) -> List[str]:
        """Create chunks from sentences with overlap"""
        chunks = []
        current_chunk = []
        current_word_count = 0
        
        for sentence in sentences:
            sentence_words = len(sentence.split())
            
            # If adding this sentence would exceed chunk size, finalize current chunk
            if current_word_count + sentence_words > self.chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                
                # Start new chunk with overlap
                overlap_words = 0
                overlap_sentences = []
                
                # Add sentences from the end for overlap
                for prev_sentence in reversed(current_chunk):
                    sentence_word_count = len(prev_sentence.split())
                    if overlap_words + sentence_word_count <= self.overlap:
                        overlap_sentences.insert(0, prev_sentence)
                        overlap_words += sentence_word_count
                    else:
                        break
                
                current_chunk = overlap_sentences
                current_word_count = overlap_words
            
            current_chunk.append(sentence)
            current_word_count += sentence_words
        
        # Add final chunk if there's content
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def _token_based_split(self, text: str) -> List[str]:
        """Fall back to simple token-based splitting for large chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunks.append(' '.join(chunk_words))
        
        return chunks


# Global chunker instance
text_chunker = TextChunker()