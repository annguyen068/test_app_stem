from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

class User(UserMixin, db.Model):
    """Mô hình User đại diện cho người dùng trong hệ thống
    
    Attributes:
        id: ID duy nhất của người dùng
        username: Tên đăng nhập duy nhất
        email: Địa chỉ email duy nhất
        password_hash: Mật khẩu đã mã hóa
        role: Vai trò (student hoặc teacher)
        created_at: Thời điểm tạo tài khoản
        projects: Các dự án do người dùng tạo (chỉ giáo viên)
        submissions: Các bài nộp do người dùng tạo (chỉ học sinh)
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'student' hoặc 'teacher'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    # Dự án do giáo viên tạo
    projects = db.relationship('Project', backref='teacher', lazy='dynamic',
                              foreign_keys='Project.teacher_id')
    # Bài nộp của học sinh
    submissions = db.relationship('Submission', backref='student', lazy='dynamic',
                                 foreign_keys='Submission.student_id')
    
    def __init__(self, username, email, password, role):
        """Khởi tạo người dùng mới
        
        Args:
            username: Tên đăng nhập
            email: Địa chỉ email
            password: Mật khẩu (chưa mã hóa)
            role: Vai trò (student hoặc teacher)
        """
        self.username = username
        self.email = email
        self.set_password(password)
        self.role = role
    
    def set_password(self, password):
        """Mã hóa và lưu mật khẩu
        
        Args:
            password: Mật khẩu chưa mã hóa
        """
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Kiểm tra mật khẩu
        
        Args:
            password: Mật khẩu cần kiểm tra
            
        Returns:
            True nếu mật khẩu đúng, False nếu sai
        """
        return check_password_hash(self.password_hash, password)
    
    def is_teacher(self):
        """Kiểm tra xem người dùng có phải là giáo viên không
        
        Returns:
            True nếu là giáo viên, False nếu không
        """
        return self.role == 'teacher'
    
    def is_student(self):
        """Kiểm tra xem người dùng có phải là học sinh không
        
        Returns:
            True nếu là học sinh, False nếu không
        """
        return self.role == 'student'
    
    def __repr__(self):
        """Biểu diễn chuỗi của đối tượng User
        
        Returns:
            Chuỗi biểu diễn người dùng
        """
        return f'<User {self.username}, {self.role}>'

@login_manager.user_loader
def load_user(user_id):
    """Tải người dùng dựa trên ID cho Flask-Login
    
    Args:
        user_id: ID của người dùng cần tải
        
    Returns:
        Đối tượng User nếu tìm thấy, None nếu không
    """
    return db.session.get(User, int(user_id)) 