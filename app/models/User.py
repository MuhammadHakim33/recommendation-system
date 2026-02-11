from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    created_at: Optional[datetime] = Field(default=datetime.now())