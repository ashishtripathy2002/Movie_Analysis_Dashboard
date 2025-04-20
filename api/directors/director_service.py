class DirectorService:
    def __init__(self, director_repository):
        self.director_repository = director_repository

    def get_all_directors(self):
        return self.director_repository.get_all_directors()

    def get_top_directors_by_movie_count(self,sort, limit=5):
        return self.director_repository.get_top_directors_by_movie_count(sort, limit)

    def get_directors_with_most_top_grossing_movies(self):
        return self.director_repository.get_directors_with_most_top_grossing_movies()

    def get_director_actor_collaborations(self, sort, limit):
        return self.director_repository.get_director_actor_collaborations(sort,limit)
