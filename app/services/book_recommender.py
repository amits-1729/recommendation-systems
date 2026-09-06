import joblib
from sklearn.metrics.pairwise import cosine_similarity

from app.core.config import (
    BOOKS_VECTORS_PATH,
    BOOKS_DETAILS_PATH,
    TOP_BOOKS_PATH
)


class BookRecommender:

    def __init__(self):
        self.vectors = joblib.load(BOOKS_VECTORS_PATH)
        self.books = joblib.load(BOOKS_DETAILS_PATH)
        self.top_books = joblib.load(TOP_BOOKS_PATH)

    def recommend(self, book_title: str, limit: int = 5):

        book_index = self.books[self.books["title"].str.lower() == book_title.lower()].index
        if len(book_index) == 0:
            return None

        book_index = book_index[0]
        similarity_scores = cosine_similarity(
            self.vectors[book_index],
            self.vectors
        )[0]

        similar_indices = similarity_scores.argsort()[-limit-1:][::-1]
        recommendations = []

        for index in similar_indices:
            if index == book_index:
                continue

            book = self.books.iloc[index]
            recommendations.append({
                "title": book["title"],
                "author": book["author"],
                "publisher": book["publisher"],
                "image_url": book["image_url_m"]
            })

        return recommendations

    def get_top_books(self, limit: int = 50):

        return self.top_books.head(limit).to_dict(
            orient="records"
        )