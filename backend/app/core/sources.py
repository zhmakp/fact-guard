from typing import List, Dict
from dataclasses import dataclass


@dataclass
class TrustedSource:
    name: str
    base_url: str
    source_type: str
    priority: int  # Lower number = higher priority


class SourceManager:
    def __init__(self):
        self.trusted_sources = self._initialize_default_sources()
        self.user_blocked_sources = set()
        self.user_trusted_sources = set()
    
    def _initialize_default_sources(self) -> List[TrustedSource]:
        """Initialize default trusted sources by category"""
        return [
            # Health Sources (Priority 1)
            TrustedSource("PubMed", "pubmed.ncbi.nlm.nih.gov", "paper", 1),
            TrustedSource("WHO", "who.int", "webpage", 1),
            TrustedSource("CDC", "cdc.gov", "webpage", 1),
            TrustedSource("NHS", "nhs.uk", "webpage", 1),
            TrustedSource("Cochrane", "cochranelibrary.com", "paper", 1),
            
            # Fact-checking Sources (Priority 2)
            TrustedSource("Snopes", "snopes.com", "webpage", 2),
            TrustedSource("PolitiFact", "politifact.com", "webpage", 2),
            TrustedSource("FactCheck.org", "factcheck.org", "webpage", 2),
            
            # News Sources (Priority 3)
            TrustedSource("Reuters", "reuters.com", "news", 3),
            TrustedSource("AP News", "apnews.com", "news", 3),
            TrustedSource("BBC", "bbc.com", "news", 3),
            
            # Academic Sources (Priority 4)
            TrustedSource("arXiv", "arxiv.org", "paper", 4),
            TrustedSource("Google Scholar", "scholar.google.com", "paper", 4),
            TrustedSource("bioRxiv", "biorxiv.org", "paper", 4),
            TrustedSource("medRxiv", "medrxiv.org", "paper", 4),
        ]
    
    def is_trusted_source(self, url: str) -> bool:
        """Check if a URL is from a trusted source"""
        # Check user-blocked sources first
        if any(blocked in url for blocked in self.user_blocked_sources):
            return False
        
        # Check user-trusted sources
        if any(trusted in url for trusted in self.user_trusted_sources):
            return True
        
        # Check default trusted sources
        return any(source.base_url in url for source in self.trusted_sources)
    
    def get_source_priority(self, url: str) -> int:
        """Get priority of a source (lower = higher priority)"""
        for source in self.trusted_sources:
            if source.base_url in url:
                return source.priority
        return 999  # Unknown sources get lowest priority
    
    def add_user_trusted_source(self, url: str):
        """Add a user-defined trusted source"""
        self.user_trusted_sources.add(url)
    
    def add_user_blocked_source(self, url: str):
        """Add a user-defined blocked source"""
        self.user_blocked_sources.add(url)
    
    def get_trusted_sources_by_category(self) -> Dict[str, List[TrustedSource]]:
        """Get trusted sources grouped by type"""
        categories = {}
        for source in self.trusted_sources:
            if source.source_type not in categories:
                categories[source.source_type] = []
            categories[source.source_type].append(source)
        return categories


# Global source manager instance
source_manager = SourceManager()