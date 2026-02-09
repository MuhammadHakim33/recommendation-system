from repositories.article_repository import ArticleRepository
from repositories.manticore_repository import ManticoreRepository
import numpy as np
from datetime import datetime, timedelta

class RecommendationService:
    def __init__(self, article_repo: ArticleRepository, manticore_repo: ManticoreRepository):
        self.article_repo = article_repo
        self.manticore_repo = manticore_repo

    def get_user_vector(self, user_id: int):
        # Get user reading history
        history = self.article_repo.get_views_by_user_id(user_id)
        
        # Validate: user must have reading history
        if not history or len(history) == 0:
            raise ValueError(f"User {user_id} has no reading history. Cannot generate recommendations.")
        
        # Get article IDs
        ids = [item.article_id for item in history]

        # Get articles with embeddings from Manticore
        articles = self.manticore_repo.get_articles_by_ids(ids)
        
        if not articles or 'data' not in articles or len(articles['data']) == 0:
            raise ValueError(f"No articles found in Manticore for user {user_id}'s history")
        
        # Extract vectors from articles
        vectors = []
        for article in articles['data']:
            vec_list = [float(x) for x in article['embedding_vector'].split(',')]
            vectors.append(vec_list)

        # Calculate average vector (user's interest profile)
        np_vec = np.array(vectors)
        user_vec = np.mean(np_vec, axis=0)

        return user_vec.tolist()
    
    def get_similar_articles(self, user_vector: list[float], limit: int = 10):
        return self.manticore_repo.get_similar_articles(user_vector, limit)['data']

    def ranking(self, articles_manticore: list[dict]) -> list:
        """
        Rank and filter articles based on:
        1. Age (not older than 60 days)
        2. Already read by user (exclude)
        """

        # get article ids from manticore
        article_ids = [article['article_id'] for article in articles_manticore]
        
        # get full article data from MySQL
        articles_db = self.article_repo.get_articles_by_ids(article_ids)

        # create dictionary lookup
        articles_dict = {article.id: article for article in articles_db}

        # get user's reading history (articles they've already read)
        view_db = self.article_repo.get_views_by_article_ids(article_ids)
        view_ids = [view.article_id for view in view_db]

        filtered_articles = []
        age = datetime.now() - timedelta(days=60)

        for item in articles_manticore:
            id = item['article_id']
            article = articles_dict[id]
            
            # filter 1: articles older than 60 days
            if article.published_at < age:
                continue

            # filter 2: articles that have been read by user
            if id in view_ids:
                continue

            filtered_articles.append(item)

        # Get final article details
        final_article_ids = [article['article_id'] for article in filtered_articles]
        result = self.article_repo.get_articles_by_ids(final_article_ids)

        return result