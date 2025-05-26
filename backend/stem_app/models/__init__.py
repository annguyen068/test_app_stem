from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(id):
    from .user import User
    return User.query.get(int(id))

from stem_app.models.user import User
from stem_app.models.project import Project
from stem_app.models.submission import Submission
from stem_app.models.comment import Comment 