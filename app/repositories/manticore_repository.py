import json
import manticoresearch
from manticoresearch.rest import ApiException
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

    def get_article_by_id(self, article_id: int):
        """Get article from Manticore by ID"""
        try:
            with manticoresearch.ApiClient(conf) as client:
                utils_api = manticoresearch.UtilsApi(client)
                query = f"SELECT id, article_id, title, content FROM articles WHERE article_id={article_id}"
                response = utils_api.sql(query)
                return response.to_dict()[0]
        except ApiException as e:
            print(f"Error querying Manticore: {e}")
            return json.loads(e.body)
        except Exception as e:
            print(f"Error querying Manticore: {e}")
            return None
    
    def get_similar_articles(self, user_vec: list[float], limit: int):
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

    def get_articles(self, search: str, limit: int):
        try:
            with manticoresearch.ApiClient(conf) as client:
                utils_api = manticoresearch.UtilsApi(client)

                if search:
                    query = f"SELECT id, article_id, title, knn_dist() FROM articles WHERE knn(embedding_vector, 5, '{search}') LIMIT {limit}"
                else:
                    query = f"SELECT id, article_id, title FROM articles LIMIT {limit}"

                response = utils_api.sql(query)
                return response.to_dict()[0]
        except Exception as e:
            print(f"Error searching Manticore: {e}")
            return None
    
    # def get_all_articles(self, limit: int = 100, offset: int = 0):
    #     """Get all articles from Manticore"""
    #     try:
    #         with manticoresearch.ApiClient(conf) as client:
    #             utils_api = manticoresearch.UtilsApi(client)
    #             query = f"SELECT id, article_id, title, content FROM articles LIMIT {offset}, {limit}"
    #             response = utils_api.sql(query)
    #             return response.to_dict()[0]
    #     except ApiException as e:
    #         print(f"Error getting all articles from Manticore: {e}")
    #         return json.loads(e.body)
    #     except Exception as e:
    #         print(f"Error getting all articles from Manticore: {e}")
    #         return {'data': [], 'total': 0, 'error': str(e), 'warning': ''}

    def insert_article(self, article: dict):
        try:
            with manticoresearch.ApiClient(conf) as client:
                utils_api = manticoresearch.UtilsApi(client)
                query = f"INSERT INTO articles (article_id, title, content) VALUES ('{article['id']}', '{article['title']}', '{article['content']}')"
                response = utils_api.sql(query)
                return response.to_dict()[0]
        except ApiException as e:
            print(f"Error inserting articles to Manticore: {e}")
            return json.loads(e.body)
        except Exception as e:
            print(f"Error inserting articles to Manticore: {e}")
            return None

    def update_article(self, article: dict):
        """Update article in Manticore"""
        try:
            with manticoresearch.ApiClient(conf) as client:
                utils_api = manticoresearch.UtilsApi(client)
                query = f"REPLACE INTO articles (id, article_id, title, content) VALUES ({article['id']}, {article['article_id']}, '{article['title']}', '{article['content']}')"
                response = utils_api.sql(query)
                return response.to_dict()[0]
        except ApiException as e:
            print(f"Error updating articles to Manticore: {e}")
            return json.loads(e.body)
        except Exception as e:
            print(f"Error updating articles to Manticore: {e}")
            return None

    def delete_article(self, article_id: int):
        try:
            with manticoresearch.ApiClient(conf) as client:
                utils_api = manticoresearch.UtilsApi(client)
                query = f"DELETE FROM articles WHERE article_id={article_id}"
                response = utils_api.sql(query)
                return response.to_dict()[0]
        except ApiException as e:
            print(f"Error deleting articles to Manticore: {e}")
            return json.loads(e.body)
        except Exception as e:
            print(f"Error deleting articles to Manticore: {e}")
            return None