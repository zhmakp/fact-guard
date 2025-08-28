from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition
from app.config import settings
from app.services.embeddings import embedding_service
from app.core.sources import source_manager
from typing import List, Dict, Any, Optional
import uuid
import logging

from app.core.chunking import text_chunker

logger = logging.getLogger(__name__)


class VectorStoreService:
    def __init__(self):
        self.client = None
        self.collection_name = settings.qdrant_collection_name
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Qdrant client and create collection if needed"""
        try:
            self.client = QdrantClient(
                host=settings.qdrant_host,
                port=settings.qdrant_port
            )
            
            # Create collection if it doesn't exist
            self._ensure_collection_exists()
            logger.info(f"Connected to Qdrant: {settings.qdrant_host}:{settings.qdrant_port}")
            
        except Exception as e:
            logger.error(f"Failed to connect to Qdrant: {str(e)}")
            raise
    
    def _ensure_collection_exists(self):
        """Ensure the collection exists with proper configuration"""
        try:
            collections = self.client.get_collections()
            collection_names = [col.name for col in collections.collections]
            
            is_new_collection = self.collection_name not in collection_names
            
            if is_new_collection:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=embedding_service.get_embedding_dimension(),
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {self.collection_name}")
                
                # Seed default sources for new collection
                import asyncio
                asyncio.create_task(self._seed_default_sources())
            
        except Exception as e:
            logger.error(f"Error ensuring collection exists: {str(e)}")
            raise
    
    async def store_document_chunks(self, chunks: List[Dict[str, Any]]) -> List[str]:
        """Store document chunks with embeddings"""
        try:
            if not chunks:
                return []
            
            # Generate embeddings for all chunks
            texts = [chunk["text"] for chunk in chunks]
            embeddings = await embedding_service.embed_texts(texts)
            
            # Prepare points for insertion
            points = []
            point_ids = []
            
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                point_id = str(uuid.uuid4())
                point_ids.append(point_id)
                
                points.append(PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "text": chunk["text"],
                        "source_name": chunk["source_name"],
                        "source_url": chunk.get("source_url", ""),
                        "source_type": chunk["source_type"],
                        "page": chunk.get("page", 0),
                        "chunk_index": chunk.get("chunk_index", i)
                    }
                ))
            
            # Insert points into collection
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            
            logger.info(f"Stored {len(points)} chunks in vector store")
            return point_ids
            
        except Exception as e:
            logger.error(f"Error storing document chunks: {str(e)}")
            raise
    
    async def similarity_search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for similar documents using vector similarity"""
        try:
            # Generate embedding for query
            query_embedding = await embedding_service.embed_single_text(query)
            
            # Search in Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                with_payload=True
            )
            
            # Format results
            results = []
            for result in search_results:
                results.append({
                    "id": result.id,
                    "score": result.score,
                    "text": result.payload.get("text", ""),
                    "source_name": result.payload.get("source_name", ""),
                    "source_url": result.payload.get("source_url", ""),
                    "source_type": result.payload.get("source_type", ""),
                    "page": result.payload.get("page", 0)
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error in similarity search: {str(e)}")
            raise
    
    async def get_all_sources(self) -> List[Dict[str, Any]]:
        """Get all unique sources in the collection"""
        try:
            # This is a simplified implementation
            # In a real system, you'd want to aggregate by source
            search_results = self.client.scroll(
                collection_name=self.collection_name,
                limit=1000,
                with_payload=True
            )[0]  # Get the points, ignore next_page_offset
            
            # Group by source
            sources = {}
            for point in search_results:
                source_name = point.payload.get("source_name", "Unknown")
                if source_name not in sources:
                    sources[source_name] = {
                        "source_name": source_name,
                        "source_url": point.payload.get("source_url", ""),
                        "source_type": point.payload.get("source_type", ""),
                        "chunk_count": 0
                    }
                sources[source_name]["chunk_count"] += 1
            
            return list(sources.values())
            
        except Exception as e:
            logger.error(f"Error fetching all sources: {str(e)}")
            return []
    
    async def store_web_source(self, source_id: str, web_source: Dict[str, Any]) -> str:
        """Store a web source (metadata only, no content chunks)"""
        try:
            # Generate embedding for the source name/description
            text = web_source["text"]
            chunks = text_chunker.chunk_text(text);
            embeddings = await embedding_service.embed_texts(chunks)
            
            # Create point for web source
            points = [PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "text": chunk,
                    "source_name": web_source["source_name"],
                    "source_url": web_source["source_url"],
                    "source_type": web_source["source_type"],
                    "page": web_source.get("page", 0),
                    "chunk_index": web_source.get("chunk_index", 0),
                    "is_web_source": True
                }
            ) for (chunk, embedding) in zip(chunks, embeddings)]
            
            # Insert point into collection
            result = self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )
            
            logger.info(f"Stored web source: {web_source['source_name']}")
            logger.info(f"Upsert result: {result}")
            return source_id
            
        except Exception as e:
            logger.error(f"Error storing web source: {str(e)}")
            raise

    async def delete_source(self, source_id: str) -> bool:
        """Delete all chunks from a specific source"""
        try:
            # Delete points by source filter
            self.client.delete(
                collection_name=self.collection_name,
                points_selector=Filter(
                    must=[
                        FieldCondition(
                            key="source_name",
                            match={"value": source_id}
                        )
                    ]
                )
            )
            
            logger.info(f"Deleted source: {source_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting source {source_id}: {str(e)}")
            return False

    async def _seed_default_sources(self):
        """Seed default trusted sources into the vector store"""
        try:
            logger.info("Seeding default sources into vector store...")
            
            # Get default sources from SourceManager
            default_sources = source_manager.trusted_sources
            
            for source in default_sources:
                source_id = str(uuid.uuid4())
                web_source = {
                    "text": f"Default trusted source: {source.name}",
                    "source_name": source.name,
                    "source_url": f"https://{source.base_url}",
                    "source_type": source.source_type,
                    "page": 0,
                    "chunk_index": 0
                }
                
                await self.store_web_source(source_id, web_source)
            
            logger.info(f"Seeded {len(default_sources)} default sources")
            
        except Exception as e:
            logger.error(f"Error seeding default sources: {str(e)}")


# Global service instance
vector_store_service = VectorStoreService()