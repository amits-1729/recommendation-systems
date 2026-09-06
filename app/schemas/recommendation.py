from pydantic import BaseModel
from typing import List


class MovieRecommendation(BaseModel):
    tmdb_id: int
    title: str | None
    overview: str | None
    release_date: str | None
    rating: float | None
    poster: str | None
    director: str | None
    cast: List[str]


class MovieRecommendationResponse(BaseModel):
    title: str
    recommendations: List[MovieRecommendation]


class BookRecommendation(BaseModel):
    title: str
    author: str
    publisher: str
    image_url: str | None


class BookRecommendationResponse(BaseModel):
    title: str
    recommendations: List[BookRecommendation]