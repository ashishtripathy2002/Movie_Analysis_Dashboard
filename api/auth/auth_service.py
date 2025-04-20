from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def register_user(self, email, password):
        # Check if user already exists
        existing_user = self.user_repository.find_user_by_email(email)
        if existing_user:
            return {"error": "User with this email already exists"}, 409

        # Hash password and create a new user
        hashed_password = generate_password_hash(password)
        role_id = 2  # Default role (e.g., "user")
        role_name="guest"
        user_id = self.user_repository.create_user(email, hashed_password, role_id)
        access_token = create_access_token(identity=email, additional_claims={"role": role_name})
        return {
            "access_token": access_token,
            "role": role_name,
            "email": email
        }, 201

    def login_user(self, email, password):
        user_data = self.user_repository.find_user_by_email(email)
        if not user_data:
            return {"error": "Invalid email or password"}, 401
        try:
            user_id, user_email, hashed_password, role_name = user_data
        except ValueError:
            return {"error": "Error: Retrieved user data is incomplete"}, 500

        if not check_password_hash(hashed_password, password):
            return {"error": "Invalid email or password"}, 401
        access_token = create_access_token(identity=email, additional_claims={"role": role_name})
        return {
            "access_token": access_token,
            "role": role_name,
            "email": user_email
        }, 200
