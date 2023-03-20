import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


# Класс для связи постов и изображений
class PostImage(SqlAlchemyBase):
    __tablename__ = 'post_images'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    post_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("posts.id"))
    image_id = sqlalchemy.Column(sqlalchemy.Integer)

    post = orm.relationship("Post")
