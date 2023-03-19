from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data import db_session
from data.users import User
from data.posts import Post
from forms.user import RegisterForm, LoginForm
from forms.post import PostForm
from . import routes


@routes.route("/")
def index():
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).filter(Post.is_archived == False).all()
    return render_template("index.html", posts=posts, title="Все посты")


@routes.route("/lost")
def lost():
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).filter(Post.is_archived == False, Post.is_found == False).all()
    return render_template("index.html", posts=posts, title="Потеряно")


@routes.route("/found")
def found():
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).filter(Post.is_archived == False, Post.is_found == True).all()
    return render_template("index.html", posts=posts, title="Найдено")
