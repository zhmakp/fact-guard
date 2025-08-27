from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from app.models.responses import JobStatus, FactCheckResult
import threading


@dataclass
class Job:
    job_id: str
    status: JobStatus
    created_at: datetime
    estimated_completion: Optional[datetime] = None
    progress: Optional[int] = None
    result: Optional[FactCheckResult] = None
    error: Optional[str] = None


class JobManager:
    def __init__(self):
        self._jobs: Dict[str, Job] = {}
        self._lock = threading.Lock()
    
    def create_job(self, job_id: str, estimated_seconds: Optional[int] = None) -> Job:
        """Create a new job entry"""
        with self._lock:
            estimated_completion = None
            if estimated_seconds:
                estimated_completion = datetime.utcnow() + timedelta(seconds=estimated_seconds)
            
            job = Job(
                job_id=job_id,
                status=JobStatus.QUEUED,
                created_at=datetime.utcnow(),
                estimated_completion=estimated_completion,
                progress=0
            )
            self._jobs[job_id] = job
            return job
    
    def get_job(self, job_id: str) -> Optional[Job]:
        """Get job by ID"""
        with self._lock:
            return self._jobs.get(job_id)
    
    def update_job(self, job_id: str, status: Optional[JobStatus] = None, 
                   progress: Optional[int] = None) -> bool:
        """Update job status and/or progress"""
        with self._lock:
            if job_id not in self._jobs:
                return False
            
            job = self._jobs[job_id]
            if status:
                job.status = status
            if progress is not None:
                job.progress = progress
            
            return True
    
    def complete_job(self, job_id: str, result: FactCheckResult) -> bool:
        """Mark job as completed with result"""
        with self._lock:
            if job_id not in self._jobs:
                return False
            
            job = self._jobs[job_id]
            job.status = JobStatus.COMPLETED
            job.progress = 100
            job.result = result
            
            return True
    
    def fail_job(self, job_id: str, error: str) -> bool:
        """Mark job as failed with error message"""
        with self._lock:
            if job_id not in self._jobs:
                return False
            
            job = self._jobs[job_id]
            job.status = JobStatus.FAILED
            job.error = error
            
            return True
    
    def cleanup_old_jobs(self, max_age_hours: int = 24):
        """Clean up jobs older than max_age_hours"""
        with self._lock:
            cutoff = datetime.utcnow() - timedelta(hours=max_age_hours)
            jobs_to_remove = [
                job_id for job_id, job in self._jobs.items()
                if job.created_at < cutoff
            ]
            
            for job_id in jobs_to_remove:
                del self._jobs[job_id]


# Global job manager instance
job_manager = JobManager()