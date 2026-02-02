from sqlmodel import SQLModel, Field
from datetime import datetime

class UserHistory(SQLModel, table=True):
    __tablename__ = "reading_history" 
    
    id: int = Field(default=None, primary_key=True)
    user_id: int
    article_id: int
    created_at: datetime = Field(default=datetime.now())

