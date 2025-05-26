#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script để tạo dữ liệu mẫu cho ứng dụng STEM
"""

from datetime import datetime, timedelta
from stem_app import create_app, db
from stem_app.models.user import User
from stem_app.models.project import Project
from stem_app.models.submission import Submission
from stem_app.models.comment import Comment

def seed_db():
    """Thêm dữ liệu mẫu vào cơ sở dữ liệu"""
    print("Đang tạo dữ liệu mẫu...")
    
    # Tạo tài khoản giáo viên
    teacher = User(username="giaovien", email="giaovien@example.com", is_teacher=True)
    teacher.set_password("password123")
    db.session.add(teacher)
    
    # Tạo tài khoản học sinh
    student1 = User(username="hocsinh1", email="hocsinh1@example.com", is_teacher=False)
    student1.set_password("password123")
    db.session.add(student1)
    
    student2 = User(username="hocsinh2", email="hocsinh2@example.com", is_teacher=False)
    student2.set_password("password123")
    db.session.add(student2)
    
    # Tạo dự án mẫu
    deadline1 = datetime.utcnow() + timedelta(days=30)
    project1 = Project(
        title="Dự án robot tự hành",
        description="Xây dựng một robot có thể tự di chuyển và tránh chướng ngại vật.",
        requirements="1. Robot phải tự di chuyển\n2. Có khả năng phát hiện và tránh chướng ngại vật\n3. Hoạt động ít nhất 30 phút liên tục",
        deadline=deadline1,
        teacher_id=teacher.id
    )
    db.session.add(project1)
    
    deadline2 = datetime.utcnow() + timedelta(days=15)
    project2 = Project(
        title="Ứng dụng học từ vựng tiếng Anh",
        description="Phát triển một ứng dụng web giúp học sinh học từ vựng tiếng Anh hiệu quả.",
        requirements="1. Có ít nhất 500 từ vựng\n2. Có chức năng kiểm tra\n3. Lưu trữ tiến độ học tập",
        deadline=deadline2,
        teacher_id=teacher.id
    )
    db.session.add(project2)
    
    # Commit để lấy ID
    db.session.commit()
    
    # Tạo bài nộp mẫu
    submission1 = Submission(
        content="Em đã hoàn thành robot tự hành sử dụng Arduino và cảm biến siêu âm.",
        project_id=project1.id,
        student_id=student1.id
    )
    submission1.grade = 85
    submission1.feedback = "Bài làm tốt, robot hoạt động ổn định. Cần cải thiện thêm về thời gian hoạt động."
    db.session.add(submission1)
    
    submission2 = Submission(
        content="Em đã phát triển ứng dụng học từ vựng sử dụng React và Flask.",
        project_id=project2.id,
        student_id=student2.id
    )
    db.session.add(submission2)
    
    # Tạo bình luận mẫu
    comment1 = Comment(
        content="Em có thể giải thích thêm về cách robot phát hiện chướng ngại vật không?",
        user_id=teacher.id,
        submission_id=submission1.id
    )
    db.session.add(comment1)
    
    comment2 = Comment(
        content="Em đã sử dụng cảm biến siêu âm HC-SR04 để đo khoảng cách và tránh chướng ngại vật.",
        user_id=student1.id,
        submission_id=submission1.id
    )
    db.session.add(comment2)
    
    # Lưu tất cả thay đổi
    db.session.commit()
    
    print("Đã tạo xong dữ liệu mẫu!")
    print("\nTài khoản mẫu:")
    print("Giáo viên: giaovien@example.com / password123")
    print("Học sinh 1: hocsinh1@example.com / password123")
    print("Học sinh 2: hocsinh2@example.com / password123")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_db() 