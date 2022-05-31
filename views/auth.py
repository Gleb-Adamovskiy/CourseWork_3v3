from flask_restx import Resource, Namespace
from services.auth import AuthService
from services.user import UsersService
from flask import request
from setup_database import db


auth_ns = Namespace('auth')

@auth_ns.route('/login/')
class AuthView(Resource):
    def post(self):
        reg_json = request.json
        email = reg_json.get('email', None)
        user_password = reg_json.get('password', None)
        if None in [email, user_password]:
            return "", 400
        tokens = AuthService(db.session).login(reg_json)
        return tokens, 201

    def put(self):
        reg = request.json['refresh_token']
        if reg is None:
            return "", 400
        return AuthService(db.session).get_new_tokens(reg)

@auth_ns.route('/register/')
class AuthReg(Resource):
    def post(self):
        reg_json = request.json
        UsersService(db.session).create(reg_json)
        return [], 201
