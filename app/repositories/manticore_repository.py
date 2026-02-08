import manticoresearch
from configs.manticore import conf

class ManticoreRepository:
    def get_articles_by_ids(self, ids: list[int]):
        """Get articles from Manticore by IDs"""
        if not ids:
            return {'data': [], 'total': 0}
        
        try:
            with manticoresearch.ApiClient(conf) as client:
                utils_api = manticoresearch.UtilsApi(client)
                query = f"SELECT id, article_id, embedding_vector FROM articles WHERE article_id IN ({','.join(map(str, ids))})"
                response = utils_api.sql(query)
                return response.to_dict()[0]
        except Exception as e:
            print(f"Error querying Manticore: {e}")
            return None
    
    def get_similar_articles(self, user_vec: list[float], limit: int = 10):
        try:
            with manticoresearch.ApiClient(conf) as client:
                utils_api = manticoresearch.UtilsApi(client)
                vector_str = ','.join(map(str, user_vec))
                query = f"SELECT id, article_id, title, knn_dist() FROM articles WHERE knn(embedding_vector, 5, ({vector_str})) LIMIT {limit}"
                response = utils_api.sql(query)
                return response.to_dict()[0]
        except Exception as e:
            print(f"Error querying Manticore: {e}")
            return None