from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.requests import UploadMetadata
from app.models.responses import UploadResponse
from app.services.document import document_service
from app.config import settings
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    source_name: str = Form(...),
    source_type: str = Form(...),
    description: str = Form(None),
    is_trusted: bool = Form(True)
):
    """Upload and process a document (PDF, CSV, etc.)"""
    try:
        # Validate file size
        if file.size and file.size > settings.max_upload_size:
            raise HTTPException(
                status_code=413, 
                detail=f"File too large. Maximum size is {settings.max_upload_size} bytes"
            )
        
        # Validate file type
        allowed_types = ["pdf", "csv", "text"]
        if source_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Allowed types: {allowed_types}"
            )
        
        # Create metadata
        metadata = UploadMetadata(
            source_name=source_name,
            source_type=source_type,
            description=description,
            is_trusted=is_trusted
        )
        
        # Generate upload ID
        upload_id = str(uuid.uuid4())
        
        # Process document
        result = await document_service.process_uploaded_file(
            upload_id, file, metadata
        )
        
        logger.info(f"Document uploaded and processed: {upload_id} - {file.filename}")
        
        return UploadResponse(
            upload_id=upload_id,
            filename=file.filename or "unknown",
            size=file.size or 0,
            chunks_processed=result.get("chunks_processed", 0),
            status="completed"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process uploaded file")