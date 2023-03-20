from flask import Blueprint, request, jsonify

from data import db_session
from data.comments import Comment

blueprint = Blueprint('comments_api', __name__,
                      template_folder='templates')


# API для использования в других приложениях


@blueprint.route('/api/comments')
def get_comments():
    session = db_session.create_session()
    comments = session.query(Comment).all()

    return jsonify(
        {
            'comments':
                [item.to_dict(only=('id', 'text', 'created_date', 'user_id', 'post_id'))
                 for item in comments]
        }
    )


@blueprint.route('/api/comments/<int:comment_id>', methods=['GET'])
def get_one_comment(comment_id):
    session = db_session.create_session()
    comment = session.query(Comment).get(comment_id)

    if not comment:
        return jsonify({'error': 'Not found'})

    return jsonify(
        {
            'comment': comment.to_dict(only=('id', 'text', 'created_date', 'user_id', 'post_id'))
        }
    )


@blueprint.route('/api/comments', methods=['POST'])
def create_comment():
    session = db_session.create_session()

    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ["text", "user_id", "post_id"]):
        return jsonify({'error': 'Bad request'})

    comment = Comment(
        text=request.json['text'],
        user_id=int(request.json['user_id']),
        post_id=int(request.json['post_id'])
    )

    session.add(comment)
    session.commit()

    return jsonify({'success': 'OK'})


@blueprint.route('/api/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    session = db_session.create_session()
    comment = session.query(Comment).get(comment_id)

    if not comment:
        return jsonify({'error': 'Not found'})

    session.delete(comment)
    session.commit()

    return jsonify({'success': 'OK'})


@blueprint.route('/api/comments/<int:comment_id>', methods=['PUT'])
def edit_comment(comment_id):
    session = db_session.create_session()
    comment = session.query(Comment).get(comment_id)

    if not comment:
        return jsonify({'error': 'Not found'})

    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ["text", "user_id", "post_id"]):
        return jsonify({'error': 'Bad request'})

    text = request.json['text']
    user_id = request.json['user_id']
    post_id = request.json['post_id']

    if text:
        comment.text = text
    if user_id:
        comment.user_id = int(user_id)
    if post_id:
        comment.post_id = int(post_id)
