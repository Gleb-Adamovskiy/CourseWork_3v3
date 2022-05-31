from flask_restx import Namespace, Resource
from flask import request
from implemented import movie_service
from setup_database import db

movies_ns = Namespace("movies")

@movies_ns.route("/")
class MoviesView(Resource):
    def get(self):
        data_filter = request.args
        return movie_service(db.session).get_all_movies(data_filter), 200

    def post(self):
        reg_json = request.json
        movie_service(db.session).create(reg_json)
        return [], 201


@movies_ns.route("/<int:id>/")
class MovieView(Resource):
    def get(self, id: int):
        return movie_service(db.session).get_item_by_id(id), 200

    def delete(self, id):
        movie_service(db.session).delete(id)
        return [], 204

    def put(self, id):
        req_json = request.json
        req_json['id'] = id
        movie_service(db.session).update(req_json)
        return [], 204

