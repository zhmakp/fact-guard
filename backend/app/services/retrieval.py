from app.services.vector_store import vector_store_service
from app.models.responses import Source
from typing import List
import logging

logger = logging.getLogger(__name__)


class RetrievalService:
    async def find_relevant_sources(self, query: str, limit: int = 10) -> List[Source]:
        """Find relevant sources for a given query"""
        try:
            # Search in vector store
            search_results = await vector_store_service.similarity_search(
                query=query,
                limit=limit
            )
            
            # Convert to Source objects
            sources = []
            for result in search_results:
                # Only include results with reasonable similarity
                if result["score"] > 0.5:  # Threshold for relevance
                    source = Source(
                        name=result["source_name"],
                        url=result["source_url"] or "#",
                        excerpt=self._create_excerpt(result["text"]),
                        type=self._map_source_type(result["source_type"])
                    )
                    sources.append(source)
            
            logger.info(f"Found {len(sources)} relevant sources for query")
            return sources
            
        except Exception as e:
            logger.error(f"Error finding relevant sources: {str(e)}")
            return []
    
    def _create_excerpt(self, text: str, max_length: int = 500) -> str:
        """Create a brief excerpt from text"""
        if len(text) <= max_length:
            return text
        
        # Find a good breaking point (end of sentence)
        excerpt = text[:max_length]
        last_period = excerpt.rfind('.')
        if last_period > max_length * 0.7:  # If we found a period reasonably close
            excerpt = excerpt[:last_period + 1]
        else:
            excerpt = excerpt.rsplit(' ', 1)[0] + "..."
        
        return excerpt
    
    def _map_source_type(self, source_type: str) -> str:
        """Map internal source type to API source type"""
        mapping = {
            "user_upload": "user_upload",
            "pdf": "paper",
            "webpage": "webpage",
            "news": "news",
            "paper": "paper"
        }
        return mapping.get(source_type, "webpage")


# Global service instance
retrieval_service = RetrievalService()