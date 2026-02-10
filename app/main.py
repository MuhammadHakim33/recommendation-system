from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from services.recommendation_service import RecommendationService
from services.article_service import ArticleService
from repositories.article_repository import ArticleRepository
from repositories.manticore_repository import ManticoreRepository
from schemas.response import SuccessResponse, ErrorResponse, Metadata
from schemas.request import ArticleCreateRequest, ArticleUpdateRequest

# ==========================================
#              INITIALIZATION SECTION
# ==========================================

# repositories
article_repo = ArticleRepository()
manticore_repo = ManticoreRepository()

# services
recommendation_service = RecommendationService(article_repo, manticore_repo)
article_service = ArticleService(manticore_repo)

# ==========================================
#              ROUTING SECTION
# ==========================================

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/recommendation/{user_id}")
def get_recommendation(user_id: int, limit: int = 10):
    try:
        user_vector = recommendation_service.get_user_vector(user_id)
        articles = recommendation_service.get_similar_articles(user_vector, limit)
        result = recommendation_service.ranking(articles)
        
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(SuccessResponse(
                message="Recommendation generated successfully",
                data=result,
            ))
        )
    except ValueError as e:
        # Validation error (user not found, no history, etc.)
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(ErrorResponse(
                message="User not found or has no reading history",
                error=str(e)
            ))
        )
    except Exception as e:
        # Internal server error
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(ErrorResponse(
                message="Internal server error",
                error=str(e)
            ))
        )

@app.get("/news")
def get_news(q: str, l: int = 10):
    try:
        articles = article_service.get_articles(q, l)
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(SuccessResponse(
                message="Search articles successfully",
                data=articles,
            ))
        )
    except ValueError as e:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(ErrorResponse(
                message="No articles found",
                error=str(e)
            ))
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(ErrorResponse(
                message="Internal server error",
                error=str(e)
            ))
        )

@app.post("/news")
def insert_article(req: ArticleCreateRequest):
    try:
        article_service.insert_article_to_manticore(req.dict())
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(SuccessResponse(
                message="Article inserted successfully",
                data=req,
            ))
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(ErrorResponse(
                message="Internal server error",
                error=str(e)
            ))
        )

@app.put("/news/{article_id}")
def update_article(article_id: int, req: ArticleUpdateRequest):
    try:
        result = article_service.update_article_to_manticore(article_id, req.dict())
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(SuccessResponse(
                message="Article updated successfully",
                data=result,
            ))
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(ErrorResponse(
                message="Internal server error",
                error=str(e)
            ))
        )

@app.delete("/news/{article_id}")
def delete_article(article_id: int):
    try:
        result = article_service.delete_article_to_manticore(article_id)
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(SuccessResponse(
                message="Article deleted successfully",
                data=result,
            ))
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(ErrorResponse(
                message="Internal server error",
                error=str(e)
            ))
        )
