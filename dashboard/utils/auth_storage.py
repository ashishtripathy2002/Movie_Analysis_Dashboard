import streamlit as st
#auth_storage.py
import streamlit as st

def set_auth_data(token, role, email):
    """Sets authentication data in Streamlit session state."""
    st.session_state["current_user"] = {"access_token": token, "role": role, "email": email}

def get_auth_headers():
    if "current_user" in st.session_state and "access_token" in st.session_state["current_user"]:
        token = st.session_state["current_user"]["access_token"]
        return {"Authorization": f"Bearer {token}"}
    else:
        return {}

def get_user_role():
    return st.session_state.get("current_user", {}).get("role", "guest")

def is_logged_in():
    return "current_user" in st.session_state and "access_token" in st.session_state["current_user"]


#api_helpers.py
import requests
from utils.auth_storage import get_auth_headers

def make_api_request(url, method="GET", data=None):
    headers = get_auth_headers()
    if method == "GET":
        return requests.get(url, headers=headers)

    elif method == "POST":
        return requests.post(url, json=data, headers=headers)

    elif method == "PUT":
        return requests.put(url, json=data, headers=headers)

    elif method == "DELETE":
        return requests.delete(url, headers=headers)
