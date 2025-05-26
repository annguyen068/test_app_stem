from datetime import datetime
from flask_login import UserMixin
import re
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates
from stem_app.models import db

class User(UserMixin, db.Model):
    """Mô hình User đại diện cho người dùng trong hệ thống
    
    Attributes:
        id: ID duy nhất của người dùng
        username: Tên đăng nhập duy nhất
        email: Địa chỉ email duy nhất
        password_hash: Mật khẩu đã mã hóa
        is_teacher: Kiểm tra xem người dùng có phải là giáo viên không
        created_at: Thời điểm tạo tài khoản
        last_seen: Thời điểm cuối cùng người dùng đã truy cập
        projects: Các dự án do người dùng tạo (chỉ giáo viên)
        submissions: Các bài nộp do người dùng tạo (chỉ học sinh)
        comments: Các bình luận do người dùng tạo
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_teacher = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    projects = db.relationship('Project', foreign_keys='Project.teacher_id', 
                              backref='author', lazy='dynamic', 
                              overlaps="teacher_projects,teacher")
    # Submissions relationship được định nghĩa trong model Submission
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    
    def __init__(self, username, email, is_teacher=False):
        """Khởi tạo người dùng mới
        
        Args:
            username: Tên đăng nhập
            email: Địa chỉ email
            is_teacher: True nếu là giáo viên, False nếu là học sinh
        """
        self.username = username
        self.email = email
        self.is_teacher = is_teacher
    
    @validates('email')
    def validate_email(self, key, email):
        """Kiểm tra tính hợp lệ của email
        
        Args:
            key: Tên trường (email)
            email: Địa chỉ email cần kiểm tra
            
        Returns:
            Email nếu hợp lệ
            
        Raises:
            ValueError: Nếu email không hợp lệ
        """
        if not email:
            raise ValueError('Email không được để trống')
        
        # Kiểm tra định dạng email
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValueError('Email không hợp lệ')
            
        # Kiểm tra độ dài
        if len(email) > 120:
            raise ValueError('Email quá dài (tối đa 120 ký tự)')
            
        return email
        
    @validates('username')
    def validate_username(self, key, username):
        """Kiểm tra tính hợp lệ của username
        
        Args:
            key: Tên trường (username)
            username: Tên người dùng cần kiểm tra
            
        Returns:
            Username nếu hợp lệ
            
        Raises:
            ValueError: Nếu username không hợp lệ
        """
        if not username:
            raise ValueError('Username không được để trống')
            
        # Kiểm tra độ dài
        if len(username) < 3:
            raise ValueError('Username quá ngắn (tối thiểu 3 ký tự)')
        
        if len(username) > 64:
            raise ValueError('Username quá dài (tối đa 64 ký tự)')
        
        # Kiểm tra ký tự hợp lệ
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValueError('Username chỉ được chứa chữ cái, số và dấu gạch dưới')
            
        return username
    
    def set_password(self, password):
        """Mã hóa và lưu mật khẩu
        
        Args:
            password: Mật khẩu chưa mã hóa
        """
        if not password or len(password) < 6:
            raise ValueError('Mật khẩu phải có ít nhất 6 ký tự')
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Kiểm tra mật khẩu
        
        Args:
            password: Mật khẩu cần kiểm tra
            
        Returns:
            True nếu mật khẩu đúng, False nếu sai
        """
        return check_password_hash(self.password_hash, password)
    
    def update_last_seen(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
    
    @property
    def is_admin(self):
        return self.is_teacher
    
    def get_projects(self):
        """Get projects based on user role"""
        from stem_app.models.project import Project
        if self.is_teacher:
            return self.projects
        return Project.query.all()
    
    def get_submissions(self):
        """Get submissions based on user role"""
        from stem_app.models.submission import Submission
        from stem_app.models.project import Project
        if self.is_teacher:
            return Submission.query.join(Project).filter(Project.teacher_id == self.id)
        return Submission.query.filter_by(student_id=self.id).all()
    
    def can_submit_to_project(self, project):
        """Check if user can submit to a project"""
        from stem_app.models.submission import Submission
        if self.is_teacher:
            return False
        existing_submission = Submission.query.filter_by(
            project_id=project.id,
            student_id=self.id
        ).first()
        return not existing_submission and project.is_active
    
    def can_edit_project(self, project):
        """Check if user can edit a project"""
        return self.is_teacher and project.teacher_id == self.id
    
    def can_grade_submission(self, submission):
        """Check if user can grade a submission"""
        return self.is_teacher and submission.project.teacher_id == self.id
    
    def to_dict(self):
        """Chuyển đối tượng User thành định dạng dictionary
        
        Returns:
            Dictionary chứa thông tin của người dùng
        """
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'is_teacher': self.is_teacher,
            'created_at': self.created_at.isoformat(),
            'last_seen': self.last_seen.isoformat()
        }
    
    def __repr__(self):
        """Biểu diễn chuỗi của đối tượng User
        
        Returns:
            Chuỗi biểu diễn người dùng
        """
        return f'<User {self.username}>' 