from utils.api_helpers import make_api_request


BASE_URL = "http://localhost:5000/auth"

class AuthService:
   
    @staticmethod
    def authenticate(email, password):
        response = make_api_request( url=f"{BASE_URL}/login", method="POST",
            data={"email": email, "password": password})
        return response
    
    @staticmethod
    def register(email, password):
        response = make_api_request(
            url= f"{BASE_URL}/register", method="POST",
            data={"email": email,"password": password})
        return response