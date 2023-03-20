from flask import Blueprint, request, jsonify

from data import db_session
from data.posts import Post

blueprint = Blueprint('posts_api', __name__,
                      template_folder='templates')


# API для использования в других приложениях


@blueprint.route('/api/posts')
def get_posts():
    session = db_session.create_session()
    posts = session.query(Post).all()

    return jsonify(
        {
            'posts':
                [item.to_dict(only=('id', 'title', 'content', 'user_id', 'is_private'))
                 for item in posts]
        }
    )


@blueprint.route('/api/posts/<int:post_id>', methods=['GET'])
def get_one_post(post_id):
    session = db_session.create_session()
    post = session.query(Post).get(post_id)

    if not post:
        return jsonify({'error': 'Not found'})

    return jsonify(
        {
            'post': post.to_dict(only=('id', 'title', 'content', 'user_id', 'is_private'))
        }
    )


@blueprint.route('/api/posts', methods=['POST'])
def create_post():
    session = db_session.create_session()

    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ["title", "text", "user_id", "is_found"]):
        return jsonify({'error': 'Bad request'})

    post = Post(
        title=request.json['title'],
        text=request.json['text'],
        user_id=request.json['user_id'],
        is_found=request.json['is_found']

    )

    session.add(post)
    session.commit()

    return jsonify({'success': 'OK'})


@blueprint.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    session = db_session.create_session()
    post = session.query(Post).get(post_id)

    if not post:
        return jsonify({'error': 'Not found'})

    session.delete(post)
    session.commit()

    return jsonify({'success': 'OK'})


@blueprint.route('/api/posts/<int:post_id>', methods=['PUT'])
def edit_post(post_id):
    session = db_session.create_session()
    post = session.query(Post).get(post_id)

    if not post:
        return jsonify({'error': 'Not found'})

    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ["title", "text", "user_id", "is_found"]):
        return jsonify({'error': 'Bad request'})

    title = request.json['title']
    text = request.json['text']
    user_id = request.json['user_id']
    is_found = request.json['is_found']

    if title:
        post.title = title
    if text:
        post.text = text
    if user_id:
        post.user_id = user_id
    if is_found:
        post.is_found = is_found

    session.commit()

    return jsonify({'success': 'OK'})
