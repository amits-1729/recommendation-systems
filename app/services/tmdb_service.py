import time
import asyncio
import httpx

from app.core.config import TMDB_API_KEY


class TMDBService:

    BASE_URL = "https://api.themoviedb.org/3"
    CACHE_DURATION = 60 * 60  # 1 hour

    def __init__(self):
        self.api_key = TMDB_API_KEY
        self.cache = {}
        self.semaphore = asyncio.Semaphore(5)

    async def get_top_rated_movies(
        self,
        client: httpx.AsyncClient,
        page: int = 1
    ):
        url = f"{self.BASE_URL}/movie/top_rated"

        params = {
            "api_key": self.api_key,
            "language": "en-US",
            "page": page
        }

        try:
            response = await client.get(
                url,
                params=params,
                timeout=5
            )

        except httpx.RequestError:
            return None

        if response.status_code != 200:
            return None

        data = response.json()

        movies = []

        for movie in data.get("results", []):
            poster_path = movie.get("poster_path")

            poster_url = None

            if poster_path:
                poster_url = (
                    "https://image.tmdb.org/t/p/w500"
                    f"{poster_path}"
                )

            movies.append({
                "tmdb_id": movie.get("id"),
                "title": movie.get("title"),
                "rating": movie.get("vote_average"),
                "poster": poster_url,
                "release_date": movie.get("release_date")
            })

        return movies

    async def get_movie_details(
        self,
        tmdb_id: int,
        client: httpx.AsyncClient
    ):

        cached_data = self.cache.get(tmdb_id)
        if cached_data:
            data, timestamp = cached_data
            if time.time() - timestamp < self.CACHE_DURATION:
                return data

            del self.cache[tmdb_id]


        async with self.semaphore:
            cached_data = self.cache.get(tmdb_id)
            if cached_data:
                data, timestamp = cached_data
                if time.time() - timestamp < self.CACHE_DURATION:
                    return data

                del self.cache[tmdb_id]


            url = f"{self.BASE_URL}/movie/{tmdb_id}"
            params = {
                "api_key": self.api_key,
                "append_to_response": "credits"
            }
            try:
                response = await client.get(
                    url,
                    params=params,
                    timeout=5
                )

            except httpx.RequestError:
                return None

            if response.status_code == 404:
                return None

            if response.status_code == 401:
                raise RuntimeError("Invalid TMDB API key")

            if response.status_code == 429:
                return None

            if response.status_code >= 500:
                return None

            if response.status_code != 200:
                return None

            data = response.json()

            director = None
            crew = data.get("credits", {}).get("crew", [])
            for person in crew:
                if person.get("job") == "Director":
                    director = person.get("name")
                    break

            cast = data.get("credits", {}).get("cast", [])
            cast_names = [
                person.get("name")
                for person in cast[:3]
            ]

            poster_path = data.get("poster_path")
            poster_url = None
            if poster_path:
                poster_url = (
                    "https://image.tmdb.org/t/p/w500"
                    f"{poster_path}"
                )

            result = {
                "tmdb_id": tmdb_id,
                "title": data.get("title"),
                "overview": data.get("overview"),
                "release_date": data.get("release_date"),
                "rating": data.get("vote_average"),
                "poster": poster_url,
                "director": director,
                "cast": cast_names
            }

            self.cache[tmdb_id] = (
                result,
                time.time()
            )

            return result

    