from flask import Blueprint

# Создание экземпляра класса Blueprint
routes = Blueprint('routes', __name__)

# Импорт всех модулей из папки routes
from .index import *
from .users import *
from .posts import *
from .auth import *
from .comments import *
