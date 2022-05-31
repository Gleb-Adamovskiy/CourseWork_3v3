import hashlib
import base64
from dao.user import UserDAO
from dao.models.user import UserSchema

def hash(password):
    hashed_password = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode('utf-8'),
        salt=base64.b64decode("salt"),
        iterations=100_000,
    )
    return base64.b64encode(hashed_password).decode('utf-8')

class UsersService:
    def __init__(self, session):
        self.session = session

    def get_item_by_id(self, uid):
        user = UserDAO(self.session).get_by_id(uid)
        return UserSchema().dump(user)

    def update(self, user):
        return UserDAO(self.session).update(user)

    def delete(self, user):
        return UserDAO(self.session).delete(user)

    def get_by_email(self, email):
        user = UserDAO(self.session).get_by_email(email)
        return UserSchema().dump(user)

    def create(self, user):
        user['password'] = hash(user['password'])
        return UserDAO(self.session).create(user)
