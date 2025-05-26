from datetime import datetime
from . import db

class Comment(db.Model):
    """Model cho bình luận của người dùng"""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    submission_id = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    
    def __init__(self, content, user_id, submission_id):
        """Khởi tạo bình luận mới
        
        Args:
            content: Nội dung bình luận
            user_id: ID của người bình luận
            submission_id: ID của bài nộp được bình luận
        """
        self.content = content
        self.user_id = user_id
        self.submission_id = submission_id
    
    def to_dict(self):
        """Chuyển đối tượng thành dictionary
        
        Returns:
            Dictionary chứa thông tin bình luận
        """
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'user_id': self.user_id,
            'submission_id': self.submission_id
        }
    
    def __repr__(self):
        """Biểu diễn chuỗi của đối tượng Comment
        
        Returns:
            Chuỗi biểu diễn bình luận
        """
        return f'<Comment {self.id} by User {self.user_id}>' 