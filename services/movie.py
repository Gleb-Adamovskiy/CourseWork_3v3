from dao.movie import MovieDAO
from dao.models.movie import MovieSchema

class MoviesService:
    def __init__(self, session):
        self.session = session

    def get_item_by_id(self, pk):
        movie = MovieDAO(self.session).get_one(pk)
        return MovieSchema().dump(movie)

    def get_all_movies(self):
        movies = MovieDAO(self.session)
        return MovieSchema(many=True).dump(movies.get_all())

    def create(self, movie_d):
        return MovieDAO(self.session).create(movie_d)

    def update(self, movie_d):
        return MovieDAO(self.session).update(movie_d)

    def delete(self, pk):
        return MovieDAO(self.session).delete(pk)
