from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required


class SummaryStatisticsResource(Resource):
    method_decorators = [jwt_required()]

    def __init__(self, movie_service):
        self.movie_service = movie_service

    @jwt_required()
    def get(self):
        # Fetch summary data from the service
        data = self.movie_service.get_summary_statistics()
        return jsonify(data)
