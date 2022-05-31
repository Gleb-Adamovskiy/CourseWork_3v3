from dao.models.user import User

class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_by_id(self, uid):
        return self.session.query(User).filter(User.id == uid).first()

    def get_by_email(self, email):
        return self.session.query(User).filter(User.email == email).first()

    def create(self, **kwargs):
        self.session.add(User(**kwargs))
        self.session.commit()

    def delete(self, uid):
        self.session.delete(self.get_by_id(uid))
        self.session.commit()

    def update(self, user_updates):
        user = self.get_by_id(user_updates.get("id"))

        email = user_updates.get("email")
        if email:
            user.email = user_updates.get("email")

        password = user_updates.get("password")
        if password:
            user.password = user_updates.get("password")

        name = user_updates.get("name")
        if name:
            user.name = user_updates.get("name")

        surname = user_updates.get("surname")
        if surname:
            user.surname = user_updates.get("surname")

        favorite_genre = user_updates.get("favorite_genre")
        if favorite_genre:
            user.favorite_genre = user_updates.get("favorite_genre")

        self.session.add(user)
        self.session.commit()
