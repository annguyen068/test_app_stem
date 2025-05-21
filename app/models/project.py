from datetime import datetime
import os
from flask import current_app
from app import db

class Project(db.Model):
    """Mô hình Project đại diện cho dự án STEM
    
    Attributes:
        id: ID duy nhất của dự án
        title: Tiêu đề dự án
        description: Mô tả chi tiết về dự án
        deadline: Hạn nộp bài
        created_at: Thời điểm tạo dự án
        teacher_id: ID của giáo viên tạo dự án
        submissions: Các bài nộp cho dự án này
    """
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    submissions = db.relationship('Submission', backref='project', lazy='dynamic',
                                 cascade='all, delete-orphan')
    
    def __init__(self, title, description, deadline, teacher_id):
        """Khởi tạo dự án mới
        
        Args:
            title: Tiêu đề dự án
            description: Mô tả chi tiết
            deadline: Hạn nộp bài
            teacher_id: ID của giáo viên tạo dự án
        """
        self.title = title
        self.description = description
        self.deadline = deadline
        self.teacher_id = teacher_id
    
    def is_active(self):
        """Kiểm tra xem dự án còn hạn nộp không
        
        Returns:
            True nếu còn hạn nộp, False nếu đã hết hạn
        """
        return datetime.utcnow() < self.deadline
    
    def __repr__(self):
        """Biểu diễn chuỗi của đối tượng Project
        
        Returns:
            Chuỗi biểu diễn dự án
        """
        return f'<Project {self.title}>'


class Submission(db.Model):
    """Mô hình Submission đại diện cho bài nộp của học sinh
    
    Attributes:
        id: ID duy nhất của bài nộp
        content: Mô tả hoặc nội dung bài nộp
        file_path: Đường dẫn đến file đã tải lên
        link: Link đến bài nộp (tùy chọn)
        score: Điểm số bài nộp (None nếu chưa chấm)
        feedback: Phản hồi từ giáo viên (None nếu chưa có)
        submitted_at: Thời điểm nộp bài
        project_id: ID của dự án mà bài nộp thuộc về
        student_id: ID của học sinh nộp bài
    """
    __tablename__ = 'submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(255), nullable=True)
    link = db.Column(db.String(500), nullable=True)
    score = db.Column(db.Float, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, content, file_path, project_id, student_id, link=None):
        """Khởi tạo bài nộp mới
        
        Args:
            content: Mô tả hoặc nội dung bài nộp
            file_path: Đường dẫn đến file đã tải lên
            project_id: ID của dự án
            student_id: ID của học sinh
            link: Link đến bài nộp (tùy chọn)
        """
        self.content = content
        self.file_path = file_path
        self.project_id = project_id
        self.student_id = student_id
        self.link = link
    
    def get_file_name(self):
        """Lấy tên file từ đường dẫn file
        
        Returns:
            Tên file nếu có, None nếu không có file
        """
        if not self.file_path:
            return None
        return os.path.basename(self.file_path)
    
    def is_graded(self):
        """Kiểm tra xem bài nộp đã được chấm điểm chưa
        
        Returns:
            True nếu đã chấm điểm, False nếu chưa
        """
        return self.score is not None
    
    def __repr__(self):
        """Biểu diễn chuỗi của đối tượng Submission
        
        Returns:
            Chuỗi biểu diễn bài nộp
        """
        return f'<Submission {self.id} - Project {self.project_id} - Student {self.student_id}>' 