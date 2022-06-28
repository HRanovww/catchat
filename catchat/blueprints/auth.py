from flask import Blueprint


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return '<h1>Login Page</h1>'


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return '<h1>Register Page</h1>'
