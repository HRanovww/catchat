from flask import Blueprint


chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/')
def home():
    return '<h1>the home page. A bunch of messages will be listed here.</h1>'


@chat_bp.route('/profile/<user_id>')
def get_profile(user_id):
    return '<h1>The profile of user %s.</h1>' % user_id
