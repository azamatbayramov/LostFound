from flask import render_template, redirect, request, abort
from flask_login import login_required, current_user
from data import db_session
from data.users import User
import os
from data.posts import Post
from data.post_images import PostImage
from forms.post import PostForm, AddPhotoForm, PostEditForm
from . import routes


# Функция добавления фото к посту
def add_photo(post, file):
    # Получаем id последнего фото и добавляем к нему 1
    filenames_list = os.listdir(path='static/img/post_img')
    last_photo_id = int(filenames_list[-1].split('.')[0]) if filenames_list else -1
    new_photo_id = last_photo_id + 1

    # Добавляем фото в папку и к посту
    db_sess = db_session.create_session()
    post.images.append(PostImage(image_id=new_photo_id))
    db_sess.merge(post)
    db_sess.commit()
    file.save(f'static/img/post_img/{new_photo_id}.jpg')


# Хэндлер добавления поста
@routes.route('/add_post', methods=['GET', 'POST'])
@login_required
def add_post():
    # Создаем форму
    form = PostForm()

    # Если форма валидна
    if form.validate_on_submit():
        # Создаем сессию
        db_sess = db_session.create_session()
        file = form.image.data

        # Проверяем, что фото в формате .jpg
        if file:
            if file.filename.split('.')[-1] not in ['jpg', 'jpeg']:
                return render_template('add_post.html', form=form,
                                       error='Фото должно быть формата .jpg')

        # Создаем пост
        post = Post()

        # Заполняем пост данными из формы
        post.title = form.title.data
        post.text = form.text.data
        post.is_found = form.is_found.data
        post.user_id = current_user.id

        # Добавляем фотографию к посту или просто добавляем пост
        if file:
            add_photo(post, file)
        else:
            db_sess.merge(post)
            db_sess.commit()

        # Редиректим на главную страницу
        return redirect('/')

    # Если форму не отправили, то просто отображаем ее
    return render_template('add_post.html', title='Добавление поста',
                           form=form)


# Хэндлер добавления фото к посту
@routes.route('/add_photo_to_post/<int:id>', methods=['GET', 'POST'])
@login_required
def add_photo_to_post(id):
    # Создаем форму
    form = AddPhotoForm()

    # Если форма валидна
    if form.validate_on_submit():

        # Получаем файл из формы и проверяем, что он в формате .jpg
        file = form.image.data
        if file:
            if file.filename.split('.')[-1] not in ['jpg', 'jpeg']:
                return render_template('add_photo.html', form=form,
                                       errors=['Фото должно быть формата .jpg'])

        # Создаем сессию
        db_sess = db_session.create_session()

        # Получаем пост
        post = db_sess.query(Post).filter(Post.id == id, Post.user == current_user).first()

        # Если пост не найден, то возвращаем 404
        if not post:
            abort(404)

        # Добавляем фото к посту или просто сохраняем пост
        if file:
            add_photo(post, file)
        else:
            db_sess.merge(post)
            db_sess.commit()

        # Редиректим на страницу поста
        return redirect(f'/posts/{id}')

    # Если форму не отправили, то просто отображаем ее
    return render_template('add_photo.html', form=form, title='Добавление фото')


# Хэндлер редактирования поста
@routes.route('/edit_post/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
    # Создаем форму
    form = PostEditForm()

    # Создаем сессию и получаем пост
    db_sess = db_session.create_session()
    post = db_sess.query(Post).filter(Post.id == id, Post.user == current_user).first()

    # Если пост не найден, то возвращаем 404
    if not post:
        abort(404)

    # Заполняем пост данными из формы
    if form.validate_on_submit():
        if form.title.data:
            post.title = form.title.data
        if form.text.data:
            post.text = form.text.data
        if form.is_found.data:
            post.is_found = form.is_found.data
        # Сохраняем пост
        db_sess.commit()
        # Редиректим на страницу поста
        return redirect(f'/posts/{id}')

    # Если форму не отправили, то просто отображаем ее
    return render_template('edit_post.html', title='Редактирование поста', form=form)


# Хэндлер удаления фото из поста
@routes.route('/delete_photo_from_post', methods=['GET', 'POST'])
@login_required
def delete_photo_from_post():
    # Получаем аргументы из запроса
    args = request.args
    id = int(args['id'])
    photo_id = int(args['image_id'])
    back_url = args['back_url']

    # Создаем сессию и получаем пост
    db_sess = db_session.create_session()
    post = db_sess.query(Post).filter(Post.id == id, Post.user == current_user).first()

    # Если пост не найден, то возвращаем 404
    if not post:
        abort(404)

    # Удаляем фото из поста
    for photo in post.images:
        if photo.image_id == photo_id:
            print('Hey')
            os.remove(f'static/img/post_img/{photo.image_id}.jpg')
            db_sess.delete(photo)
            db_sess.commit()
            break

    # Редиректим на страницу поста
    return redirect(back_url)


# Хэндлер удаления поста
@routes.route('/delete_post', methods=['GET', 'POST'])
@login_required
def delete_post():
    # Получаем аргументы из запроса
    args = request.args
    id = int(args['id'])
    back_url = args['back_url']

    # Создаем сессию и получаем пост
    db_sess = db_session.create_session()
    post = db_sess.query(Post).filter(Post.id == id, Post.user == current_user).first()

    # Если пост не найден, то возвращаем 404
    if not post:
        abort(404)

    # Удаляем фото из поста
    for photo in post.images:
        os.remove(f'static/img/post_img/{photo.image_id}.jpg')
        db_sess.delete(photo)

    # Удаляем пост
    db_sess.delete(post)

    # Сохраняем изменения
    db_sess.commit()

    # Редиректим на обратную страницу
    return redirect(back_url)


# Хэндлер страницы поста
@routes.route("/posts/<int:id>")
def post_page(id):
    # Создаем сессию и получаем пост
    db_sess = db_session.create_session()
    post = db_sess.query(Post).filter(Post.id == id).first()

    # Если пост не найден, то возвращаем 404
    if not post:
        abort(404)

    # Возвращаем страницу поста
    return render_template("post_page.html", post=post, post_page=True)


# Хэндлер архивации поста
@routes.route("/archive_post")
@login_required
def archive_post():
    # Получаем аргументы из запроса
    args = request.args
    id = int(args['id'])
    back_url = args['back_url']
    archive = args['archive']

    # Создаем сессию и получаем пост
    db_sess = db_session.create_session()
    post = db_sess.query(Post).filter(Post.id == id, Post.user == current_user).first()

    # Если пост не найден, то возвращаем 404
    if not post:
        abort(404)

    # Архивируем/разархивируем пост
    if archive == 'off':
        post.is_archived = False
    else:
        post.is_archived = True

    # Сохраняем изменения
    db_sess.commit()

    # Редиректим на обратную страницу
    return redirect(back_url)


# Хэндлер лайка поста
@routes.route('/set_like', methods=['GET', 'POST'])
@login_required
def set_like():
    # Получаем аргументы из запроса
    args = request.args
    id = int(args['id'])
    back_url = args['back_url']
    like = args['like']

    # Создаем сессию и получаем пост
    db_sess = db_session.create_session()
    post = db_sess.query(Post).filter(Post.id == id).first()
    user = db_sess.query(User).filter(User.id == current_user.id).first()

    # Если пост не найден, то возвращаем 404
    if not post:
        abort(404)

    # Ставим/убираем лайк
    if like == 'off':
        post.liked_users.remove(user)
    else:
        post.liked_users.append(user)

    # Сохраняем изменения
    db_sess.commit()

    # Редиректим на обратную страницу
    return redirect(back_url)
