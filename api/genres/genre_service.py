class GenreService:
    def __init__(self, genre_repository):
        self.genre_repository = genre_repository
    def get_all_genres(self):
        return self.genre_repository.get_all_genres()
    def get_genre_popularity_revenue_correlation(self):
        return self.genre_repository.get_genre_popularity_revenue_correlation()

    def get_most_profitable_genres_for_keywords(self, keywords=None):
        return self.genre_repository.get_most_profitable_genres_for_keywords(keywords=keywords)

    def get_profit_margin_by_genre_and_year(self):
        return self.genre_repository.get_profit_margin_by_genre_and_year()