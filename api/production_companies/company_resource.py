from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required

class TopProductionCompaniesResource(Resource):
    method_decorators = [jwt_required()]  # Apply JWT authentication to this resource

    def __init__(self, production_company_service):
        self.production_company_service = production_company_service

    def get(self):
        # Get query parameters
        limit = int(request.args.get('limit', 0))
        sort = request.args.get('sort')
        genres = request.args.get('genres', '').split(',')
        start_year = int(request.args.get('start_year', 1970))
        end_year = int(request.args.get('end_year', 2023))

        # Validate sort parameter
        if sort != 'total_revenue':
            return {"error": "Invalid sort parameter. Must be 'total_revenue'."}, 400

        # Fetch top production companies by revenue with filters
        data = self.production_company_service.get_top_production_companies(
            genres=genres, 
            start_year=start_year, 
            end_year=end_year, 
            limit=limit
        )
        return jsonify(data)
