import os
import sys
from dotenv import load_dotenv
from datetime import timedelta

# Tải biến môi trường từ file .env nếu tồn tại
try:
    load_dotenv()
except Exception as e:
    print(f"Warning: Could not load .env file: {str(e)}")
    print("Using default environment variables")

# Đường dẫn tuyệt đối đến thư mục gốc của ứng dụng
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')

# Đảm bảo các thư mục tồn tại với quyền đầy đủ
os.makedirs(INSTANCE_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)

print(f"Instance directory: {INSTANCE_DIR}")

class Config:
    """Lớp cấu hình cho ứng dụng Flask"""
    # Bảo mật
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-2024'
    
    # Cấu hình SQLAlchemy - sẽ được override trong init_app
    SQLALCHEMY_DATABASE_URI = 'sqlite:///temp.db'  # Placeholder
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_timeout': 30,
        'pool_recycle': 300,
        'connect_args': {
            'check_same_thread': False,
            'timeout': 30
        }
    }
    
    # Cấu hình upload file
    UPLOAD_FOLDER = UPLOAD_DIR
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'png', 'jpg', 'jpeg'}
    
    # Cấu hình email
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@stem-app.com')
    
    # Cấu hình session
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
    
    # Cấu hình pagination
    POSTS_PER_PAGE = 10 
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-2024'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # CORS Configuration
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']  # Add your frontend URL
    
    @staticmethod
    def init_app(app):
        # Override database URI với absolute path
        if not os.environ.get('DATABASE_URL') or app.config.get('SQLALCHEMY_DATABASE_URI') == 'sqlite:///temp.db':
            db_path = os.path.join(INSTANCE_DIR, 'stem_app.db')
            app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.abspath(db_path)}'
            print(f"✓ Database URI updated to: {app.config['SQLALCHEMY_DATABASE_URI']}")
        else:
            print(f"✓ Using environment DATABASE_URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # Tạo thư mục uploads nếu chưa tồn tại
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Đảm bảo có quyền ghi vào thư mục instance
        try:
            test_file = os.path.join(INSTANCE_DIR, 'test_write.txt')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            print(f"✓ Có quyền ghi vào thư mục instance")
        except Exception as e:
            print(f"✗ Không có quyền ghi vào thư mục instance: {e}")
            raise RuntimeError(f"Không thể ghi vào thư mục instance: {INSTANCE_DIR}")

class DevelopmentConfig(Config):
    DEBUG = True
    
class TestingConfig(Config):
    TESTING = True
    # Sử dụng database riêng cho testing
    TEST_DB_PATH = os.path.join(INSTANCE_DIR, 'test.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.abspath(TEST_DB_PATH)}'
    WTF_CSRF_ENABLED = False
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        print("✓ Initializing testing configuration")

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    
    # Trong production, đảm bảo các biến môi trường được set
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Kiểm tra các biến môi trường bắt buộc
        required_env = ['SECRET_KEY', 'DATABASE_URL', 'JWT_SECRET_KEY']
        for env in required_env:
            if not os.environ.get(env):
                raise RuntimeError(
                    f'ERROR: {env} is not set. '
                    'Set required environment variables before running in production.'
                )
        
        # Bật các tùy chọn bảo mật
        app.config['SESSION_COOKIE_SECURE'] = True
        app.config['REMEMBER_COOKIE_SECURE'] = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 