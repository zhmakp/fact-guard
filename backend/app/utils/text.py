import re
import unicodedata
from typing import List, Optional


def clean_text(text: str) -> str:
    """Clean and normalize text content"""
    if not text:
        return ""
    
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Clean up common encoding issues
    text = text.replace('\xa0', ' ')  # Non-breaking space
    text = text.replace('\u2019', "'")  # Smart apostrophe
    text = text.replace('\u201c', '"')  # Smart quote left
    text = text.replace('\u201d', '"')  # Smart quote right
    
    return text.strip()


def extract_sentences(text: str) -> List[str]:
    """Extract sentences from text"""
    # Simple sentence boundary detection
    sentences = re.split(r'[.!?]+\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to maximum length with suffix"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def extract_key_phrases(text: str, max_phrases: int = 10) -> List[str]:
    """Extract key phrases from text (simple implementation)"""
    # Remove common stop words and extract meaningful phrases
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
        'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
        'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
    }
    
    # Extract potential phrases (2-4 words)
    words = re.findall(r'\b\w+\b', text.lower())
    phrases = []
    
    for i in range(len(words) - 1):
        # 2-word phrases
        if words[i] not in stop_words and words[i+1] not in stop_words:
            phrases.append(f"{words[i]} {words[i+1]}")
        
        # 3-word phrases
        if i < len(words) - 2 and words[i] not in stop_words:
            phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
            if not any(word in stop_words for word in [words[i+1], words[i+2]]):
                phrases.append(phrase)
    
    # Remove duplicates and return top phrases
    unique_phrases = list(set(phrases))
    return unique_phrases[:max_phrases]


def detect_claim_type(text: str) -> str:
    """Detect the type of claim from text"""
    text_lower = text.lower()
    
    # Health-related keywords
    health_keywords = [
        'health', 'disease', 'medicine', 'treatment', 'vaccine', 'virus',
        'bacteria', 'drug', 'therapy', 'diagnosis', 'symptom', 'medical'
    ]
    
    # Political keywords
    political_keywords = [
        'government', 'policy', 'election', 'vote', 'politician', 'law',
        'congress', 'senate', 'president', 'minister', 'party'
    ]
    
    # Scientific keywords
    science_keywords = [
        'research', 'study', 'experiment', 'data', 'evidence', 'theory',
        'hypothesis', 'scientific', 'analysis', 'findings'
    ]
    
    if any(keyword in text_lower for keyword in health_keywords):
        return "health"
    elif any(keyword in text_lower for keyword in political_keywords):
        return "political"
    elif any(keyword in text_lower for keyword in science_keywords):
        return "scientific"
    else:
        return "general"


def is_valid_claim(text: str) -> bool:
    """Check if text appears to be a valid factual claim"""
    if not text or len(text.strip()) < 10:
        return False
    
    # Check for basic sentence structure
    if not re.search(r'[.!?]', text):
        return False
    
    # Must contain some meaningful words (not just numbers/symbols)
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    if len(words) < 3:
        return False
    
    return True