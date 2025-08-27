from fastapi import APIRouter, HTTPException
from app.models.responses import JobStatusResponse
from app.services.jobs import job_manager
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/job/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """Get the status of a background job"""
    try:
        job = job_manager.get_job(job_id)
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return JobStatusResponse(
            job_id=job_id,
            status=job.status,
            result=job.result,
            error=job.error,
            progress=job.progress
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching job status for {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch job status")