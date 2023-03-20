from flask import render_template, redirect, abort
from flask_login import logout_user, login_required, current_user
from data import db_session
from data.users import User
from forms.user import EditForm, ChangePasswordForm, ChangeAvatarForm
from . import routes
import os


# Пользовательские страницы
@routes.route("/my")
@routes.route("/my/")
@login_required
def my_page():
    # Перенаправление на страницу пользователя
    return redirect(f"/users/{current_user.id}")


# Пользовательские страницы
@routes.route("/users/<int:id>")
@routes.route("/users/<int:id>/")
def user_page(id):
    # Получаем пользователя из БД
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(id)

    # Если пользователя нет, то возвращаем 404
    if not user:
        abort(404)

    # Возвращаем страницу пользователя
    return render_template("user_page.html", user=user)


# Удаление аккаунта
@routes.route("/delete_account")
@login_required
def delete_account():
    # Получаем пользователя из БД
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()

    # Если пользователя нет, то возвращаем 404
    if not user:
        abort(404)

    # Удаляем посты и фотографии
    for post in user.posts:
        for photo in post.images:
            if f"{photo.image_id}.jpg" in os.listdir('static/img/post_img'):
                os.remove(f'static/img/post_img/{photo.image_id}.jpg')
            db_sess.delete(photo)
        db_sess.delete(post)

    # Удаляем пользователя
    db_sess.delete(user)

    # Сохраняем изменения
    db_sess.commit()

    # Выходим из аккаунта
    logout_user()

    # Возвращаем на главную
    return redirect("/")


# Редактирование аккаунта
@routes.route("/edit_account", methods=["GET", "POST"])
@login_required
def edit_account():
    # Создаем форму
    form = EditForm()

    # Если форма отправлена
    if form.validate_on_submit():
        # Получаем пользователя из БД
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()

        # Если пользователя нет, то возвращаем 404
        if not user:
            abort(404)

        # Изменяем данные
        if form.name.data:
            user.name = form.name.data
        if form.email.data:
            user.email = form.email.data
        if form.about.data:
            user.about = form.about.data

        # Сохраняем изменения
        db_sess.commit()

        # Возвращаем на страницу пользователя
        return redirect(f"/users/{current_user.id}")

    # Возвращаем страницу редактирования
    return render_template("edit_account.html", title="Редактирование аккаунта", form=form)


# Смена пароля
@routes.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    # Создаем форму
    form = ChangePasswordForm()

    # Если форма отправлена
    if form.validate_on_submit():
        # Получаем пользователя из БД
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == current_user.id).first()

        # Если пользователя нет, то возвращаем 404
        if not user:
            abort(404)

        # Проверяем пароли
        if not form.new_password_again.data == form.new_password.data:
            return render_template("change_password.html", title="Смена пароля", form=form,
                                   message="Пароли не совпадают")

        if not user.check_password(form.password.data):
            return render_template("change_password.html", title="Смена пароля", form=form,
                                   message="Неверный пароль")

        # Изменяем пароль
        user.set_password(form.new_password.data)

        # Сохраняем изменения
        db_sess.commit()

        # Возвращаем на страницу пользователя
        return redirect(f"/users/{current_user.id}")

    # Возвращаем страницу смены пароля
    return render_template("change_password.html", title="Смена пароля", form=form)


# Смена аватара
@routes.route("/change_avatar", methods=["GET", "POST"])
@login_required
def change_avatar():
    # Создаем форму
    form = ChangeAvatarForm()

    # Если форма отправлена
    if form.validate_on_submit():
        # Получаем файл
        file = form.image.data

        # Проверяем файл на формат
        if file:
            if file.filename.split('.')[-1] not in ['jpg', 'jpeg']:
                return render_template('add_photo.html', form=form,
                                       errors=['Фото должно быть формата .jpg'])

        # Сохраняем файл
        file.save(f'static/img/user_img/{current_user.id}.jpg')

        # Возвращаем на страницу пользователя
        return redirect(f"/users/{current_user.id}")

    # Возвращаем страницу смены аватара
    return render_template("add_photo.html", title="Смена аватара", form=form)


# Удаление аватара
@routes.route("/delete_avatar", methods=["GET", "POST"])
@login_required
def delete_avatar():
    # Удаляем файл аватара пользователя, если он есть
    if f"{current_user.id}.jpg" in os.listdir("static/img/user_img"):
        os.remove(f"static/img/user_img/{current_user.id}.jpg")

    # Возвращаем на страницу пользователя
    return redirect(f"/users/{current_user.id}")
