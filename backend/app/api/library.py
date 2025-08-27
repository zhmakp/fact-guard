from fastapi import APIRouter, HTTPException
from typing import List
from app.models.responses import UploadResponse
from app.services.vector_store import vector_store_service
import logging

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