from dao.genre import GenreDAO
from dao.models.genre import GenreSchema

class GenresService:
    def __init__(self, session):
        self.session = session

    def get_item_one(self, pk):
        genre = GenreDAO(self.session).get_one(pk)
        return GenreSchema().dump(genre)

    def get_all(self):
        genres = GenreDAO(self.session)
        return GenreSchema(many=True).dump(genres.get_all())

    def create(self, genre_d):
        return GenreDAO(self.session).create(genre_d)

    def update(self, genre_d):
        return GenreDAO(self.session).update(genre_d)

    def delete(self, pk):
        return GenreDAO(self.session).delete(pk)
