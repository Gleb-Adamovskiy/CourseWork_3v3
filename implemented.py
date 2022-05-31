from dao.director import DirectorDAO
from dao.genre import GenreDAO
from dao.movie import MovieDAO
from dao.user import UserDAO
from dao.auth import AuthDAO
from services.director import DirectorsService
from services.genre import GenresService
from services.movie import MoviesService
from services.user import UsersService
from services.auth import AuthService
from setup_database import db

director_dao = DirectorDAO(session=db.session)
genre_dao = GenreDAO(session=db.session)
movie_dao = MovieDAO(session=db.session)
user_dao = UserDAO(session=db.session)
auth_dao = AuthDAO(session=db.session)

director_service = DirectorsService(director_dao)
genre_service = GenresService(genre_dao)
movie_service = MoviesService(movie_dao)
user_service = UsersService(user_dao)
auth_service = AuthService(auth_dao)
