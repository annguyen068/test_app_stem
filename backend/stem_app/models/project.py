from datetime import datetime
import os
from flask import current_app
from sqlalchemy.orm import relationship, validates
from . import db

class Project(db.Model):
    """Model cho dự án STEM"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)
    deadline = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    submissions = db.relationship('Submission', backref='project', lazy=True, cascade="all, delete-orphan")
    teacher = db.relationship('User', backref=db.backref('teacher_projects', overlaps="author"), 
                             lazy=True, overlaps="projects,author")
    
    def __init__(self, title, description, teacher_id, requirements=None, deadline=None, is_active=True):
        """Khởi tạo dự án mới
        
        Args:
            title: Tiêu đề dự án
            description: Mô tả chi tiết
            teacher_id: ID của giáo viên tạo dự án
            requirements: Yêu cầu của dự án (tùy chọn)
            deadline: Hạn nộp bài (tùy chọn)
            is_active: Trạng thái hoạt động của dự án
        """
        self.title = title
        self.description = description
        self.teacher_id = teacher_id
        self.requirements = requirements
        self.deadline = deadline
        self.is_active = is_active
    
    @validates('title')
    def validate_title(self, key, title):
        """Kiểm tra tính hợp lệ của tiêu đề
        
        Args:
            key: Tên trường (title)
            title: Tiêu đề cần kiểm tra
            
        Returns:
            Title nếu hợp lệ
            
        Raises:
            ValueError: Nếu title không hợp lệ
        """
        if not title or title.strip() == '':
            raise ValueError('Tiêu đề không được để trống')
            
        # Kiểm tra độ dài
        if len(title) < 3:
            raise ValueError('Tiêu đề quá ngắn (tối thiểu 3 ký tự)')
            
        if len(title) > 100:
            raise ValueError('Tiêu đề quá dài (tối đa 100 ký tự)')
            
        return title
    
    @validates('description')
    def validate_description(self, key, description):
        """Kiểm tra tính hợp lệ của mô tả
        
        Args:
            key: Tên trường (description)
            description: Mô tả cần kiểm tra
            
        Returns:
            Description nếu hợp lệ
            
        Raises:
            ValueError: Nếu description không hợp lệ
        """
        if not description or description.strip() == '':
            raise ValueError('Mô tả không được để trống')
            
        if len(description) < 10:
            raise ValueError('Mô tả quá ngắn (tối thiểu 10 ký tự)')
            
        return description
    
    @validates('deadline')
    def validate_deadline(self, key, deadline):
        """Kiểm tra tính hợp lệ của deadline
        
        Args:
            key: Tên trường (deadline)
            deadline: Deadline cần kiểm tra
            
        Returns:
            Deadline nếu hợp lệ
        """
        # Deadline có thể là None (không có hạn nộp)
        if deadline is None:
            return None
            
        return deadline
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'requirements': self.requirements,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'teacher_id': self.teacher_id,
            'submission_count': len(self.submissions)
        }
    
    def check_deadline(self):
        """Kiểm tra xem dự án còn hạn nộp không
        
        Returns:
            True nếu còn hạn nộp, False nếu đã hết hạn
        """
        if not self.deadline:
            return True  # Nếu không có deadline thì luôn còn hạn
        return datetime.utcnow() < self.deadline
    
    def get_submission_by_student(self, student_id):
        """Lấy bài nộp của một học sinh cụ thể
        
        Args:
            student_id: ID của học sinh
            
        Returns:
            Submission object hoặc None nếu không tìm thấy
        """
        return next((sub for sub in self.submissions if sub.student_id == student_id), None)
    
    def __repr__(self):
        """Biểu diễn chuỗi của đối tượng Project
        
        Returns:
            Chuỗi biểu diễn dự án
        """
        return f'<Project {self.title}>' 