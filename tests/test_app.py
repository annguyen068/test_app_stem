import os
import sys
import pytest
import tempfile
import datetime
from flask import Flask
from werkzeug.security import generate_password_hash

# Thêm thư mục gốc của dự án vào đường dẫn
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User
from app.models.project import Project, Submission
from config import Config

class TestConfig(Config):
    """Cấu hình cho việc kiểm thử"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

@pytest.fixture
def app():
    """Tạo và cấu hình ứng dụng Flask cho kiểm thử"""
    app = create_app(TestConfig)
    
    # Tạo context ứng dụng
    with app.app_context():
        # Tạo tất cả các bảng trong cơ sở dữ liệu
        db.create_all()
        
        # Tạo dữ liệu mẫu cho kiểm thử
        # Tạo người dùng giáo viên
        teacher = User(
            username='teacher_test',
            email='teacher@example.com',
            password='password123',
            role='teacher'
        )
        
        # Tạo người dùng học sinh
        student = User(
            username='student_test',
            email='student@example.com',
            password='password123',
            role='student'
        )
        
        db.session.add(teacher)
        db.session.add(student)
        db.session.commit()
        
        # Tạo dự án mẫu
        project = Project(
            title='Dự án STEM mẫu',
            description='Đây là dự án mẫu để kiểm thử',
            deadline=datetime.datetime.now() + datetime.timedelta(days=7),
            teacher_id=teacher.id
        )
        
        db.session.add(project)
        db.session.commit()
        
        yield app
        
        # Dọn dẹp sau khi kiểm thử
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Tạo client kiểm thử"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Tạo runner cho các lệnh CLI"""
    return app.test_cli_runner()

