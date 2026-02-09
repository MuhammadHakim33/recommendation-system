from repositories.manticore_repository import ManticoreRepository

class ArticleService:
    def __init__(self, manticore_repo: ManticoreRepository):
        self.manticore_repo = manticore_repo

    def get_articles(self, query: str, limit: int):
        articles = self.manticore_repo.search_articles(query, limit)["data"]

        if not articles or len(articles) == 0:
            raise ValueError("No articles found")

        return articles
        