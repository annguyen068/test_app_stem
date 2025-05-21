import os
from dotenv import load_dotenv

# Tải biến môi trường từ file .env nếu tồn tại
load_dotenv()

class Config:
    """Lớp cấu hình cho ứng dụng Flask"""
    # Bảo mật
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret_key_change_in_production')
    
    # Cấu hình SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///stem_projects.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Cấu hình upload file
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 10 * 1024 * 1024))  # 10MB 