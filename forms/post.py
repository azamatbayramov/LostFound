from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired


# Форма для создания поста
class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    text = TextAreaField("Содержание")
    is_found = BooleanField("Найдено")
    image = FileField("Фотография")
    submit = SubmitField('Создать')


# Форма для редактирования поста
class PostEditForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    text = TextAreaField("Содержание")
    is_found = BooleanField("Найдено")
    submit = SubmitField('Создать')


# Форма для добавления фотографии
class AddPhotoForm(FlaskForm):
    image = FileField("Фотография")
    submit = SubmitField('Добавить')
