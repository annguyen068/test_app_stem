import os
import sys
import tempfile
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from stem_app.models import db, login_manager
from stem_app.config import config

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Load config
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG', 'default')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)
    
    # Cấu hình CORS để cho phép frontend truy cập API
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Cấu hình Flask-Login để trả về lỗi 401 thay vì chuyển hướng
    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({'error': 'Unauthorized access'}), 401
    
    # Xử lý lỗi 404 (Not Found)
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Không tìm thấy tài nguyên yêu cầu'}), 404
    
    # Xử lý lỗi 500 (Internal Server Error)
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"500 error: {str(error)}")
        db.session.rollback()  # Rollback session nếu có lỗi database
        
        # Kiểm tra lỗi liên quan đến database
        error_str = str(error).lower()
        if 'sqlite' in error_str or 'database' in error_str or 'db' in error_str:
            return jsonify({
                'error': 'Lỗi kết nối database',
                'details': str(error),
                'message': 'Không thể kết nối đến database, vui lòng kiểm tra quyền truy cập'
            }), 500
        
        return jsonify({
            'error': 'Lỗi máy chủ nội bộ',
            'details': str(error)
        }), 500
    
    # Xử lý lỗi 405 (Method Not Allowed)
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'error': 'Phương thức không được phép'}), 405
    
    # Register blueprints
    from stem_app.routes.main import main_bp
    from stem_app.routes.auth import auth_bp
    from stem_app.routes.projects import projects_bp
    from stem_app.routes.submissions import submissions_bp
    from stem_app.api import api_bp
    
    app.register_blueprint(main_bp)  # Main blueprint không cần prefix
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(projects_bp, url_prefix='/projects')
    app.register_blueprint(submissions_bp, url_prefix='/submissions')
    app.register_blueprint(api_bp)  # API blueprint đã có prefix '/api'
    
    # Khởi tạo database nếu chưa tồn tại
    with app.app_context():
        try:
            print("Khởi tạo database...")
            
            # Tạo tất cả các bảng
            db.create_all()
            print("Database tables đã được tạo thành công")
            
            # Kiểm tra kết nối database
            from sqlalchemy import text
            result = db.session.execute(text("SELECT 1"))
            print("Kết nối database thành công!")
            
            # Tạo dữ liệu mẫu nếu chưa có
            from stem_app.models.user import User
            from stem_app.models.project import Project
            from datetime import datetime, timedelta
            
            # Kiểm tra xem đã có user nào chưa
            user_count = User.query.count()
            print(f"Số lượng user hiện tại: {user_count}")
            
            if user_count == 0:
                print("Tạo dữ liệu mẫu...")
                
                # Tạo tài khoản giáo viên mẫu
                teacher = User(
                    username='giaovien',
                    email='giaovien@example.com',
                    is_teacher=True
                )
                teacher.set_password('password123')
                
                # Tạo tài khoản học sinh mẫu
                student = User(
                    username='hocsinh',
                    email='hocsinh@example.com',
                    is_teacher=False
                )
                student.set_password('password123')
                
                db.session.add(teacher)
                db.session.add(student)
                db.session.commit()
                
                # Tạo dự án mẫu
                project = Project(
                    title='Dự án STEM mẫu',
                    description='Đây là dự án STEM mẫu để test hệ thống',
                    requirements='Yêu cầu cho dự án STEM mẫu',
                    teacher_id=teacher.id,
                    deadline=datetime.now() + timedelta(days=30),
                    is_active=True
                )
                
                db.session.add(project)
                db.session.commit()
                
                print("Đã tạo dữ liệu mẫu thành công")
            else:
                print("Dữ liệu mẫu đã tồn tại")
            
        except Exception as e:
            print(f"Lỗi khi khởi tạo database: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Nếu lỗi database, thử với in-memory database
            print("Thử sử dụng in-memory database...")
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
            
            try:
                db.create_all()
                print("Đã chuyển sang in-memory database")
            except Exception as e2:
                print(f"Không thể khởi tạo in-memory database: {str(e2)}")
    
    return app 