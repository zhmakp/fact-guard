from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime
from enum import Enum


class Verdict(str, Enum):
    TRUE = "True"
    FALSE = "False" 
    UNCLEAR = "Unclear"


class JobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class Source(BaseModel):
    name: str = Field(..., description="Name of the source")
    url: str = Field(..., description="Source URL")
    excerpt: str = Field(..., description="Relevant excerpt (1-2 sentences)")
    type: Literal["paper", "webpage", "news", "user_upload"] = Field(..., description="Type of source")


class CompactResult(BaseModel):
    claim: str = Field(..., description="The claim being fact-checked")
    verdict: Verdict = Field(..., description="Verdict: True, False, or Unclear")
    confidence: float = Field(..., ge=0.0, le=100.0, description="Confidence score 0-100")
    explanation: str = Field(..., description="1-line summary explanation")
    top_sources: List[Source] = Field(..., max_items=3, description="Top 3 supporting sources")


class DetailedResult(BaseModel):
    claim: str
    verdict: Verdict
    confidence: float
    detailed_explanation: str = Field(..., description="Comprehensive explanation")
    reasoning_steps: List[str] = Field(..., description="Step-by-step reasoning")
    all_sources: List[Source] = Field(..., description="All relevant sources found")
    contradictory_info: Optional[str] = Field(None, description="Contradictory information found")
    limitations: Optional[str] = Field(None, description="Limitations of the fact-check")


class FactCheckResult(BaseModel):
    id: str = Field(..., description="Unique result ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the fact-check was completed")
    compact: CompactResult
    full: DetailedResult


class JobResponse(BaseModel):
    job_id: str = Field(..., description="Unique job ID")
    status: JobStatus = Field(JobStatus.QUEUED, description="Initial job status")
    estimated_seconds: Optional[int] = Field(None, description="Estimated completion time in seconds")


class JobStatusResponse(BaseModel):
    job_id: str
    status: JobStatus
    result: Optional[FactCheckResult] = None
    error: Optional[str] = None
    progress: Optional[int] = Field(None, ge=0, le=100, description="Progress percentage")


class UploadResponse(BaseModel):
    upload_id: str = Field(..., description="Unique upload ID")
    filename: str = Field(..., description="Original filename")
    size: int = Field(..., description="File size in bytes")
    chunks_processed: int = Field(..., description="Number of text chunks processed")
    status: str = Field("completed", description="Upload processing status")