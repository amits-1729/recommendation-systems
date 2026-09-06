import joblib
from sklearn.metrics.pairwise import cosine_similarity

from app.core.config import (
    MOVIES_VECTORS_PATH,
    MOVIES_DETAILS_PATH
)


class MovieRecommender:

    def __init__(self):
        self.vectors = joblib.load(MOVIES_VECTORS_PATH)
        self.movies = joblib.load(MOVIES_DETAILS_PATH)

    def recommend(self, movie_title: str, limit: int = 5):

        movie_index = self.movies[self.movies["title"].str.lower() == movie_title.lower()].index
        if len(movie_index) == 0:
            return None

        movie_index = movie_index[0]
        similarity_scores = cosine_similarity(
            self.vectors[movie_index],
            self.vectors
        )[0]

        similar_indices = similarity_scores.argsort()[-limit-1:][::-1]

        recommendations = []
        for index in similar_indices:
            if index == movie_index:
                continue
            recommendations.append({
                "id": int(self.movies.iloc[index]["id"]),
                "title": self.movies.iloc[index]["title"],
                "score": float(self.movies.iloc[index]["score"])
            })

        return recommendations