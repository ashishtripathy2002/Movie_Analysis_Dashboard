from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required

class ActorsHighestAvgVoteResource(Resource):
    def __init__(self, actor_service):
        self.actor_service = actor_service

    @jwt_required()
    def get(self):
        genre = request.args.get('genre')
        limit = request.args.get('limit', type=int, default=100)
        sort = request.args.get('sort')
        if genre or sort:
            actors = self.actor_service.get_actors_with_highest_avg_vote(sort, genre, limit)
        else:
            actors = self.actor_service.get_all_actors()
        return jsonify(actors)


class ActorsGenreRatingDifferenceResource(Resource):
    def __init__(self, actor_service):
        self.actor_service = actor_service

    @jwt_required()
    def get(self):
        genre1 = request.args.get('genre1')
        genre2 = request.args.get('genre2')
        limit = request.args.get('limit', type=int, default=100)
        actors = self.actor_service.get_actors_rating_difference_between_genres(genre1, genre2, limit)
        return jsonify(actors)


class ActorsHighRatedAppearancesResource(Resource):
    def __init__(self, actor_service):
        self.actor_service = actor_service

    @jwt_required()
    def get(self):
        min_rating = request.args.get('min_rating', type=float, default=8)
        limit = request.args.get('limit', type=int, default=100)
        actors = self.actor_service.get_actors_with_most_high_rated_appearances(min_rating, limit)
        return jsonify(actors)
