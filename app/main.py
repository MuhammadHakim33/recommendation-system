from fastapi import FastAPI
from services.recommendation_service import RecommendationService
from repositories.article_repository import ArticleRepository
from repositories.manticore_repository import ManticoreRepository

# ==========================================
#              INITIALIZATION SECTION
# ==========================================

# repositories
article_repo = ArticleRepository()
manticore_repo = ManticoreRepository()

# services
recommendation_service = RecommendationService(article_repo, manticore_repo)

# ==========================================
#              ROUTING SECTION
# ==========================================

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/recommendation/{user_id}")
def get_recommendation(user_id: int):
    user_vector = recommendation_service.get_user_vector(user_id)
    articles = recommendation_service.get_similar_articles(user_vector, 20)
    return recommendation_service.ranking(articles)