def test_trang_chu(client):
    """Kiểm tra trang chủ hoạt động đúng"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Qu\xe1\xba\xa3n l\xc3\xbd D\xe1\xbb\xb1 \xc3\xa1n STEM' in response.data

def test_dang_ky(client):
    """Kiểm tra chức năng đăng ký người dùng"""
    # Dữ liệu form đăng ký
    data = {
        'username': 'new_user',
        'email': 'new_user@example.com',
        'password': 'password123',
        'confirm_password': 'password123',
        'role': 'student'
    }
    
    # Gửi request POST đến route đăng ký
    response = client.post('/auth/register', data=data, follow_redirects=True)
    
    # Kiểm tra kết quả
    assert response.status_code == 200
    
    # Kiểm tra xem người dùng đã được tạo trong cơ sở dữ liệu chưa
    user = User.query.filter_by(username='new_user').first()
    assert user is not None
    assert user.email == 'new_user@example.com'
    assert user.role == 'student'

def test_dang_nhap(client):
    """Kiểm tra chức năng đăng nhập"""
    # Dữ liệu form đăng nhập
    login_data = {
        'username': 'teacher_test',
        'password': 'password123'
    }
    
    # Gửi request POST đến route đăng nhập
    response = client.post('/auth/login', data=login_data, follow_redirects=True)
    
    # Kiểm tra kết quả
    assert response.status_code == 200
    assert b'Dashboard' in response.data or b'B\xe1\xba\xa3ng \xc4\x91i\xe1\xbb\x81u khi\xe1\xbb\x83n' in response.data

def test_tao_du_an(app, client):
    """Kiểm tra chức năng tạo dự án (yêu cầu đăng nhập giáo viên)"""
    # Đăng nhập với tài khoản giáo viên
    client.post('/auth/login', data={
        'username': 'teacher_test',
        'password': 'password123'
    })
    
    # Dữ liệu form tạo dự án
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)
    project_data = {
        'title': 'Dự án kiểm thử mới',
        'description': 'Mô tả dự án kiểm thử',
        'deadline': tomorrow.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Gửi request POST đến route tạo dự án
    response = client.post('/projects/create', data=project_data, follow_redirects=True)
    
    # Kiểm tra kết quả
    assert response.status_code == 200
    
    # Kiểm tra xem dự án đã được tạo trong cơ sở dữ liệu chưa
    with app.app_context():
        project = Project.query.filter_by(title='Dự án kiểm thử mới').first()
        assert project is not None
        assert project.description == 'Mô tả dự án kiểm thử'

def test_nop_bai(app, client):
    """Kiểm tra chức năng nộp bài (yêu cầu đăng nhập học sinh)"""
    # Đăng nhập với tài khoản học sinh
    client.post('/auth/login', data={
        'username': 'student_test',
        'password': 'password123'
    })
    
    # Lấy ID dự án mẫu đã tạo
    with app.app_context():
        project = Project.query.first()
        project_id = project.id
    
    # Dữ liệu form nộp bài
    submission_data = {
        'content': 'Nội dung bài nộp kiểm thử',
    }
    
    # Gửi request POST đến route nộp bài
    response = client.post(f'/projects/{project_id}/submit', data=submission_data, follow_redirects=True)
    
    # Kiểm tra kết quả
    assert response.status_code == 200
    
    # Kiểm tra xem bài nộp đã được tạo trong cơ sở dữ liệu chưa
    with app.app_context():
        submission = Submission.query.filter_by(project_id=project_id).first()
        assert submission is not None
        assert submission.content == 'Nội dung bài nộp kiểm thử'

def test_cham_diem(app, client):
    """Kiểm tra chức năng chấm điểm (yêu cầu đăng nhập giáo viên và có bài nộp)"""
    # Tạo bài nộp trước (cần có cả thông tin học sinh và dự án)
    with app.app_context():
        student = User.query.filter_by(username='student_test').first()
        project = Project.query.first()
        
        submission = Submission(
            content='Nội dung bài nộp mẫu',
            file_path=None,
            project_id=project.id,
            student_id=student.id
        )
        
        db.session.add(submission)
        db.session.commit()
        
        submission_id = submission.id
    
    # Đăng nhập với tài khoản giáo viên
    client.post('/auth/login', data={
        'username': 'teacher_test',
        'password': 'password123'
    })
    
    # Dữ liệu form chấm điểm
    grade_data = {
        'score': 8.5,
        'feedback': 'Phản hồi từ giáo viên cho bài nộp'
    }
    
    # Gửi request POST đến route chấm điểm
    response = client.post(f'/projects/submissions/{submission_id}/grade', data=grade_data, follow_redirects=True)
    
    # Kiểm tra kết quả
    assert response.status_code == 200
    
    # Kiểm tra xem điểm đã được cập nhật trong cơ sở dữ liệu chưa
    with app.app_context():
        updated_submission = db.session.get(Submission, submission_id)
        assert updated_submission is not None
        assert updated_submission.score == 8.5
        assert updated_submission.feedback == 'Phản hồi từ giáo viên cho bài nộp'

def test_xem_du_an(app, client):
    """Kiểm tra xem chi tiết dự án"""
    # Đăng nhập với tài khoản giáo viên
    client.post('/auth/login', data={
        'username': 'teacher_test',
        'password': 'password123'
    })
    
    # Lấy ID dự án mẫu
    with app.app_context():
        project = Project.query.first()
        project_id = project.id
    
    # Gửi request GET đến route xem dự án
    response = client.get(f'/projects/{project_id}')
    
    # Kiểm tra kết quả
    assert response.status_code == 200
    assert b'Chi ti\xe1\xba\xbft d\xe1\xbb\xb1 \xc3\xa1n' in response.data

def test_xem_bai_nop(app, client):
    """Kiểm tra xem chi tiết bài nộp"""
    # Tạo bài nộp trước (cần có cả thông tin học sinh và dự án)
    with app.app_context():
        student = User.query.filter_by(username='student_test').first()
        project = Project.query.first()
        
        submission = Submission(
            content='Nội dung bài nộp mẫu',
            file_path=None,
            project_id=project.id,
            student_id=student.id
        )
        
        db.session.add(submission)
        db.session.commit()
        
        submission_id = submission.id
    
    # Đăng nhập với tài khoản học sinh
    client.post('/auth/login', data={
        'username': 'student_test',
        'password': 'password123'
    })
    
    # Gửi request GET đến route xem bài nộp
    response = client.get(f'/projects/submissions/{submission_id}')
    
    # Kiểm tra kết quả
    assert response.status_code == 200
    assert b'Chi ti\xe1\xba\xbft b\xc3\xa0i n\xe1\xbb\x99p' in response.data 