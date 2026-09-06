from fastapi import APIRouter, HTTPException, Query

from app.services.book_recommender import BookRecommender
from app.schemas.recommendation import BookRecommendationResponse


router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

book_recommender = BookRecommender()

@router.get("")
def get_books():
    books = book_recommender.books["title"].tolist()

    return {
        "books": books
    }


@router.get("/search")
def search_books(
    query: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=50)
):
    books = book_recommender.books

    results = books[
        books["title"].str.contains(
            query,
            case=False,
            na=False
        )
    ]["title"].head(limit).tolist()

    return {
        "books": results
    }

@router.get(
    "/recommend/{book_title}",
    response_model=BookRecommendationResponse
)
def recommend_books(
    book_title: str,
    limit: int = Query(default=5, ge=1, le=20)
):

    recommendations = book_recommender.recommend(
        book_title,
        limit
    )

    if recommendations is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return {
        "title": book_title,
        "recommendations": recommendations
    }


@router.get("/top")
def get_top_books(limit: int = Query(default=50, ge=1, le=50)):

    return book_recommender.get_top_books(limit)