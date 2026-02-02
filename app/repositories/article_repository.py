from configs.db import engine
from sqlmodel import Session, select
from models.Article import Article

def get_articles_by_ids(article_ids: list[int]):
    with Session(engine) as session:
        statement = select(Article).where(Article.id.in_(article_ids))
        result = session.exec(statement)
        return result.all()
