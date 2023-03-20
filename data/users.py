import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import orm


# Модель пользователя для базы данных
class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    posts = orm.relationship("Post", back_populates='user')
    liked_posts = orm.relation("Post", back_populates='liked_users', secondary="liked_users_table")

    comments = orm.relation("Comment", back_populates='user')

    # Установка пароля
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    # Проверка пароля
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
