from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from app.models.project import Project, Submission

# Tạo blueprint cho routes chính
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Hiển thị trang chủ
    
    - Hiển thị thông tin giới thiệu về ứng dụng
    
    Returns:
        Template trang chủ
    """
    return render_template('main/index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Hiển thị bảng điều khiển 
    
    - Nếu người dùng là giáo viên, hiển thị danh sách dự án do họ tạo
    - Nếu người dùng là học sinh, hiển thị danh sách dự án có thể nộp bài
    
    Returns:
        Template bảng điều khiển
    """
    if current_user.is_teacher():
        # Lấy tất cả dự án do giáo viên tạo
        projects = Project.query.filter_by(teacher_id=current_user.id).order_by(Project.created_at.desc()).all()
        return render_template('main/teacher_dashboard.html', projects=projects)
    else:
        # Lấy tất cả dự án và bài nộp của học sinh
        projects = Project.query.order_by(Project.deadline.asc()).all()
        
        # Lấy danh sách ID của dự án mà học sinh đã nộp bài
        submitted_project_ids = [s.project_id for s in Submission.query.filter_by(student_id=current_user.id).all()]
        
        return render_template('main/student_dashboard.html', 
                               projects=projects,
                               submitted_project_ids=submitted_project_ids)

@main_bp.route('/submissions')
@login_required
def submissions():
    """Hiển thị danh sách bài nộp
    
    - Nếu người dùng là học sinh, hiển thị danh sách bài nộp của học sinh đó
    - Nếu người dùng là giáo viên, chuyển hướng đến trang dashboard
    
    Returns:
        Template danh sách bài nộp hoặc chuyển hướng
    """
    if current_user.is_student():
        # Lấy tất cả bài nộp của học sinh kèm thông tin dự án
        submissions = (Submission.query
                       .filter_by(student_id=current_user.id)
                       .join(Project, Submission.project_id == Project.id)
                       .order_by(Submission.submitted_at.desc())
                       .all())
        
        return render_template('main/student_submissions.html', submissions=submissions)
    else:
        # Giáo viên không có trang submissions riêng, chuyển hướng về dashboard
        return redirect(url_for('main.dashboard')) 