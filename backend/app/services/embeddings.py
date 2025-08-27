from fastembed import TextEmbedding
from typing import List
import numpy as np
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self.model_name = model_name
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the embedding model"""
        try:
            self.model = TextEmbedding(model_name=self.model_name)
            logger.info(f"Initialized embedding model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize embedding model: {str(e)}")
            raise
    
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        try:
            if not self.model:
                self._initialize_model()
            
            # Generate embeddings
            embeddings = list(self.model.embed(texts))
            
            # Convert to list of lists
            return [embedding.tolist() for embedding in embeddings]
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
    
    async def embed_single_text(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        embeddings = await self.embed_texts([text])
        return embeddings[0]
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings from this model"""
        # BAAI/bge-small-en-v1.5 produces 384-dimensional embeddings
        return 384
    
    @staticmethod
    def cosine_similarity(embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings"""
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        dot_product = np.dot(vec1, vec2)
        magnitude1 = np.linalg.norm(vec1)
        magnitude2 = np.linalg.norm(vec2)
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)


# Global service instance
embedding_service = EmbeddingService()