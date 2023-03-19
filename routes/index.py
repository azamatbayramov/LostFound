from flask import render_template
from data import db_session
from data.posts import Post
from . import routes


# Главная страница
@routes.route("/")
def index():
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).filter(Post.is_archived == False).all()
    return render_template("index.html", posts=posts, title="Все посты")


# Страницы с постами про потеряшки
@routes.route("/lost")
def lost():
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).filter(Post.is_archived == False, Post.is_found == False).all()
    return render_template("index.html", posts=posts, title="Потеряно")


# Страницы с постами про найденные вещи
@routes.route("/found")
def found():
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).filter(Post.is_archived == False, Post.is_found == True).all()
    return render_template("index.html", posts=posts, title="Найдено")
