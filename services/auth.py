from datetime import datetime, timedelta
import jwt
import hashlib
import base64
from dao.auth import AuthDAO


def hash(password):
    hashed_password = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode('utf-8'),
        salt=base64.b64decode("salt"),
        iterations=100_000,
    )
    return base64.b64encode(hashed_password).decode('utf-8')


def get_tokens(data: dict):
    data['exp'] = datetime.utcnow() + timedelta(minutes=50)
    data['refresh_token'] = False

    access_token = jwt.encode(
        payload=data,
        key="secret_key",
        algorithm='HS256',
    )

    data['exp'] = datetime.utcnow() + timedelta(days=100)
    data['refresh_token'] = True

    refresh_token: str = jwt.encode(
        payload=data,
        key="secret_key",
        algorithm='HS256',
    )

    return {'access_token': access_token, 'refresh_token': refresh_token,}


def decode_token(token: str, refresh_token: bool = False):
    decoded_token = {}
    decoded_token = jwt.decode(
        jwt=token,
        key="secret_key",
        algorithms=['HS256'],
    )

    if decoded_token['refresh_token'] != refresh_token:
        return 'Got wrong token type.'

    return decoded_token


class AuthService:
    def __init__(self, session):
        self.session = session

    def login(self, data: dict):

        user_data = AuthDAO(self.session).get_by_email(data['email'])
        if user_data is None:
            return 'Email not found'

        hash_password = hash(data['password'])
        if user_data['password'] != hash_password:
            return 'Invalid password'

        tokens: dict = get_tokens({'email': data['email']})
        return tokens

    def get_new_tokens(self, refresh_token: str):

        decoded_token = decode_token(refresh_token, refresh_token=True)

        tokens = get_tokens({'email': decoded_token['email']})
        return tokens
