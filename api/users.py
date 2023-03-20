from flask import Blueprint, request, jsonify

from data import db_session
from data.users import User

blueprint = Blueprint('users_api', __name__,
                      template_folder='templates')


# API для использования в других приложениях


# GET для получения списка пользователей
@blueprint.route('/api/users')
def get_users():
    session = db_session.create_session()
    users = session.query(User).all()

    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email'))
                 for item in users]
        }
    )


# GET для получения одного пользователя
@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'Not found'})

    return jsonify(
        {
            'user': user.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email'))
        }
    )


# POST для создания пользователя
@blueprint.route('/api/users', methods=['POST'])
def create_user():
    session = db_session.create_session()

    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ["name", "email", "password", "about"]):
        return jsonify({'error': 'Bad request'})
    elif session.query(User).filter(User.email == request.json['email']).first():
        return jsonify({'error': 'Id already exists'})

    user = User(
        name=request.json['name'],
        email=request.json['email'],
        about=request.json['about']
    )

    user.set_password(request.json['password'])

    session.add(user)
    session.commit()

    return jsonify({'success': 'OK'})


# DELETE для удаления пользователя
@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'Not found'})

    session.delete(user)
    session.commit()

    return jsonify({'success': 'OK'})


# PUT для редактирования пользователя
@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)

    if not user:
        return jsonify({'error': 'Not found'})

    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ["name", "email", "password", "about"]):
        return jsonify({'error': 'Bad request'})

    if session.query(User).filter(User.email == request.json['email']).first():
        return jsonify({'error': 'Id already exists'})

    name = request.json['name']
    email = request.json['email']
    about = request.json['about']
    password = request.json['password']

    if name:
        user.name = name
    if email:
        user.email = email
    if about:
        user.about = about
    if password:
        user.set_password(password)

    session.commit()

    return jsonify({'success': 'OK'})
