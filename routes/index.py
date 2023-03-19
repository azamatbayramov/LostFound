from flask import render_template
from data import db_session
from data.posts import Post
from . import routes


# Главная страница
@routes.route("/")
def index():
    # Получаем все посты из базы данных
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).filter(Post.is_archived == False).all()

    # Возвращаем шаблон с постами
    return render_template("index.html", posts=posts, title="Все посты")


# Страницы с постами про потеряшки
@routes.route("/lost")
def lost():
    # Получаем все посты с потеряшками из базы данных
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).filter(Post.is_archived == False, Post.is_found == False).all()

    # Возвращаем шаблон с постами
    return render_template("index.html", posts=posts, title="Потеряно")


# Страницы с постами про найденные вещи
@routes.route("/found")
def found():
    # Получаем все посты с найденными вещами из базы данных
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).filter(Post.is_archived == False, Post.is_found == True).all()

    # Возвращаем шаблон с постами
    return render_template("index.html", posts=posts, title="Найдено")
