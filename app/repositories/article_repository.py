from sqlmodel import Session, select
from sqlalchemy.orm.exc import NoResultFound
from models.Article import Article, View
from configs.db import engine

class ArticleRepository:
    def get_articles_by_ids(self, article_ids: list[int]):
        try:
            with Session(engine) as session:
                statement = select(Article).where(Article.id.in_(article_ids))
                result = session.exec(statement)
                return result.all()
        except Exception as e:
            print(f"Error getting articles: {e}")
            return []

    def get_article_by_id(self, article_id: int):
        try:
            with Session(engine) as session:
                statement = select(Article).where(Article.id == article_id)
                result = session.exec(statement)
                return result.first()
        except Exception as e:
            print(f"Error getting article: {e}")
            return None

    def get_views_by_user_id(self, user_id: int):
        try:
            with Session(engine) as session:
                statement = select(View).where(View.user_id == user_id)
                result = session.exec(statement)
                return result.all()
        except Exception as e:
            print(f"Error getting views: {e}")
            return []  # Return empty list instead of raising
    
    def get_views_by_article_ids(self, article_ids: list[int]):
        try:
            with Session(engine) as session:
                statement = select(View).where(View.article_id.in_(article_ids))
                result = session.exec(statement)
                return result.all()
        except Exception as e:
            print(f"Error getting views: {e}")
            return []