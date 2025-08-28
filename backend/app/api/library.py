from fastapi import APIRouter, HTTPException
from typing import List
from app.models.requests import WhitelistSourceRequest
from app.models.responses import UploadResponse
from app.services.vector_store import vector_store_service
from app.utils.web import web_scraper
import logging
import uuid

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/library", response_model=List[dict])
async def get_library():
    """Get all uploaded documents and sources in the library"""
    try:
        sources = await vector_store_service.get_all_sources()
        return sources
        
    except Exception as e:
        logger.error(f"Error fetching library: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch library")


@router.post("/library")
async def add_web_source(request: WhitelistSourceRequest):
    """Add a web source to the library"""
    try:
        source_id = str(uuid.uuid4())
        
        # Create a web source entry (no actual content, just metadata)
        web_source = {
            "text": (await web_scraper.extract_text_from_url(request.source_url))["content"],
            "source_name": request.source_name,
            "source_url": request.source_url,
            "source_type": request.source_type,
            "page": 0,
            "chunk_index": 0
        }
        
        # Store the web source
        await vector_store_service.store_web_source(source_id, web_source)
        
        return {
            "source_id": source_id,
            "source_name": request.source_name,
            "source_url": request.source_url,
            "source_type": request.source_type,
            "message": "Web source added successfully"
        }
        
    except Exception as e:
        logger.error(f"Error adding web source: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to add web source")


@router.delete("/library/{source_id}")
async def delete_source(source_id: str):
    """Delete a source from the library"""
    try:
        success = await vector_store_service.delete_source(source_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Source not found")
        
        return {"message": "Source deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting source {source_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete source")