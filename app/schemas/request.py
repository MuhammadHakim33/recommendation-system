from pydantic import BaseModel
from typing import Optional

class ArticleCreateRequest(BaseModel):
    id: int
    title: str
    content: str


class ArticleUpdateRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
