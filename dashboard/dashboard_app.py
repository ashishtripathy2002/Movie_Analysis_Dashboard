import streamlit as st
import time
from streamlit_option_menu import option_menu
from components.data_analytics import render_analytics_dashboard
from components.movie_mngt import movie_mgmt
from services.metadata_service import MetadataService
from services.auth_service import AuthService
from utils.auth_storage import set_auth_data
import re

# Configure the page settings
st.set_page_config(page_title="Movie Analyser", page_icon=":popcorn:", layout="wide")


## session state to see if user is logged in or not
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
##session state for current page....to track current page
if 'page' not in st.session_state:
    st.session_state['page'] = 'login'
##Session state for current user info
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = {"access_token": "", "email": "", "role": ""}


def register(email, password, error_container):
    validate_user(email, password,error_container)
    response = AuthService.register(email, password)
    if response.status_code == 201:
        data = response.json()
        set_auth_data(data["access_token"], data["role"], email)
        st.session_state['logged_in'] = True
        st.session_state['page'] = 'dashboard'
        st.success("Account created successfully!")
    else:
        error_message = response.json().get("error", "Registration failed. Please try again.")
        show_temporary_message(error_message, error_container)

def show_temporary_message(message, container, duration=3):
    container.error(message)
    time.sleep(duration)
    container.empty()

def logout():
    st.session_state['logged_in'] = False
    st.session_state['page'] = 'login'
    st.session_state['current_user'] = {}

def validate_user(email, password, error_container):
    if len(password) < 6:
        error_container.error("Password must be at least 6 characters long.")
        return
    EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(EMAIL_REGEX, email):
        error_container.error("Please enter a valid email address.")
        return
    
def login(email, password, error_container):
    validate_user(email, password,error_container)
    ##GET API to check if entered user exists or not
    response = AuthService.authenticate(email, password)
    if response.status_code == 200:
        data = response.json()
        set_auth_data(data["access_token"], data["role"], email)
        st.toast("Login successful!")
        return True
    else:
        ##response: {"error": "Invalid email or password"}
        error_message = response.json().get("error", "Login failed. Please try again.")
        st.error(error_message)
        return False

def login_setup(): 
        login_successful = login(st.session_state.email_input, st.session_state.password_input,st.empty())
        # Update session state if login was successful
        if login_successful:
            st.session_state.logged_in = True
            st.session_state['page'] = 'dashboard'

def auth_page(): 
    st.title("Welcome to Movie Analyser")
    st.write("Please log in or register to access the dashboard.")
    ##tab for login and register option
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1: # Login form
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        st.session_state.email_input = email
        st.session_state.password_input = password
        st.button('Login', on_click=login_setup)

    
    with tab2: # Registration form
        st.subheader("Register")
        error_container = st.empty() 
        with st.form(key="register_form"):
            email = st.text_input("Email", key="register_email")
            password = st.text_input("Password", type="password", key="register_password")
            confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
            submit_register = st.form_submit_button("Create my account")

            if submit_register:
                if password != confirm_password:
                    show_temporary_message("Passwords do not match.", error_container)
                else:
                    register(email, password, error_container)

def dashboard():
    with st.sidebar:
        menu_options = ["Home",  "Manage Data"]
        menu_icons = ["house", "database"]
    

        selected = option_menu(
            "Navigation",
            menu_options,
            icons=menu_icons,
            menu_icon="cast",
            default_index=0,
            orientation="vertical",
            styles={
                "container": {"padding": "0!important", "background-color": "#f0f2f6"},
                "icon": {"color": "blue", "font-size": "20px"},
                "nav-link": {
                    "color": "black",
                    "font-size": "18px",
                    "text-align": "left",
                    "margin": "5px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#007bff", "color": "white"},
            }
        )

        if st.button("Logout", on_click=logout):
            pass

    if selected == "Home":
        st.title("Movie Analysis")
        summary_data = MetadataService.fetch_summary()
        if summary_data:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Movies", summary_data.get("total_movies", 0))
            col2.metric("Actors", summary_data.get("total_actors", 0))
            col3.metric("Directors", summary_data.get("total_directors", 0))
            col4.metric("Production Companies", summary_data.get("total_production_companies", 0))
        else:
            st.warning("Failed to load summary statistics.")
        render_analytics_dashboard()

    elif selected == "Manage Data":
        st.title("Manage Data")
        movie_mgmt()

    elif selected == "Account":
        st.title("Account Settings")
        st.text(f"Email: {st.session_state['current_user'].get('email', '')}")


def main():
    if st.session_state['logged_in']:
        dashboard()
    else:
        auth_page()

if __name__ == "__main__":
    main()