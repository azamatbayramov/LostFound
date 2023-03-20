from flask import Flask
from flask_login import LoginManager

from routes import *

# Создание приложения и подключение роутов
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.register_blueprint(routes)

# Создание менеджера для аутентификации
login_manager = LoginManager()


# Функция для загрузки пользователя
@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()

    return db_sess.query(User).get(user_id)


# Функция для запуска приложения
def main():
    login_manager.init_app(app)
    db_session.global_init("db/database.sqlite")
    app.run(port=80)


# Запуск приложения
if __name__ == '__main__':
    main()
