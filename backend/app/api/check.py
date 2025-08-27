from fastapi import APIRouter, HTTPException, BackgroundTasks
from app.models.requests import FactCheckRequest
from app.models.responses import JobResponse, JobStatus
from app.services.jobs import job_manager
from app.services.llm import fact_check_service
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


async def process_fact_check(job_id: str, request: FactCheckRequest):
    """Background task to process fact-check request"""
    try:
        # Update job status to running
        job_manager.update_job(job_id, status=JobStatus.RUNNING, progress=10)
        
        # Process the fact-check
        result = await fact_check_service.check_claim(request)
        
        # Complete the job
        job_manager.complete_job(job_id, result)
        logger.info(f"Fact-check job {job_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Fact-check job {job_id} failed: {str(e)}")
        job_manager.fail_job(job_id, str(e))


@router.post("/check", response_model=JobResponse)
async def submit_fact_check(
    request: FactCheckRequest, 
    background_tasks: BackgroundTasks
):
    """Submit a fact-check request and return a job ID for tracking"""
    try:
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Create job entry
        job_manager.create_job(job_id, estimated_seconds=30)
        
        # Schedule background processing
        background_tasks.add_task(process_fact_check, job_id, request)
        
        logger.info(f"Fact-check job {job_id} queued for request: {request.type}")
        
        return JobResponse(
            job_id=job_id,
            status=JobStatus.QUEUED,
            estimated_seconds=30
        )
        
    except Exception as e:
        logger.error(f"Error submitting fact-check: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to submit fact-check request")