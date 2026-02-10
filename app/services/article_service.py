from repositories.manticore_repository import ManticoreRepository

class ArticleService:
    def __init__(self, manticore_repo: ManticoreRepository):
        self.manticore_repo = manticore_repo

    def get_articles(self, query: str, limit: int):
        articles = self.manticore_repo.search_articles(query, limit)["data"]

        if not articles or len(articles) == 0:
            raise ValueError("No articles found")

        return articles
        
    def insert_article_to_manticore(self, article: dict):
        result = self.manticore_repo.insert_article(article)

        if result == None:
            raise ValueError("Failed to insert article")

        return result

    def update_article_to_manticore(self, article_id: int, article: dict):
        article_db = self.manticore_repo.get_article_by_id(article_id)['data']

        if not article_db:
            raise ValueError("No articles found")

        data = {
            'id': article_db[0]['id'],
            'article_id': article_id,
            'title': article_db[0]['title'],
            'content': article_db[0]['content']
        }

        if article.get('title'):
            data['title'] = article['title']

        if article.get('content'):
            data['content'] = article['content']

        result = self.manticore_repo.update_article(data)

        if result['error']:
            raise ValueError(f"Failed to update article: {result['error']}")

        return result

    def delete_article_to_manticore(self, article_id: int):
        article_db = self.manticore_repo.get_article_by_id(article_id)['data']

        if not article_db:
            raise ValueError("No articles found")

        result = self.manticore_repo.delete_article(article_id)

        if result['error']:
            raise ValueError(f"Failed to delete article: {result['error']}")

        return {
            'article_id': article_id,
            'status': 'deleted'
        }