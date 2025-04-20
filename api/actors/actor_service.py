class ActorService:
    def __init__(self, actor_repository):
        self.actor_repository = actor_repository
    def get_all_actors(self):
        return self.actor_repository.get_all_actors()
    def get_actors_with_highest_avg_vote(self,sort, genre, limit=100):
        return self.actor_repository.get_actors_with_highest_avg_vote(sort, genre, limit)

    def get_actors_rating_difference_between_genres(self, genre1, genre2, limit=100):
        return self.actor_repository.get_actors_rating_difference_between_genres(genre1, genre2, limit)

    def get_actors_with_most_high_rated_appearances(self, min_rating=8, limit=100):
        return self.actor_repository.get_actors_with_most_high_rated_appearances(min_rating, limit)
