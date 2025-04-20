from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from keywords.keywords_service import KeywordsService


class KeywordsResource(Resource):
    def __init__(self, keywords_service: KeywordsService):
        self.keywords_service = keywords_service

    @jwt_required()
    def get(self):
        keywords = self.keywords_service.get_all_keywords()
        return jsonify(keywords)