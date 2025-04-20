# services/metadata_service.py
from utils.api_helpers import make_api_request
import streamlit as st

API_BASE_URL = "http://localhost:5000"

class MetadataService:
    """Service class for fetching metadata from the backend API."""

    @staticmethod
    @st.cache_data
    def fetch_genres():
        """Fetches a list of all genres from the backend."""
        url = f"{API_BASE_URL}/genres"
        response = make_api_request(url)
        return response.json() if response.status_code == 200 else {"error": response.text}

    @staticmethod
    @st.cache_data
    def fetch_keywords():
        """Fetches a list of all keywords from the backend."""
        url = f"{API_BASE_URL}/keywords"
        response = make_api_request(url)
        return response.json() if response.status_code == 200 else {"error": response.text}

    @staticmethod
    # @st.cache_data
    def fetch_summary():
        """Fetches a summary from the backend."""
        url = f"{API_BASE_URL}/summary"
        response = make_api_request(url)
        return response.json() if response.status_code == 200 else {"error": response.text}
