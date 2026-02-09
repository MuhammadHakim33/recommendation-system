from pydantic import BaseModel
from datetime import datetime
from typing import Any, Optional

class Metadata(BaseModel):
    total: int
    generated_at: datetime
    filters_applied: dict

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    error: str

class SuccessResponse(BaseModel):
    status: str = "success"
    message: str
    data: list 
    metadata: Optional[Metadata] = None 
    
    class Config:
        arbitrary_types_allowed = True 