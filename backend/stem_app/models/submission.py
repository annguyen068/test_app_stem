from datetime import datetime
import os
from werkzeug.utils import secure_filename
from flask import current_app
from sqlalchemy.orm import validates
from . import db

class Submission(db.Model):
    """Model cho bài nộp"""
    __tablename__ = 'submissions'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    file_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    score = db.Column(db.Float)
    feedback = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    student = db.relationship('User', foreign_keys=[student_id], backref='student_submissions')
    
    def __init__(self, title, content, project_id, student_id, file_path=None):
        """Khởi tạo bài nộp mới
        
        Args:
            title: Tiêu đề bài nộp
            content: Mô tả hoặc nội dung bài nộp
            file_path: Đường dẫn đến file đã tải lên
            project_id: ID của dự án
            student_id: ID của học sinh
        """
        self.title = title
        self.content = content
        self.project_id = project_id
        self.student_id = student_id
        if file_path:
            self.set_file_path(file_path)
    
    @validates('score')
    def validate_score(self, key, score):
        """Kiểm tra tính hợp lệ của điểm số
        
        Args:
            key: Tên trường (score)
            score: Điểm số cần kiểm tra
            
        Returns:
            Điểm số nếu hợp lệ
            
        Raises:
            ValueError: Nếu điểm số không hợp lệ
        """
        if score is not None:
            if not isinstance(score, (int, float)):
                raise ValueError('Score must be a number')
            if score < 0 or score > 10:
                raise ValueError('Score must be between 0 and 10')
        return score
    
    def set_file_path(self, file_path):
        """Cập nhật đường dẫn file, đảm bảo an toàn
        
        Args:
            file_path: Đường dẫn file gốc
        """
        if file_path:
            filename = secure_filename(os.path.basename(file_path))
            self.file_path = os.path.join('uploads', str(self.project_id), filename)
    
    def get_absolute_file_path(self):
        """Lấy đường dẫn tuyệt đối đến file
        
        Returns:
            Đường dẫn tuyệt đối hoặc None nếu không có file
        """
        if not self.file_path:
            return None
        return os.path.join(current_app.config['UPLOAD_FOLDER'], self.file_path)
    
    def delete_file(self):
        """Xóa file vật lý nếu tồn tại"""
        if self.file_path:
            try:
                file_path = self.get_absolute_file_path()
                if os.path.exists(file_path):
                    os.remove(file_path)
                self.file_path = None
            except Exception as e:
                current_app.logger.error(f"Error deleting file {self.file_path}: {str(e)}")
    
    def to_dict(self):
        """Chuyển đối tượng thành dictionary
        
        Returns:
            Dictionary chứa thông tin bài nộp
        """
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'file_path': self.file_path,
            'file_name': self.get_file_name(),
            'submitted_at': self.submitted_at.isoformat(),
            'score': self.score,
            'feedback': self.feedback,
            'project_id': self.project_id,
            'student_id': self.student_id
        }
    
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
        return f'<Submission {self.id} for Project {self.project_id}>' 