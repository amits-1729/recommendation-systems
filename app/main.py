from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.routes.movies import router as movie_router
from app.routes.books import router as book_router

from fastapi.middleware.cors import CORSMiddleware


limiter = Limiter(
    key_func=get_remote_address
)


app = FastAPI(
    title="Movie & Book Recommendation API",
    description="Recommendation API using ML models",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production domains as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)


app.include_router(movie_router)
app.include_router(book_router)


@app.get("/")
def root():
    return {
        "message": "Movie & Book Recommendation API is running"
    }