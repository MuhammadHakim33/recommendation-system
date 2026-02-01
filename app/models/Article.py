from sqlmodel import SQLModel, Field

class Article(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str
    published_at: datetime = Field(default=datetime.now())