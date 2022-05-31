from flask_restx import Namespace, Resource
from flask import request

from utils import auth_required_data, auth_required_data_patch, auth_change_password

user_ns = Namespace("user")

@user_ns.route("/")
class UserView(Resource):
    @auth_required_data
    def get(self):
        return

    @auth_required_data_patch
    def patch(self):
        req_json = request.json
        return req_json


@user_ns.route("/password/")
class UserPasswordEdit(Resource):
    @auth_change_password
    def put(self):
        req_json = request.json
        return req_json
