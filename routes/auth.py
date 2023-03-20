from flask import render_template, redirect
from flask_login import login_user, logout_user, login_required, current_user
from data import db_session
from data.users import User
from forms.user import RegisterForm, LoginForm
from . import routes


# Регистрация
@routes.route("/register", methods=['GET', 'POST'])
def register():
    # Проверка, авторизован ли пользователь
    if current_user.is_authenticated:
        # Если да, то перенаправляем на главную
        return redirect("/")

    # Создание формы
    form = RegisterForm()

    # Проверка валидности формы
    if form.validate_on_submit():
        # Проверка паролей
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form, message="Пароли не совпадают")

        # Проверка наличия пользователя в БД
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")

        # Создание нового пользователя и добавление его в БД
        user = User(name=form.name.data, email=form.email.data, about=form.about.data)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        # Перенаправление на страницу авторизации
        return redirect('/login')

    # Вывод формы
    return render_template('register.html', title='Регистрация', form=form)


# Авторизация
@routes.route('/login', methods=['GET', 'POST'])
def login():
    # Проверка, авторизован ли пользователь
    if current_user.is_authenticated:
        # Если да, то перенаправляем на главную
        return redirect("/")

    # Создание формы
    form = LoginForm()

    # Проверка валидности формы
    if form.validate_on_submit():
        # Проверка наличия пользователя в БД
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()

        # Проверка пароля
        if user and user.check_password(form.password.data):
            # Авторизация пользователя
            login_user(user, remember=form.remember_me.data)
            # Перенаправление на главную
            return redirect("/")

        # Вывод ошибки
        return render_template('login.html', message="Неправильный логин или пароль", form=form)

    # Вывод формы
    return render_template('login.html', title='Авторизация', form=form)


# Выход
@routes.route('/logout')
@login_required
def logout():
    # Выход из аккаунта
    logout_user()
    # Перенаправление на главную
    return redirect("/")
