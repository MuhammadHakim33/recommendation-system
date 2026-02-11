from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Article(SQLModel, table=True):
    __tablename__ = "articles"
    
    id: int = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str
    published_at: datetime = Field(default=datetime.now())

class View(SQLModel, table=True):
    __tablename__ = "views" 
    
    id: int = Field(default=None, primary_key=True)
    user_id: int
    article_id: int
    created_at: datetime = Field(default=datetime.now())