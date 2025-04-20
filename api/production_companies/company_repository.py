from sqlalchemy.sql import text

class ProductionCompanyRepository:
    def __init__(self, db):
        self.db = db

    def get_top_production_companies_by_revenue(self, genres, start_year, end_year, limit):
        # Define the default clauses and parameters
        genre_filter_clause = ""
        having_clause = ""
        params = {
            "start_year": start_year,
            "end_year": end_year,
            "limit": limit
        }

        # If genres are specified, add genre filtering condition and set up the HAVING clause
        if genres:
            genre_filter_clause = "AND g.genre_name IN :genres"
            having_clause = "HAVING COUNT(DISTINCT g.genre_name) = :num_genres"
            params["genres"] = tuple(genres)
            params["num_genres"] = len(genres)
        
        # Add limit clause if limit is provided
        limit_clause = "LIMIT :limit" if limit else ""

        # Define the SQL query
        query = text(f"""
            SELECT 
                pc.company_id, 
                pc.company_name, 
                COALESCE(SUM(m.revenue), 0) AS total_revenue
            FROM 
                production_companies AS pc
            JOIN 
                movie_production_company AS mpc ON pc.company_id = mpc.company_id
            JOIN 
                movies AS m ON mpc.movie_id = m.movie_id
            LEFT JOIN 
                movie_genre AS mg ON m.movie_id = mg.movie_id
            LEFT JOIN 
                genres AS g ON mg.genre_id = g.genre_id
            WHERE 
                m.revenue IS NOT NULL
                AND m.release_year BETWEEN :start_year AND :end_year
                {genre_filter_clause}
            GROUP BY 
                pc.company_id, pc.company_name
            {having_clause}
            ORDER BY 
                total_revenue DESC
            {limit_clause}
        """)
        
        # Execute the query
        result = self.db.execute_dql_commands(query, params)
        data = result.fetchall() if result else []

        # If no data is returned, return an empty list or custom message
        if not data:
            return {"error": "No data available for the specified year range or genres"}

        # Return formatted results
        return [
            {
                "company_id": row.company_id,
                "company_name": row.company_name,
                "total_revenue": int(row.total_revenue)
            }
            for row in data
        ]
