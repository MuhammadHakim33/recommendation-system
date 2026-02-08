from repositories.article_repository import ArticleRepository
from repositories.manticore_repository import ManticoreRepository
import numpy as np
from datetime import datetime, timedelta

class RecommendationService:
    def __init__(self, article_repo: ArticleRepository, manticore_repo: ManticoreRepository):
        self.article_repo = article_repo
        self.manticore_repo = manticore_repo

    def get_user_vector(self, user_id: int):
        # get user reading history
        history = self.article_repo.get_views_by_user_id(user_id)
        
        # get articles ids
        ids = [item.article_id for item in history]

        # get articles
        articles = self.manticore_repo.get_articles_by_ids(ids)
        
        vectors = []

        for article in articles['data']:
            vec_list = [float(x) for x in article['embedding_vector'].split(',')]
            vectors.append(vec_list)

        np_vec = np.array(vectors)
        user_vec = np.mean(np_vec, axis=0)

        return user_vec.tolist()
    
    def get_similar_articles(self, user_vector: list[float], limit: int = 10):
        return self.manticore_repo.get_similar_articles(user_vector, limit)['data']

    def ranking(self, articles_manticore: list[dict]):
        article_ids = [article['article_id'] for article in articles_manticore]
        
        articles_db = self.article_repo.get_articles_by_ids(article_ids)

        view_db = self.article_repo.get_views_by_article_ids(article_ids)

        filtered_articles = []
        for i in range(len(articles_manticore)):
            # filter articles older than 60 days
            if articles_db[i].published_at < datetime.now() - timedelta(days=60):
                continue
            # filter articles that have been read by user
            if articles_manticore[i]['article_id'] in view_db:
                continue

            filtered_articles.append(articles_manticore[i])

        final_article_ids = [article['article_id'] for article in filtered_articles]

        result = self.article_repo.get_articles_by_ids(final_article_ids)

        return result