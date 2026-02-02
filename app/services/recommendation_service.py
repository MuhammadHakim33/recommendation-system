from repositories.user_repository import get_user_reading_history
from repositories.article_repository import get_articles_by_ids

def get_user_vector(user_id: int):
    return get_user_reading_history(user_id)