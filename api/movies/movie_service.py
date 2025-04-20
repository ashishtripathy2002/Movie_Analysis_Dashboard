class MovieService:
    def __init__(self, movie_repository):
        self.movie_repository = movie_repository

    def get_movie_by_id(self, movie_id):
        """Retrieve a movie by its ID."""
        return self.movie_repository.get_movie_by_id(movie_id)

    def get_all_movies(self, page, per_page, sort=None, genre_filter=None):
        """Retrieve all movies with pagination, sorting, and filtering."""
        movies = self.movie_repository.get_all_movies(
            page=page,
            per_page=per_page,
            sort=sort,
            genre_list=genre_filter
        )
        total_count = self.movie_repository.get_total_movies_count(genre_filter)

        return {
            "movies": movies,
            "total_count": total_count,
            "page": page,
            "per_page": per_page
        }

    def create_movie(self, data):
        """Create a new movie with associations."""
        # Validate input data if needed (e.g., check required fields)
        # required_fields = ["title", "release_date", "runtime", "overview", "budget", "revenue", "vote_average"]
        # missing_fields = [field for field in required_fields if field not in data]
        #
        # if missing_fields:
        #     return {"error": f"Missing required fields: {', '.join(missing_fields)}"}, 400

        # Call the repository to create the movie and handle associations
        return self.movie_repository.create_movie(data)

    def update_movie(self, movie_id, data):
        """Update an existing movie."""
        return self.movie_repository.update_movie(movie_id, data)

    def delete_movie(self, movie_id):
        """Delete a movie by its ID."""
        return self.movie_repository.delete_movie(movie_id)

    def get_top_rated_movies_by_year(self, year, limit=5):
        return self.movie_repository.get_top_rated_movies_by_year(year, limit)

    def get_top_movies_by_profit_margin(self,sort, limit):
        return self.movie_repository.get_top_movies_by_profit_margin(sort,limit)

    def get_summary_statistics(self):
        return self.movie_repository.get_summary_statistics()