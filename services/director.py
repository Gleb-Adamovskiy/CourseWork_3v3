from dao.director import DirectorDAO
from dao.models.director import DirectorSchema


class DirectorsService:
    def __init__(self, session):
        self.session = session

    def get_item_one(self, pk):
        director = DirectorDAO(self.session).get_one(pk)
        return DirectorSchema().dump(director)

    def get_all(self):
        directors = DirectorDAO(self.session)
        return DirectorSchema(many=True).dump(directors.get_all())

    def create(self, director_d):
        return DirectorDAO(self.session).create(director_d)

    def update(self, director_d):
        return DirectorDAO(self.session).update(director_d)

    def delete(self, pk):
        return DirectorDAO(self.session).delete(pk)
