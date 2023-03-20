from flask import render_template, abort, redirect
from flask_login import current_user, login_required
from data import db_session
from data.posts import Post
from . import routes
from data.comment import Comment
from forms.comment import CommentForm


# Добавление комментария
@routes.route('/add_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def add_comment(id):
    # Получаем пост, к которому добавляется комментарий
    db_sess = db_session.create_session()
    post = db_sess.query(Post).filter(Post.id == id).first()

    # Если пост не найден, возвращаем 404
    if not post:
        abort(404)

    # Создаем форму
    form = CommentForm()

    # Если форма заполнена и валидна, добавляем комментарий
    if form.validate_on_submit():
        # Получаем текст комментария
        text = form.text.data

        # Если текст пустой, возвращаем форму с сообщением об ошибке
        if not text:
            return render_template("add_comment.html", form=form, message="Введите текст комментария")

        # Создаем комментарий
        comment = Comment(text=text)
        comment.user_id = current_user.id
        comment.post_id = post.id

        # Добавляем комментарий в сессию
        db_sess.add(comment)

        # Сохраняем изменения
        db_sess.commit()

        # Перенаправляем на страницу поста
        return redirect(f"/posts/{post.id}")

    # Возвращаем форму
    return render_template("add_comment.html", form=form, title="Добавление комментария")


# Редактирование комментария
@routes.route('/edit_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_comment(id):
    # Создаем форму
    form = CommentForm()

    # Получаем комментарий
    db_sess = db_session.create_session()
    comment = db_sess.query(Comment).filter(Comment.id == id, Comment.user == current_user).first()

    # Если комментарий не найден, возвращаем 404
    if not comment:
        abort(404)

    # Если форма заполнена и валидна, редактируем комментарий
    if form.validate_on_submit():
        # Получаем текст комментария
        text = form.text.data

        # Если текст пустой, возвращаем форму с сообщением об ошибке
        if not text:
            return render_template("add_comment.html", form=form, message="Введите текст комментария",
                                   title="Редактирование комментария")

        # Редактируем комментарий
        comment.text = text

        # Сохраняем изменения
        db_sess.commit()

        # Перенаправляем на страницу поста
        return redirect(f"/posts/{comment.post_id}")

    # Возвращаем форму
    return render_template("add_comment.html", form=form, title="Редактирование комментария")


# Удаление комментария
@routes.route('/delete_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_comment(id):
    # Получаем комментарий
    db_sess = db_session.create_session()
    comment = db_sess.query(Comment).filter(Comment.id == id, Comment.user == current_user).first()

    # Если комментарий не найден, возвращаем 404
    if not comment:
        abort(404)

    # Удаляем комментарий и сохраняем изменения
    db_sess.delete(comment)
    db_sess.commit()

    # Перенаправляем на страницу поста
    return redirect(f"/posts/{comment.post_id}")
