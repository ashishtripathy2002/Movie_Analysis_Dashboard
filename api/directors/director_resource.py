from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from directors.director_service import DirectorService


class TopDirectorsResource(Resource):
    def __init__(self, director_service: DirectorService):
        self.director_service = director_service

    @jwt_required()
    def get(self):
        sort = request.args.get('sort')
        limit = request.args.get('limit', type=int)

        if sort:
            # If sorting or limit is specified, call get_top_directors
            directors = self.director_service.get_top_directors_by_movie_count(sort=sort, limit=limit)
        else:
            # If no sorting or limit, call get_all_directors
            directors = self.director_service.get_all_directors()

        return jsonify(directors)


class TopGrossingDirectorsResource(Resource):
    def __init__(self, director_service: DirectorService):
        self.director_service = director_service

    @jwt_required()
    def get(self):
        directors = self.director_service.get_directors_with_most_top_grossing_movies()
        return jsonify(directors)

class DirectorActorCollaborationResource(Resource):
    def __init__(self, director_service: DirectorService):
        self.director_service = director_service

    @jwt_required()
    def get(self):
        limit = int(request.args.get('limit', 0))
        sort = request.args.get('sort')
        collaborations = self.director_service.get_director_actor_collaborations(sort,limit)
        return jsonify(collaborations)
