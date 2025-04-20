from sqlalchemy.sql import text
from decimal import Decimal


class DirectorRepository:
    def __init__(self, db):
        self.db = db

    def get_all_directors(self):
        query = text(f"""
               SELECT d.director_id, d.director_name FROM directors AS d""")
        result = self.db.execute_dql_commands(query)
        data = result.fetchall() if result else []
        return [{"director_id": row.director_id, "director_name": row.director_name} for row in data]

    def get_top_directors_by_movie_count(self,sort=None, limit=None):
        """Retrieve top directors with optional sorting and limiting."""
        sort_clause = "ORDER BY number_of_directed_movies DESC" if sort == "number_of_directed_movies" else ""
        query = text(f"""
                   SELECT d.director_id, d.director_name, COUNT(m.movie_id) AS number_of_directed_movies
                   FROM directors AS d
                   LEFT JOIN movie_director AS md ON d.director_id = md.director_id
                   LEFT JOIN movies AS m ON m.movie_id = md.movie_id
                   GROUP BY d.director_id, d.director_name
                   {sort_clause}
                   LIMIT :limit
               """) if limit else text(f"""
                   SELECT d.director_id, d.director_name, COUNT(m.movie_id) AS number_of_directed_movies
                   FROM directors AS d
                   LEFT JOIN movie_director AS md ON d.director_id = md.director_id
                   LEFT JOIN movies AS m ON m.movie_id = md.movie_id
                   GROUP BY d.director_id, d.director_name
                   {sort_clause}
               """)

        params = {'limit': limit} if limit else {}
        result = self.db.execute_dql_commands(query, params)
        data = result.fetchall() if result else []

        return [
            {"director_id": row.director_id,"director_name": row.director_name, "number_of_directed_movies": row.number_of_directed_movies}
            for row in data
        ]


    def get_directors_with_most_top_grossing_movies(self):
        query = text("""
            WITH top_100_grossing AS (
                SELECT movie_id, (revenue-budget) as film_gross FROM movies WHERE revenue IS NOT NULL
                ORDER BY film_gross DESC LIMIT 100
            )
            SELECT d.director_id, d.director_name, COUNT(tg.movie_id) AS num_movies, SUM(tg.film_gross) as total_film_gross
            FROM directors AS d
            JOIN movie_director AS md ON d.director_id = md.director_id
            JOIN top_100_grossing AS tg ON tg.movie_id = md.movie_id
            GROUP BY d.director_id, d.director_name
            ORDER BY num_movies DESC, total_film_gross DESC;  -- Then by total gross revenue

        """)
        result = self.db.execute_dql_commands(query)
        return [{"director_id": row.director_id, "director_name": row.director_name, "num_movies":row.num_movies,"films_gross": row.total_film_gross} for
                row in result.fetchall()]

    def get_director_actor_collaborations(self, sort, limit):
        query = f"""
            SELECT director_name, actor_name, movie_id, original_title,revenue, collaboration_count
            FROM highest_grossing_collaborations
        """
      
        result = self.db.execute_dql_commands(text(query))

        # Format response
        data = result.fetchall() if result else []
        
        # Convert Decimal to float for JSON serialization
        return [
            {
                "director_name": row.director_name,
                "actor_name": row.actor_name,
                "movie_id": row.movie_id,
                "collaboration_count": row.collaboration_count,
                "revenue": float(row.revenue)
            }
            for row in data
        ]
