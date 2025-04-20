from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

class ActorRepository:
    def __init__(self, db):
        self.db = db
    def get_all_actors(self):
        try:
            query = text("""SELECT actor_id, actor_name FROM actors;""")
            result = self.db.execute_dql_commands(query)
            return [{"actor_id": row.actor_id, "actor_name": row.actor_name} for row in result.fetchall()]
        except SQLAlchemyError as e:
            print(f"Database error occurred: {e}")
            return jsonify({"error": "A database error occurred. Please try again later."}), 500

    def get_actors_with_highest_avg_vote(self, sort, genre=None, limit=100):
        # Set the sorting clause based on the sort parameter
        sort_clause = "ORDER BY avg_vote DESC" if sort == "avg_vote" else ""

        # Set the genre filter clause only if a genre is specified
        genre_filter = "WHERE LOWER(g.genre_name) = LOWER(:genre)" if genre else ""

        # Define the query with optional genre filter
        query = text(f"""
            SELECT a.actor_id, a.actor_name, AVG(m.vote_count) AS avg_vote
            FROM actors AS a
            JOIN movie_actor AS ma ON a.actor_id = ma.actor_id
            JOIN movies AS m ON ma.movie_id = m.movie_id
            JOIN movie_genre AS mg ON m.movie_id = mg.movie_id
            JOIN genres AS g ON mg.genre_id = g.genre_id
            {genre_filter}
            GROUP BY a.actor_id, a.actor_name
            {sort_clause}
            LIMIT :limit
        """)

        # Prepare parameters for the query
        parameters = {'limit': limit}
        if genre:
            parameters['genre'] = genre

        # Execute the query with the correct parameters
        result = self.db.execute_dql_commands(query, parameters)

        # Handle the case where the result is None
        if result is None:
            return []  # Return an empty list if no results are found

        # Return the result as a list of dictionaries
        return [
            {"actor_id": row.actor_id, "actor_name": row.actor_name, "avg_vote": float(row.avg_vote)}
            for row in result.fetchall()
        ]

    def get_actors_rating_difference_between_genres(self, genre1, genre2, limit):
        query = text("""
            WITH genre1_ratings AS (
                SELECT a.actor_id, a.actor_name, AVG(m.vote_average) AS avg_genre1_rating
                FROM actors AS a
                JOIN movie_actor AS ma ON a.actor_id = ma.actor_id
                JOIN movies AS m ON ma.movie_id = m.movie_id
                JOIN movie_genre AS mg ON m.movie_id = mg.movie_id
                JOIN genres AS g ON mg.genre_id = g.genre_id
                WHERE LOWER(g.genre_name) = :genre1
                GROUP BY a.actor_id, a.actor_name
            ),
            genre2_ratings AS (
                SELECT a.actor_id, a.actor_name, AVG(m.vote_average) AS avg_genre2_rating
                FROM actors AS a
                JOIN movie_actor AS ma ON a.actor_id = ma.actor_id
                JOIN movies AS m ON ma.movie_id = m.movie_id
                JOIN movie_genre AS mg ON m.movie_id = mg.movie_id
                JOIN genres AS g ON mg.genre_id = g.genre_id
                WHERE LOWER(g.genre_name) = :genre2
                GROUP BY a.actor_id, a.actor_name
            )
            SELECT g1.actor_id, g1.actor_name, ABS(g1.avg_genre1_rating - g2.avg_genre2_rating) AS rating_difference
            FROM genre1_ratings g1
            JOIN genre2_ratings g2 ON g1.actor_id = g2.actor_id
            ORDER BY rating_difference DESC
            LIMIT :limit
        """)
        result = self.db.execute_dql_commands(query, {'genre1': genre1.lower(), 'genre2': genre2.lower(), 'limit': limit})
        return [{"actor_id": row.actor_id, "actor_name": row.actor_name, "rating_difference": float(row.rating_difference)} for row in result.fetchall()]

    def get_actors_with_most_high_rated_appearances(self, min_rating=8, limit=100):
        query = text("""
            SELECT a.actor_id, a.actor_name, COUNT(*) AS high_rated_appearances
            FROM actors AS a
            JOIN movie_actor AS ma ON a.actor_id = ma.actor_id
            JOIN movies AS m ON ma.movie_id = m.movie_id
            WHERE m.vote_average >= :min_rating
            GROUP BY a.actor_id, a.actor_name
            ORDER BY high_rated_appearances DESC
            LIMIT :limit
        """)
        result = self.db.execute_dql_commands(query, {'min_rating': min_rating, 'limit': limit})
        return [{"actor_id": row.actor_id, "actor_name": row.actor_name, "high_rated_appearances": row.high_rated_appearances} for row in result.fetchall()]
