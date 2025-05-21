import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# Khởi tạo extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    """Hàm factory để tạo và cấu hình ứng dụng Flask
    
    Args:
        config_class: Lớp cấu hình cho ứng dụng
        
    Returns:
        Đối tượng ứng dụng Flask đã cấu hình
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Khởi tạo các extensions với ứng dụng
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Cấu hình login_manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Vui lòng đăng nhập để truy cập trang này.'
    login_manager.login_message_category = 'info'
    
    # Tạo thư mục uploads nếu chưa tồn tại
    os.makedirs(os.path.join(app.root_path, app.config['UPLOAD_FOLDER']), exist_ok=True)
    
    # Đăng ký các blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.projects import projects_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(projects_bp)
    
    # Đăng ký các hàm xử lý lỗi
    from app.routes.errors import handle_404, handle_500
    app.register_error_handler(404, handle_404)
    app.register_error_handler(500, handle_500)
    
    return app

# Import các models để đảm bảo SQLAlchemy biết về chúng
from app.models.user import User
from app.models.project import Project, Submission 