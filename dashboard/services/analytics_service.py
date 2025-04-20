# analytics_service.py
from utils.api_helpers import make_api_request
import streamlit as st
BASE_URL = "http://localhost:5000"

class AnalyticsService:
    @st.cache_data
    @staticmethod
    def get_top_directors(limit=5):
        url = f"{BASE_URL}/directors?sort=number_of_directed_movies&limit={limit}"
        response = make_api_request(url)
        return response.json() if response.status_code == 200 else {"error": response.text}

    @st.cache_data
    @staticmethod
    def get_top_profit_margin_movies(limit=5):
        url = f"{BASE_URL}/movies?sort=profit_margin&limit={limit}"
        response = make_api_request(url)
        return response.json() if response.status_code == 200 else {"error": response.text}

    @st.cache_data
    @staticmethod
    def get_directors_top_grossing(limit=100):
        url = f"{BASE_URL}/directors/top_grossing?limit={limit}"
        response = make_api_request(url)
        return response.json() if response.status_code == 200 else {"error": response.text}

    @st.cache_data
    @staticmethod
    def get_highest_avg_vote_actors_by_genre(genre=None,limit=100):
        url = f"{BASE_URL}/actors?genre={genre}&sort=avg_vote&limit={limit}"
        if genre is None or genre==genre.strip()=="":
            url = f"{BASE_URL}/actors?sort=avg_vote&limit={limit}"
        response = make_api_request(url)
        return response.json() if response.status_code == 200 else {"error": response.text}

    
    @staticmethod
    def get_director_actor_collaborations(limit=100):
        url = f"{BASE_URL}/directors/collaborations?sort=highest_grossing&limit={limit}"
        response = make_api_request(url)
        return response.json() if response.status_code == 200 else {"error": response.text}

    @st.cache_data
    @staticmethod
    def get_genre_popularity_revenue_correlation():
        url = f"{BASE_URL}/genres/popularity_revenue_correlation"
        response = make_api_request(url)
        return response.json() if response.status_code == 200 else {"error": response.text}

    @st.cache_data
    @staticmethod
    def get_highest_rating_diff_actors_between_2_genres(genre1='drama', genre2='comedy'):
        url = f"{BASE_URL}/actors/genre_rating_difference?genre1={genre1}&genre2={genre2}"
        response = make_api_request(url)
        return response.json() if response.status_code == 200 else {"error": response.text}

    @st.cache_data
    @staticmethod
    def get_top_production_companies_by_revenue(genres, start_year=None, end_year=None, limit=5):
        url = f"{BASE_URL}/production_companies?sort=total_revenue&limit={limit}"
        if genres:
            genre_param = ','.join(genres)
            url += f"&genres={genre_param}"
        if start_year:
            url += f"&start_year={start_year}"
        if end_year:
            url += f"&end_year={end_year}"
        response = make_api_request(url)
        return response.json() if response.status_code == 200 else {"error": response.text}


    @st.cache_data
    @staticmethod
    def get_actors_with_high_rated_appearances(limit,min_rating=8):
        url = f"{BASE_URL}/actors/high_rated_appearances?min_rating={min_rating}&limit={limit}"
        response = make_api_request(url)
        return response.json() if response.status_code == 200 else {"error": response.text}

    @st.cache_data
    @staticmethod
    def get_most_profitable_genres_with_sequels_prequels(keywords):
        print(keywords)
        url = f"{BASE_URL}/genres/profitable_movies?keywords={','.join(keywords)}"
        response = make_api_request(url)
        return response.json() if response.status_code == 200 else {"error": response.text}

    @st.cache_data
    @staticmethod
    def get_profit_margin_by_genre_and_year():
        url = f"{BASE_URL}/genres/profit_margin"  # Hypothetical endpoint for profit margin by genre
        response = make_api_request(url)
        return response.json() if response.status_code == 200 else {"error": response.text}
