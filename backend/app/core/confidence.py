from typing import List, Dict, Any
from app.core.sources import source_manager


class ConfidenceScorer:
    def __init__(self):
        self.base_confidence = 0.5
        self.source_weight = 0.3
        self.consensus_weight = 0.2
        self.recency_weight = 0.1
    
    def calculate_confidence(
        self, 
        sources: List[Dict[str, Any]], 
        verdict_consensus: float,
        llm_confidence: float = 0.5
    ) -> float:
        """Calculate overall confidence score based on multiple factors"""
        
        # Start with LLM's base confidence
        confidence = llm_confidence
        
        # Source quality factor
        source_quality = self._calculate_source_quality(sources)
        confidence += source_quality * self.source_weight
        
        # Consensus factor (how much sources agree)
        confidence += verdict_consensus * self.consensus_weight
        
        # Source quantity factor (more sources = higher confidence, with diminishing returns)
        quantity_factor = min(len(sources) / 10.0, 0.1)  # Cap at 10% boost
        confidence += quantity_factor
        
        # Ensure confidence stays within bounds
        return max(0.0, min(1.0, confidence))
    
    def _calculate_source_quality(self, sources: List[Dict[str, Any]]) -> float:
        """Calculate average quality of sources"""
        if not sources:
            return 0.0
        
        total_quality = 0.0
        for source in sources:
            url = source.get("url", "")
            
            # Base quality for any source
            quality = 0.3
            
            # Trusted source bonus
            if source_manager.is_trusted_source(url):
                priority = source_manager.get_source_priority(url)
                # Higher priority (lower number) gets higher quality score
                quality += 0.4 * (5 - min(priority, 4)) / 4
            
            # Source type bonuses
            source_type = source.get("type", "webpage")
            type_bonuses = {
                "paper": 0.3,     # Academic papers get highest bonus
                "webpage": 0.1,   # Regular webpages get small bonus
                "news": 0.2,      # News sources get medium bonus
                "user_upload": 0.0  # User uploads are neutral
            }
            quality += type_bonuses.get(source_type, 0.0)
            
            total_quality += quality
        
        return min(total_quality / len(sources), 1.0)
    
    def calculate_verdict_consensus(self, verdicts: List[str]) -> float:
        """Calculate how much the sources agree on a verdict"""
        if not verdicts:
            return 0.0
        
        # Count verdicts
        verdict_counts = {}
        for verdict in verdicts:
            verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1
        
        # Calculate consensus as the proportion of the majority verdict
        max_count = max(verdict_counts.values())
        consensus = max_count / len(verdicts)
        
        return consensus
    
    def adjust_confidence_for_contradictions(
        self, 
        base_confidence: float, 
        has_contradictions: bool
    ) -> float:
        """Reduce confidence when contradictory information is found"""
        if has_contradictions:
            return base_confidence * 0.8  # 20% reduction for contradictions
        return base_confidence


# Global confidence scorer instance
confidence_scorer = ConfidenceScorer()