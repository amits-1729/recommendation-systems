from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

MOVIES_VECTORS_PATH = DATA_DIR / "movies_vectors.joblib"
MOVIES_DETAILS_PATH = DATA_DIR / "movies_details.joblib"

BOOKS_VECTORS_PATH = DATA_DIR / "books_vectors.joblib"
BOOKS_DETAILS_PATH = DATA_DIR / "books_details.joblib"

TOP_BOOKS_PATH = DATA_DIR / "top_50_books.joblib"

TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not TMDB_API_KEY:
    raise ValueError(
        "TMDB_API_KEY is not configured"
    )