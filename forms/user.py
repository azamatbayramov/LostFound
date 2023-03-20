from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, FileField
from wtforms.validators import DataRequired


# Форма регистрации
class RegisterForm(FlaskForm, ):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')


# Форма входа
class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])

    remember_me = BooleanField('Запомнить меня')

    submit = SubmitField('Войти')


# Форма редактирования профиля
class EditForm(FlaskForm):
    email = EmailField('Почта')
    name = StringField('Имя пользователя')
    about = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')


# Форма смены пароля
class ChangePasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    new_password = PasswordField('Повторите пароль', validators=[DataRequired()])
    new_password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


# Форма смены аватара
class ChangeAvatarForm(FlaskForm):
    image = FileField('Фото', validators=[DataRequired()])
    submit = SubmitField('Сменить')
