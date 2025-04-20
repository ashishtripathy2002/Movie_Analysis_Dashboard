from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

from auth.auth_resource import RegisterResource, LoginResource
from auth.auth_service import AuthService
from config import Config
from database import PostgresqlDB
from routes import Routes
from user.user_repository import UserRepository

from datetime import timedelta
# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
app.config['API_TITLE'] = 'My Movie Analysis API'
app.config['API_VERSION'] = 'v1'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change to your actual secret key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)  # Token valid for 24 hours


# Initialize JWT
jwt = JWTManager(app)

api = Api(app)
routes = Routes(app)
app = routes.get_app()

# # Error handler example
@app.errorhandler(404)
def page_not_found(e):
    return {"error": str(e)}, 404

# Main entry point
if __name__ == "__main__":
    app.run(debug=True)