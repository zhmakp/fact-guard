from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from enum import Enum


class InputType(str, Enum):
    CLAIM = "claim"
    URL = "url"
    UPLOAD = "upload"


class FactCheckRequest(BaseModel):
    claim: Optional[str] = Field(None, description="Text claim to fact-check")
    url: Optional[str] = Field(None, description="URL to fact-check")
    type: InputType = Field(..., description="Type of input")
    
    @validator('type', pre=True, always=True)
    def validate_input_type(cls, v, values):
        if v == InputType.CLAIM and not values.get('claim'):
            raise ValueError('claim is required when type is "claim"')
        if v == InputType.URL and not values.get('url'):
            raise ValueError('url is required when type is "url"')
        return v


class UploadMetadata(BaseModel):
    source_name: str = Field(..., description="Name of the source")
    source_type: Literal["pdf", "csv", "text"] = Field(..., description="Type of uploaded file")
    description: Optional[str] = Field(None, description="Optional description")
    is_trusted: bool = Field(True, description="Whether this is a trusted source")


class ConfidenceThreshold(BaseModel):
    minimum_confidence: float = Field(0.7, ge=0.0, le=1.0, description="Minimum confidence threshold")


class SourceConfig(BaseModel):
    trusted_sources: list[str] = Field(default_factory=list, description="List of trusted source URLs")
    blocked_sources: list[str] = Field(default_factory=list, description="List of blocked source URLs")


class WhitelistSourceRequest(BaseModel):
    source_name: str = Field(..., description="Name of the source")
    source_url: str = Field(..., description="URL of the source")
    source_type: Literal["paper", "webpage", "news", "user_upload"] = Field(..., description="Type of source")