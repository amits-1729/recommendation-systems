# Movie & Book Recommendation API

A FastAPI backend for two recommendation systems:

- 🎬 **Movie Recommendation** – Content-Based Filtering
- 📚 **Book Recommendation** – Item-Item Collaborative Filtering

The project combines ML models with backend concepts like FastAPI, OOP, async requests, caching and rate limiting.

## Features

- Movie recommendations using cosine similarity
- Book recommendations using item-item collaborative filtering
- TMDB API integration for movie details
- Async TMDB requests using `asyncio`
- In-memory caching for TMDB data
- Semaphore for controlling concurrent requests
- API rate limiting using SlowAPI
- Pydantic response validation
- Environment variables for API keys

## Project Structure

```text
recommendation_backend/
│
├── app/
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── movies.py
│   │   └── books.py
│   │
│   ├── services/
│   │   ├── movie_recommender.py
│   │   ├── book_recommender.py
│   │   └── tmdb_service.py
│   │
│   ├── schemas/
│   │   └── recommendation.py
│   │
│   ├── core/
│   │   └── config.py
│   │
│   └── data/
│       ├── movies_vectors.joblib
│       ├── movies_details.joblib
│       ├── books_vectors.joblib
│       ├── books_details.joblib
│       └── top_50_books.joblib
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## API Endpoints

### Movies

```http
GET /movies/recommend/{movie_title}?limit=5
```

Returns similar movies along with their TMDB details such as rating, poster, director and cast.

### Books

```http
GET /books/recommend/{book_title}?limit=5
```

Returns similar books with title, author, publisher and image.

### Top Books

```http
GET /books/top?limit=10
```

Returns the top books from the dataset.

## Running Locally

Clone the repository and install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your TMDB API key:

```env
TMDB_API_KEY=your_api_key
```

Run the server:

```bash
uvicorn app.main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## Tech Stack

- Python
- FastAPI
- Scikit-learn
- Pandas
- Joblib
- HTTPX
- AsyncIO
- SlowAPI
- TMDB API

## Future Improvements

- User authentication
- Personalized recommendations
- Recommendation history
- Automated tests
- Docker deployment