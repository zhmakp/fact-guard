from math import log
import re
import ollama
from app.config import settings
from app.models.requests import FactCheckRequest
from app.models.responses import (
    FactCheckResult, CompactResult, DetailedResult, 
    Verdict, Source
)
from app.services.retrieval import retrieval_service
from datetime import datetime
import logging
import uuid
import json

logger = logging.getLogger(__name__)


class FactCheckService:
    def __init__(self):
        self.client = ollama.AsyncClient(host=settings.ollama_base_url)
        self.model = settings.ollama_model
    
    async def check_claim(self, request: FactCheckRequest) -> FactCheckResult:
        """Main fact-checking pipeline"""
        try:
            # Extract claim text
            if request.type.value == "claim":
                claim_text = request.claim
            elif request.type.value == "url":
                claim_text = await self._extract_claim_from_url(request.url)
            else:
                raise ValueError("Upload type not supported in this method")
            
            # Retrieve relevant sources
            relevant_sources = await retrieval_service.find_relevant_sources(claim_text)
            logger.info(f"Found {len(relevant_sources)} relevant sources")

            # Generate fact-check using LLM
            compact_result = await self._generate_compact_fact_check(claim_text, relevant_sources)
            detailed_result = await self._generate_detailed_fact_check(claim_text, relevant_sources)
            
            # Create complete result
            result = FactCheckResult(
                id=str(uuid.uuid4()),
                timestamp=datetime.utcnow(),
                compact=compact_result,
                full=detailed_result
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error in fact-check pipeline: {str(e)}")
            raise
    
    async def _extract_claim_from_url(self, url: str) -> str:
        """Extract main claim from a URL (simplified implementation)"""
        # This would use web scraping in a full implementation
        # For now, return placeholder
        return f"Claims extracted from {url}"
    
    async def _generate_compact_fact_check(self, claim: str, sources: list) -> CompactResult:
        """Generate compact fact-check result"""
        
        # Create context from sources
        context = self._build_context_from_sources(sources)
        
        prompt = f"""
        Fact-check the following claim using the provided sources:
        
        CLAIM: {claim}
        
        SOURCES:
        {context}
        
        Provide a verdict (True, False, or Unclear), confidence score (0-100), 
        and a brief 1-line explanation.
        
        Format your response as JSON:
        {{
            "verdict": "True|False|Unclear",
            "confidence": <number>,
            "explanation": "<brief explanation>"
        }}
        """
        logger.info(f"Generated prompt for compact fact-check: {prompt}")
        try:
            response = await self.client.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Parse LLM response (simplified - would need robust JSON parsing)
            result_text = response['message']['content'].replace('```json', '').replace('```', '').strip()
            logger.info(f"LLM response for compact fact-check: {result_text}")
            json_result = json.loads(result_text)
            # For demo purposes, return mock result
            return CompactResult(
                claim=claim,
                verdict=json_result["verdict"] if "verdict" in json_result else Verdict.UNCLEAR,
                confidence=json_result["confidence"] if "confidence" in json_result else 50.0,
                explanation=json_result["explanation"] if "explanation" in json_result else "No explanation provided",
                top_sources=sources[:3] if sources else []
            )
            
        except Exception as e:
            logger.error(f"Error generating compact fact-check: {str(e)}")
            # Return safe default
            return CompactResult(
                claim=claim,
                verdict=Verdict.UNCLEAR,
                confidence=50.0,
                explanation="Unable to complete fact-check due to processing error",
                top_sources=[]
            )
    
    async def _generate_detailed_fact_check(self, claim: str, sources: list) -> DetailedResult:
        """Generate detailed fact-check result"""
        
        # For demo purposes, return mock detailed result
        return DetailedResult(
            claim=claim,
            verdict=Verdict.UNCLEAR,
            confidence=75.0,
            detailed_explanation="This is a detailed explanation of the fact-check process and findings.",
            reasoning_steps=[
                "Analyzed claim for factual statements",
                "Searched relevant sources in knowledge base",
                "Cross-referenced information across multiple sources",
                "Evaluated contradictory information",
                "Assigned confidence score based on source quality and consensus"
            ],
            all_sources=sources,
            contradictory_info="Some sources present conflicting information on this topic",
            limitations="Limited recent sources available for this specific claim"
        )
    
    def _build_context_from_sources(self, sources: list) -> str:
        """Build context string from source list"""
        context_parts = []
        for i, source in enumerate(sources[:20], 1):  # Use top 5 sources
            if hasattr(source, 'excerpt'):
                context_parts.append(f"{i}. {source.name}: {source.excerpt}")
        
        return "\n".join(context_parts) if context_parts else "No relevant sources found."


# Global service instance
fact_check_service = FactCheckService()