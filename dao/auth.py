from dao.models.user import User

class AuthDAO:
    def __init__(self, session):
        self.session = session

    def get_by_email(self, email):
        users = self.session.query(User)

        if email:
            users = users.filter(User.email == email).one()
            data = {
                'email': users.email,
                'role': users.role,
                'password': users.password,
            }
            return data
        return None
