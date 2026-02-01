from sqlmodel import SQLModel, Field

class UserHistory(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int
    article_id: int
    created_at: datetime = Field(default=datetime.now())

