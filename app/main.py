from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from services.recommendation_service import RecommendationService
from services.article_service import ArticleService
from services.user_service import UserService
from repositories.article_repository import ArticleRepository
from repositories.manticore_repository import ManticoreRepository
from repositories.user_repository import UserRepository
from schemas.response import SuccessResponse, ErrorResponse
from schemas.request import ArticleCreateRequest, ArticleUpdateRequest

# ==========================================
#              INITIALIZATION SECTION
# ==========================================

# repositories
article_repo = ArticleRepository()
manticore_repo = ManticoreRepository()
user_repo = UserRepository()

# services
recommendation_service = RecommendationService(article_repo, manticore_repo)
article_service = ArticleService(manticore_repo)
user_service = UserService(user_repo)

# ==========================================
#              ROUTING SECTION
# ==========================================

app = FastAPI()

router = APIRouter(prefix="/api/v1", tags=["Recommendation"])

# MAIN ROUTES

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/recommendation/{user_id}")
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

@router.get("/articles")
def list_articles_from_mysql(limit: int = 100):
    """List all articles from MySQL database"""
    try:
        articles = article_repo.get_all_articles(limit=limit)
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(SuccessResponse(
                message=f"Retrieved {len(articles)} articles from MySQL",
                data=[{
                    "id": article.id,
                    "title": article.title,
                    "category": article.category,
                    "published_at": article.published_at.isoformat() if article.published_at else None
                } for article in articles],
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

@router.get("/users")
def list_users(limit: int = 100):
    """List all users from MySQL database"""
    try:
        users = user_service.get_all_users(limit=limit)
        return JSONResponse(
            status_code=200,
            content=jsonable_encoder(SuccessResponse(
                message=f"Retrieved {len(users)} users from MySQL",
                data=users,
            ))
        )
    except ValueError as e:
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder(ErrorResponse(
                message="User not found",
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


# MANTICORE ROUTES

@router.get("/manticore/articles")
def get_articles_from_manticore(search: str = "", limit: int = 100):
    try:
        articles = article_service.get_articles_from_manticore(search, limit)
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

@router.post("/manticore/articles")
def insert_article_to_manticore(req: ArticleCreateRequest):
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

@router.put("/manticore/articles/{article_id}")
def update_article_to_manticore(article_id: int, req: ArticleUpdateRequest):
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

@router.delete("/manticore/articles/{article_id}")
def delete_article_to_manticore(article_id: int):
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


app.include_router(router)
