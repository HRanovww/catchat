from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_moment import Moment
from flask_socketio import SocketIO


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
moment = Moment()
socketio = SocketIO()


@login_manager.user_loader
def load_user(user_id):
    from catchat.models import User
    return User.query.get(int(user_id))


# This is used when the decorator 'login_required' is triggered.
# It helps the decorator find the right page.
login_manager.login_view = 'auth.login'
