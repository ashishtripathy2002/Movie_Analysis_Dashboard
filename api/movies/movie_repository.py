from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.sql import text

class MovieRepository:
    def __init__(self, db):
        self.db = db

    def get_all_movies(self, page, per_page, sort=None, genre_list=None):
        """Retrieve movies with pagination, sorting, and multi-genre 'contains' filtering."""
        offset = (page - 1) * per_page
        valid_sort_fields = {'vote_average', 'revenue', 'profit_margin'}
        sort_clause = f"ORDER BY {sort} DESC" if sort in valid_sort_fields else ""

        genre_filter_clause = ""
        params = {'per_page': per_page, 'offset': offset}

        # Apply genre 'contains' filtering if genre_filter is provided
        if genre_list:
            
            # Adjust the query to return movies that contain at least all specified genres
            genre_filter_clause = """
                WHERE ARRAY[:genre_list] <@ genres
            """
            params['genre_list'] = genre_list
        limit_clause = "LIMIT :per_page OFFSET :offset" if per_page > 0 else ""
        if per_page > 0:
            params['per_page'] = per_page
        query = text(f"""
                SELECT 
                    movie_id, 
                    original_title AS title, 
                    release_date, 
                    runtime, 
                    overview, 
                    budget, 
                    revenue, 
                    vote_average,
                     tagline,
                    keywords,
                    genres,
                    actors,
                    directors,
                    production_companies
                FROM 
                    movie_details_view
            {genre_filter_clause}
            {sort_clause}
            {limit_clause}
        """)

        result = self.db.execute_dql_commands(query, params)
        movies = [
            {
                "movie_id": row.movie_id,
                "title": row.title,
                "release_date": row.release_date,
                "runtime": row.runtime,
                "overview": row.overview,
                "budget": row.budget,
                "revenue": row.revenue,
                "tagline":row.tagline,
                "vote_average": row.vote_average,
                "genres": row.genres,
                "actors": row.actors,
                "directors": row.directors,
                "keywords":row.keywords,
                "production_companies": row.production_companies
            }
            for row in result.fetchall()
        ] if result else []
        return movies

    def get_total_movies_count(self, genre_filter=None):
        """Get the total number of movies, with optional genre filtering."""
        genre_filter_clause = "WHERE genres LIKE :genre_filter" if genre_filter else ""
        query = text(f"SELECT COUNT(movie_id) FROM movie_details_view {genre_filter_clause}")

        params = {'genre_filter': f"%{genre_filter}%"} if genre_filter else None
        result = self.db.execute_dql_commands(query, params)
        return result.fetchone()[0] if result else 0

    def get_movie_by_id(self, movie_id):
        """Retrieve a movie by its ID."""
        query = text("SELECT * FROM movie_details_view WHERE movie_id = :movie_id")
        result = self.db.execute_dql_commands(query, {'movie_id': movie_id})

        # Check if a result was found; return None if no movie exists
        row = result.fetchone() if result else None
        if row is None:
            return None

        # Convert the row to a dictionary using row._mapping
        return {
            "movie_id": row.movie_id,
            "title": row.original_title,
            "release_date": row.release_date,
            "runtime": row.runtime,
            "overview": row.overview,
            "revenue": row.revenue,
            "budget": row.budget,
            "vote_average": row.vote_average,
            "actors": row.actors,
            "genres": row.genres,
            "production_companies": row.production_companies,
            "directors": row.directors,
            "keywords": row.keywords
        }

    def update_movie(self, movie_id, data):
      
        """Update fields of an existing movie."""
        update_fields = []
        for key in data.keys():
            update_fields.append(f"{key} = :{key}")
        update_clause = ", ".join(update_fields)
        query = text(f"UPDATE movies SET {update_clause} WHERE movie_id = :movie_id")
        params = {"movie_id": movie_id, **data}
   
        # Execute the query
        result = self.db.execute_ddl_and_dml_commands(query, params)
        
        # Check if any rows were updated
        if result.rowcount is None:
            return False
        return result.rowcount > 0


    def delete_movie(self, movie_id):
        """Delete a movie by its ID."""
        query = text("DELETE FROM movies WHERE movie_id = :movie_id")
        result = self.db.execute_ddl_and_dml_commands(query, {'movie_id': movie_id})
        return result.rowcount > 0

    def get_top_rated_movies_by_year(self, year, limit):
        query = text("""
            SELECT movie_id, original_title AS title, vote_average
            FROM movies
            WHERE EXTRACT(YEAR FROM release_date) = :year
            ORDER BY vote_average DESC
            LIMIT :limit
        """)
        result = self.db.execute_dql_commands(query, {'year': year, 'limit': limit})
        return [{"movie_id": row.movie_id, "title": row.title, "vote_average": row.vote_average} for row in
                result.fetchall()]

    def get_top_movies_by_profit_margin(self, sort=None, limit=None):
        sort_clause = "ORDER BY profit_margin DESC" if sort == "profit_margin" else ""
        limit_clause = "LIMIT :limit" if limit is not None else ""
        query = text(f"""
            SELECT m.movie_id, m.original_title AS movie_title, 
            COALESCE(m.revenue / NULLIF(m.budget, 0), 0) AS profit_margin,m.revenue, m.budget
            FROM movies AS m WHERE m.budget IS NOT NULL AND m.revenue IS NOT NULL
            {sort_clause} {limit_clause}
        """)

        params = {}
        if limit is not None:
            params['limit'] = limit

        result = self.db.execute_dql_commands(query, params)
        data = result.fetchall() if result else []
        return [
            {
                "movie_id": row.movie_id,"movie_title": row.movie_title,"profit_margin": float(row.profit_margin), 
                "revenue": row.revenue,"budget": row.budget
            } for row in data
        ]
    def create_movie(self, movie_queries):
        for query in movie_queries:
            try:
                self.db.execute_ddl_and_dml_commands(text(query)) 
            except SQLAlchemyError:
                return  jsonify({"error": "A database error occurred. Please try again later."}), 500
        return  jsonify({"message": "Successful Insert."}), 201


    def get_summary_statistics(self):
        try:
            total_counts_query = text("""
                SELECT 
                    (SELECT COUNT(*) FROM movies) AS total_movies,
                    (SELECT COUNT(*) FROM actors) AS total_actors,
                    (SELECT COUNT(*) FROM directors) AS total_directors,
                    (SELECT COUNT(*) FROM production_companies) AS total_production_companies
            """)
            total_counts_result = self.db.execute_dql_commands(total_counts_query)
            total_counts_data = total_counts_result.fetchone() if total_counts_result else {}
            
            summary = {
                "total_movies": total_counts_data.total_movies,
                "total_actors": total_counts_data.total_actors,
                "total_directors": total_counts_data.total_directors,
                "total_production_companies": total_counts_data.total_production_companies,
            }
            return summary

        except SQLAlchemyError as e:
            print(f"Database error occurred: {e}")
            return jsonify({"error": "A database error occurred. Please try again later."}), 500