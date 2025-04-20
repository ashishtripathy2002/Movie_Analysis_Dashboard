from sqlalchemy.sql import text
from sqlalchemy.exc import SQLAlchemyError
from flask import jsonify


class GenreRepository:
    def __init__(self, db):
        self.db = db

    def get_genre_popularity_revenue_correlation(self):
        try:
            query = text("""
                SELECT g.genre_id, g.genre_name, AVG(m.revenue) AS box_office_revenue,
                       AVG(m.popularity) AS popularity_score,
                       CORR(m.popularity, m.revenue) AS correlation_coefficient
                FROM genres AS g
                JOIN movie_genre AS mg ON g.genre_id = mg.genre_id
                JOIN movies AS m ON mg.movie_id = m.movie_id
                WHERE m.revenue IS NOT NULL AND m.popularity IS NOT NULL
                GROUP BY g.genre_id, g.genre_name
            """)
            result = self.db.execute_dql_commands(query)
            data = result.fetchall() if result else []
            return [
                {
                    "genre_id": row.genre_id,
                    "genre_name": row.genre_name,
                    "box_office_revenue": float(row.box_office_revenue),
                    "popularity_score": float(row.popularity_score),
                    "correlation_coefficient": float(row.correlation_coefficient)
                } for row in data
            ]

        except SQLAlchemyError as e:
            print(f"Database error occurred: {e}")
            return jsonify({"error": "A database error occurred. Please try again later."}), 500


    def get_most_profitable_genres_for_keywords(self, keywords=None):
        if not keywords:
            # If no keywords are specified, return an empty list or handle it as needed
            return {"error": "No keywords specified. Please provide at least one keyword to filter the results."}

        # Prepare the query with keyword conditions
        keywords_placeholder = ', '.join([":keyword" + str(i) for i in range(len(keywords))])

        # Define the query using SQLAlchemy text with a condition that matches all specified keywords
        query = text(f"""
            WITH KeywordMovies AS (
                SELECT m.movie_id,k.keyword_name, m.revenue, m.budget, (m.revenue - m.budget) AS profit
                FROM movies m
                JOIN movie_keyword mk ON m.movie_id = mk.movie_id
                JOIN keywords k ON mk.keyword_id = k.keyword_id
                WHERE k.keyword_name IN ({keywords_placeholder})
                GROUP BY m.movie_id, m.revenue, m.budget, k.keyword_name
            ),
            GenreProfitability AS (
                SELECT g.genre_id, g.genre_name,km.keyword_name, AVG(km.profit) AS avg_profit, SUM(km.profit) AS total_profit
                FROM KeywordMovies km
                JOIN movie_genre mg ON km.movie_id = mg.movie_id
                JOIN genres g ON mg.genre_id = g.genre_id
                GROUP BY g.genre_id, g.genre_name, km.keyword_name
            )
            SELECT genre_id, genre_name,keyword_name, avg_profit, total_profit
            FROM GenreProfitability
            ORDER BY total_profit DESC;
        """)

        # Build the params dictionary dynamically
        params = {f"keyword{i}": keyword for i, keyword in enumerate(keywords)}

        # Execute the query with parameters
        result = self.db.execute_dql_commands(query, params)
        data = result.fetchall() if result else []

        # Format the results for JSON response
        return [
            {
                "genre_id": row.genre_id,
                "genre_name": row.genre_name,
                "keyword_name": row.keyword_name,
                "total_profit": float(row.total_profit)
            } for row in data
        ]

    # def get_most_profitable_genres_for_keywords(self, keywords=None):
    #     # Check if keywords are provided; if not, skip filtering by keywords
    #     if keywords:
    #         keywords_placeholder = ', '.join([":keyword" + str(i) for i in range(len(keywords))])
    #         keyword_filter = f"WHERE k.keyword_name IN ({keywords_placeholder})"
    #         params = {f"keyword{i}": keyword for i, keyword in enumerate(keywords)}
    #     else:
    #         keyword_filter = ""  # No keyword filter
    #         params = {}
    #
    #     # Define the query with the dynamic keyword filter
    #     query = text(f"""
    #         WITH KeywordMovies AS (
    #             SELECT m.movie_id, m.revenue, m.budget, (m.revenue - m.budget) AS profit
    #             FROM movies m
    #             JOIN movie_keyword mk ON m.movie_id = mk.movie_id
    #             JOIN keywords k ON mk.keyword_id = k.keyword_id
    #             {keyword_filter}
    #         ),
    #         GenreProfitability AS (
    #             SELECT g.genre_id, g.genre_name, AVG(km.profit) AS avg_profit, SUM(km.profit) AS total_profit
    #             FROM KeywordMovies km
    #             JOIN movie_genre mg ON km.movie_id = mg.movie_id
    #             JOIN genres g ON mg.genre_id = g.genre_id
    #             GROUP BY g.genre_id, g.genre_name
    #         )
    #         SELECT genre_id, genre_name, avg_profit, total_profit
    #         FROM GenreProfitability
    #         ORDER BY total_profit DESC;
    #     """)
    #
    #     # Execute the query with parameters
    #     result = self.db.execute_dql_commands(query, params)
    #     data = result.fetchall() if result else []
    #
    #     # Format the results for JSON response
    #     return [
    #         {
    #             "genre_id": row.genre_id,
    #             "genre_name": row.genre_name,
    #             "avg_profit": float(row.avg_profit),
    #             "total_profit": float(row.total_profit)
    #         } for row in data
    #     ]

    def get_all_genres(self):
        try:
            query = text("""
                SELECT genre_id, genre_name FROM genres;""")
            result = self.db.execute_dql_commands(query)
            data = result.fetchall() if result else []
            return [
                {
                    "genre_id": row.genre_id,
                    "genre_name": row.genre_name,
                } for row in data
            ]

        except SQLAlchemyError as e:
            print(f"Database error occurred: {e}")
            return jsonify({"error": "A database error occurred. Please try again later."}), 500


    def get_profit_margin_by_genre_and_year(self):
        try:
            query = text("""
                  SELECT 
                        g.genre_id, 
                        g.genre_name, 
                        EXTRACT(YEAR FROM CAST(m.release_date AS DATE)) AS year,  -- Cast release_date to DATE
                        SUM(COALESCE((m.revenue - m.budget) / NULLIF(m.budget, 0), 0)) AS profit_margin
                    FROM 
                        genres AS g
                    JOIN 
                        movie_genre AS mg ON g.genre_id = mg.genre_id
                    JOIN 
                        movies AS m ON mg.movie_id = m.movie_id
                    WHERE 
                        m.budget IS NOT NULL 
                        AND m.revenue IS NOT NULL
                        AND m.release_date IS NOT NULL
                        AND   EXTRACT(YEAR FROM CAST(m.release_date AS DATE)) <2023
                    GROUP BY 
                        g.genre_id, g.genre_name, year
                    ORDER BY 
                        g.genre_name, year;
                        
              """)

            # Execute the query and fetch results
            result = self.db.execute_dql_commands(query)
            data = result.fetchall() if result else []

            # Format the results as a list of dictionaries
            return [
                {
                    "genre_id": row.genre_id,
                    "genre_name": row.genre_name,
                    "year": int(row.year),
                    "profit_margin": float(row.profit_margin)
                } for row in data
            ]

        except SQLAlchemyError as e:
            print(f"Database error occurred: {e}")
            return {"error": "A database error occurred. Please try again later."}
