from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt
from flask import request, jsonify


class MovieResource(Resource):
    def __init__(self, movie_service):
        self.movie_service = movie_service

    @jwt_required()
    def get(self, movie_id=None):
        """Get movie by ID or a paginated list of movies."""
        if movie_id:
            movie = self.movie_service.get_movie_by_id(movie_id)
            if movie:
                return {"movie": movie}, 200
            return {"error": "Movie not found"}, 404
        else:
            # Handle paginated movie list

            sort = request.args.get('sort')

            # Validate sort parameter
            if sort == 'profit_margin':
                limit = request.args.get('limit', type=int)

                # Retrieve the top movies by profit margin
                movies = self.movie_service.get_top_movies_by_profit_margin(sort=sort, limit=limit)

                # Return the response with jsonify to ensure JSON format
                return jsonify(movies)

            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 0))
            sort = request.args.get('sort')

            # Process genre filter from query parameter into a list
            genre_filter = request.args.get('filter')
            genre_list = genre_filter.split(',') if genre_filter else None

            # Retrieve movies data from the service layer
            movies_data = self.movie_service.get_all_movies(
                page=page,
                per_page=per_page,
                sort=sort,
                genre_filter=genre_list
            )
            return movies_data, 200

    @jwt_required()
    def post(self):
        """Create a new movie (Admin only)."""
        claims = get_jwt()
        if claims['role'] != "admin":
            return {"error": "Admin access required"}, 403

        data = request.get_json()
        result = self.movie_service.create_movie(data)
        return result

    # @jwt_required()
    # def post(self):
    #     """Create a new movie (Admin-only)."""
    #     # Check if the current user is an admin
    #     claims = get_jwt_identity()
    #     if claims.get("role") != "admin":
    #         return {"error": "Admin access required"}, 403
    #
    #     # Get data from request
    #     data = request.get_json()
    #
    #     # Call service to create the movie
    #     result, status_code = self.movie_service.create_movie(data)
    #     return jsonify(result), status_code
    @jwt_required()
    def put(self, movie_id):
        """Update an existing movie by ID (Admin only)."""
        claims = get_jwt()
        if claims['role'] != "admin":
            return {"error": "Admin access required"}, 403

        data = request.get_json()
        success = self.movie_service.update_movie(movie_id, data)
        if success:
            return {"message": "Movie updated successfully"}, 200
        return {"error": "Movie not found"}, 404

    @jwt_required()
    def delete(self, movie_id):
        """Delete a movie by ID (Admin only)."""
        claims = get_jwt()
        if claims['role'] != "admin":
            return {"error": "Admin access required"}, 403

        success = self.movie_service.delete_movie(movie_id)
        if success:
            return {"message": "Movie deleted successfully"}, 204
        return {"error": "Movie not found"}, 404

class TopRatedMoviesByYearResource(Resource):
    def __init__(self, movie_service):
        self.movie_service = movie_service

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('year', type=int, required=True, help="Year is required")
        parser.add_argument('limit', type=int, default=5)
        args = parser.parse_args()
        data = self.movie_service.get_top_rated_movies_by_year(args['year'], args['limit'])
        return data, 200



