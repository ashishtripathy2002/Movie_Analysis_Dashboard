from flask_restful import Resource, reqparse

register_parser = reqparse.RequestParser()
register_parser.add_argument('email', required=True, help="Email is required")
register_parser.add_argument('password', required=True, help="Password is required")

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', required=True, help="Email is required")
login_parser.add_argument('password', required=True, help="Password is required")

class RegisterResource(Resource):
    def __init__(self, user_service):
        self.user_service = user_service

    def post(self):
        args = register_parser.parse_args()
        response, status_code = self.user_service.register_user(args['email'], args['password'])
        return response, status_code

class LoginResource(Resource):
    def __init__(self, user_service):
        self.user_service = user_service

    def post(self):
        args = login_parser.parse_args()
        response, status_code = self.user_service.login_user(args['email'], args['password'])
        return response, status_code
