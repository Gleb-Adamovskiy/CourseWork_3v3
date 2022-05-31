import base64
import hashlib
import jwt
from dao.auth import AuthDAO
from dao.user import UserDAO
from setup_database import db
from flask import request


def get_token_from_head(headers):
    if 'Authorization' not in headers:
        return 404
    return headers['Authorization'].split(' ')[-1]


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


def hash(password):
    hashed_password = hashlib.pbkdf2_hmac(
        hash_name='sha256',
        password=password.encode('utf-8'),
        salt=base64.b64decode("salt"),
        iterations=100_000,
    )
    return base64.b64encode(hashed_password).decode('utf-8')


def auth_required_data(func):
    def wrap(*args, **kwargs):
        token = get_token_from_head(request.headers)
        decoded_token = decode_token(token)
        if not AuthDAO(db.session).get_by_email(decoded_token['email']):
            return 404
        result = UserDAO(db.session).get_by_email(decoded_token['email'])
        data = {'email': result.email, 'name': result.name, 'surname': result.surname}
        return data
    return wrap


def auth_required_data_patch(func):
    def wrapper(*args, **kwargs):
        token = get_token_from_head(request.headers)
        decoded_token = decode_token(token)
        if not AuthDAO(db.session).get_by_email(decoded_token['email']):
            return 404
        result = UserDAO(db.session).get_by_email(decoded_token['email'])
        new_data = func(*args, **kwargs)
        data = {'id': result.id, 'name': new_data["name"], 'surname': new_data["surname"]}
        UserDAO(db.session).update(data)
        return [], 204
    return wrapper


def auth_change_password(func):
    def wrapper(*args, **kwargs):
        token = get_token_from_head(request.headers)
        decoded_token = decode_token(token)
        if not AuthDAO(db.session).get_by_email(decoded_token['email']):
            return 404
        result = UserDAO(db.session).get_by_email(decoded_token['email'])
        current_password = result.password
        new_data_password = func(*args, **kwargs)
        temp_password = hash(new_data_password['old_password'])
        if current_password != temp_password:
            return 401
        temp_password = hash(new_data_password['new_password'])
        data = {'id': result.id, 'password': temp_password}
        UserDAO(db.session).update(data)
        return [], 204
    return wrapper