import asyncio
import httpx

from fastapi import APIRouter, HTTPException, Request, Query

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.services.movie_recommender import MovieRecommender
from app.services.tmdb_service import TMDBService

from app.schemas.recommendation import MovieRecommendationResponse

limiter = Limiter(
    key_func=get_remote_address
)


router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)


movie_recommender = MovieRecommender()
tmdb_service = TMDBService()

@router.get("")
def get_movies():
    movies = movie_recommender.movies["title"].tolist()

    return {
        "movies": movies
    }


@router.get("/search")
def search_movies(
    query: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=50)
):
    movies = movie_recommender.movies

    results = movies[
        movies["title"].str.contains(
            query,
            case=False,
            na=False
        )
    ]["title"].head(limit).tolist()

    return {
        "movies": results
    }


@router.get(
    "/recommend/{movie_title}",
    response_model=MovieRecommendationResponse
)
@limiter.limit("10/minute")
async def recommend_movies(
    request: Request,
    movie_title: str,
    limit: int = Query(default=5, ge=1, le=20)
):

    recommendations = movie_recommender.recommend(
        movie_title,
        limit
    )

    if recommendations is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    try:
        async with httpx.AsyncClient() as client:

            tasks = [
                tmdb_service.get_movie_details(
                    movie["id"],
                    client
                )
                for movie in recommendations
            ]
            movie_details = await asyncio.gather(*tasks)

    except RuntimeError:
        raise HTTPException(
            status_code=502,
            detail="Movie information service is currently unavailable"
        )

    movie_details = [
        movie
        for movie in movie_details
        if movie is not None
    ]

    return {
        "title": movie_title,
        "recommendations": movie_details
    }


@router.get("/top-rated")
async def get_top_rated_movies(
    page: int = Query(1, ge=1, le=10)
):
    async with httpx.AsyncClient() as client:

        movies = await tmdb_service.get_top_rated_movies(
            client,
            page
        )

    if movies is None:
        raise HTTPException(
            status_code=502,
            detail="Unable to fetch movies from TMDB"
        )

    return {
        "page": page,
        "movies": movies
    }