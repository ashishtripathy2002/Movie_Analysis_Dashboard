from utils.api_helpers import make_api_request
import streamlit as st
BASE_URL = "http://localhost:5000"  # Replace with the actual base URL

class MovieService:
    # @st.cache_data
    @staticmethod
    def create_movie(data):
        url = f"{BASE_URL}/movies"
        response = make_api_request(url, method="POST", json=data)
        return response.json() if response.status_code == 201 else {"error": response.text}

    # @st.cache_data
    @staticmethod
    def update_movie(movie_id, data):
        url = f"{BASE_URL}/movies/{movie_id}"
        response = make_api_request(url, method="PUT", data=data)
        return response.json() if response.status_code == 200 else {"error": response.text}

    # @st.cache_data
    @staticmethod
    def delete_movie(movie_id):
        url = f"{BASE_URL}/movies/{movie_id}"
        response = make_api_request(url, method="DELETE")
        return response.json() if response.status_code == 200 else {"error": response.text}

    @st.cache_data
    @staticmethod
    def get_movie_details(movie_id):
        url = f"{BASE_URL}/movies/{movie_id}"
        response = make_api_request(url)
        response = make_api_request(url)
        return response.json() if response.status_code == 200 else {"error": response.text}


    @staticmethod
    def get_all_movies(page=1, per_page=10, sort=None, filter=None):
        url = f"{BASE_URL}/movies?page={page}&per_page={per_page}"
        if sort:
            url += f"&sort={sort}"
        if filter:
            url += f"&filter={filter}"
        response = make_api_request(url)
        return response.json() if response.status_code == 200 else {"error": response.text}
