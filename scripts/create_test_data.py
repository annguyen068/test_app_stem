import os
import sys
import random
from datetime import datetime, timedelta

# Thêm thư mục gốc vào PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.user import User
from app.models.project import Project, Submission

def create_test_data():
    """Tạo dữ liệu mẫu cho testing"""
    app = create_app()
    
    with app.app_context():
        # Xóa dữ liệu cũ
        db.drop_all()
        db.create_all()
        
        print("Đang tạo tài khoản giáo viên...")
        teachers = []
        for i in range(2):
            teacher = User(
                username=f'teacher{i+1}',
                email=f'teacher{i+1}@example.com',
                password='password123',
                role='teacher'
            )
            db.session.add(teacher)
            teachers.append(teacher)
        
        print("Đang tạo tài khoản học sinh...")
        students = []
        for i in range(100):
            student = User(
                username=f'student{i+1}',
                email=f'student{i+1}@example.com',
                password='password123',
                role='student'
            )
            db.session.add(student)
            students.append(student)
        
        db.session.commit()
        
        print("Đang tạo các dự án mẫu...")
        projects = []
        project_titles = [
            "Xây dựng robot thu gom rác",
            "Hệ thống tưới cây tự động",
            "Ứng dụng IoT trong nông nghiệp",
            "Thiết kế máy lọc không khí",
            "Robot hỗ trợ người già"
        ]
        
        for teacher in teachers:
            for title in project_titles:
                deadline = datetime.now() + timedelta(days=random.randint(30, 90))
                project = Project(
                    title=f"{title} - {teacher.username}",
                    description=f"Dự án STEM về {title.lower()} do giáo viên {teacher.username} phụ trách",
                    deadline=deadline,
                    teacher_id=teacher.id
                )
                db.session.add(project)
                projects.append(project)
        
        db.session.commit()
        
        print("Đang tạo các bài nộp mẫu...")
        for student in students:
            # Mỗi học sinh nộp bài cho 2-4 dự án ngẫu nhiên
            selected_projects = random.sample(projects, random.randint(2, 4))
            for project in selected_projects:
                submission = Submission(
                    content=f"Bài nộp của {student.username} cho dự án {project.title}",
                    file_path=None,
                    project_id=project.id,
                    student_id=student.id
                )
                
                # 70% bài nộp đã được chấm điểm
                if random.random() < 0.7:
                    submission.score = round(random.uniform(5.0, 10.0), 1)
                    submission.feedback = f"Phản hồi cho bài nộp của {student.username}"
                
                db.session.add(submission)
        
        db.session.commit()
        
        print("\nThống kê dữ liệu đã tạo:")
        print(f"- Số giáo viên: {len(teachers)}")
        print(f"- Số học sinh: {len(students)}")
        print(f"- Số dự án: {len(projects)}")
        print(f"- Số bài nộp: {db.session.query(Submission).count()}")

if __name__ == '__main__':
    create_test_data() 