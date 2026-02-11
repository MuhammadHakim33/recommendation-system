from pydantic import BaseModel
from datetime import datetime
from typing import Any, Optional

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    error: str

class SuccessResponse(BaseModel):
    status: str = "success"
    message: str
    data: Any