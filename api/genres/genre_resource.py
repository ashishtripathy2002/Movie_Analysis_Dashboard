from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity


class GenreResource(Resource):
    method_decorators = [jwt_required()]
    def __init__(self, genre_service):
        self.genre_service = genre_service

    @jwt_required()
    def get(self):
        data = self.genre_service.get_all_genres()
        return jsonify(data)
class GenrePopularityRevenueCorrelationResource(Resource):
    method_decorators = [jwt_required()]

    def __init__(self, genre_service):
        self.genre_service = genre_service

    @jwt_required()
    def get(self):
        # Call service to get correlation data
        data = self.genre_service.get_genre_popularity_revenue_correlation()
        return jsonify(data)


class GenreProfitableMoviesResource(Resource):
    method_decorators = [jwt_required()]

    def __init__(self, genre_service):
        self.genre_service = genre_service

    @jwt_required()
    def get(self):
        # Parse optional 'keywords' query parameter
        keywords = request.args.get('keywords')
        keywords_list = keywords.split(',') if keywords else None
        print(keywords_list, keywords)

        # Call service to get profitable genres data
        data = self.genre_service.get_most_profitable_genres_for_keywords(keywords=keywords_list)
        return jsonify(data)

class GenreProfitMarginResource(Resource):
    method_decorators = [jwt_required()]

    def __init__(self, genre_service):
        self.genre_service = genre_service
    @jwt_required()
    def get(self):
        # Fetch profit margin by genre data
        data = self.genre_service.get_profit_margin_by_genre_and_year()
        return jsonify(data)