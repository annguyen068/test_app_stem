from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_file, abort
from flask_login import current_user, login_required
import os
from datetime import datetime

from app import db
from app.models.project import Project, Submission
from app.utils.forms import ProjectForm, SubmissionForm, GradeForm
from app.utils.file_utils import save_file, get_file_path, delete_file

# Tạo blueprint cho routes liên quan đến dự án
projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

# Utility function
def check_teacher_permission(project_id):
    """Kiểm tra xem người dùng hiện tại có quyền truy cập dự án không
    
    Args:
        project_id: ID của dự án cần kiểm tra
        
    Returns:
        Project object nếu có quyền, None nếu không
    """
    project = Project.query.get_or_404(project_id)
    
    if not current_user.is_teacher() or project.teacher_id != current_user.id:
        abort(403)  # Forbidden
    
    return project

@projects_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Tạo dự án mới (chỉ dành cho giáo viên)
    
    - GET: Hiển thị form tạo dự án
    - POST: Xử lý tạo dự án mới
    
    Returns:
        Template tạo dự án hoặc chuyển hướng đến dashboard
    """
    # Chỉ giáo viên mới có thể tạo dự án
    if not current_user.is_teacher():
        flash('Chỉ giáo viên mới có thể tạo dự án.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    form = ProjectForm()
    
    if form.validate_on_submit():
        try:
            project = Project(
                title=form.title.data,
                description=form.description.data,
                deadline=form.deadline.data,
                teacher_id=current_user.id
            )
            
            db.session.add(project)
            db.session.commit()
            
            flash('Dự án đã được tạo thành công!', 'success')
            return redirect(url_for('main.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Có lỗi xảy ra: {str(e)}', 'danger')
    
    return render_template('projects/create.html', form=form)

@projects_bp.route('/<int:project_id>')
@login_required
def view(project_id):
    """Xem chi tiết dự án
    
    - Hiển thị thông tin chi tiết về dự án
    - Nếu là giáo viên và sở hữu dự án, hiển thị danh sách các bài nộp
    - Nếu là học sinh, hiển thị form nộp bài hoặc bài nộp đã tồn tại
    
    Args:
        project_id: ID của dự án cần xem
        
    Returns:
        Template chi tiết dự án
    """
    project = Project.query.get_or_404(project_id)
    
    if current_user.is_teacher():
        # Kiểm tra xem giáo viên có phải là người tạo dự án
        if project.teacher_id != current_user.id:
            flash('Bạn không có quyền xem dự án này.', 'danger')
            return redirect(url_for('main.dashboard'))
        
        # Lấy tất cả bài nộp cho dự án
        submissions = (Submission.query
                       .filter_by(project_id=project.id)
                       .order_by(Submission.submitted_at.desc())
                       .all())
        
        return render_template('projects/view_teacher.html', project=project, submissions=submissions)
    else:
        # Tìm bài nộp của học sinh hiện tại cho dự án này (nếu có)
        submission = Submission.query.filter_by(
            project_id=project.id, 
            student_id=current_user.id
        ).first()
        
        # Nếu học sinh chưa nộp và dự án còn hạn, hiển thị form nộp bài
        if not submission and project.is_active():
            form = SubmissionForm()
            return render_template('projects/view_student.html', 
                                  project=project, 
                                  submission=None, 
                                  form=form)
        
        # Nếu học sinh đã nộp hoặc dự án hết hạn, chỉ hiển thị thông tin
        return render_template('projects/view_student.html', 
                              project=project, 
                              submission=submission)

@projects_bp.route('/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(project_id):
    """Chỉnh sửa dự án (chỉ dành cho giáo viên sở hữu dự án)
    
    - GET: Hiển thị form chỉnh sửa với thông tin hiện tại
    - POST: Xử lý cập nhật dự án
    
    Args:
        project_id: ID của dự án cần chỉnh sửa
        
    Returns:
        Template chỉnh sửa dự án hoặc chuyển hướng
    """
    project = check_teacher_permission(project_id)
    
    form = ProjectForm(obj=project)
    
    if form.validate_on_submit():
        try:
            project.title = form.title.data
            project.description = form.description.data
            project.deadline = form.deadline.data
            
            db.session.commit()
            
            flash('Dự án đã được cập nhật thành công!', 'success')
            return redirect(url_for('projects.view', project_id=project.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Có lỗi xảy ra: {str(e)}', 'danger')
    
    return render_template('projects/edit.html', form=form, project=project)

@projects_bp.route('/<int:project_id>/delete', methods=['POST'])
@login_required
def delete(project_id):
    """Xóa dự án (chỉ dành cho giáo viên sở hữu dự án)
    
    - POST: Xử lý xóa dự án và các bài nộp liên quan
    
    Args:
        project_id: ID của dự án cần xóa
        
    Returns:
        Chuyển hướng đến dashboard
    """
    project = check_teacher_permission(project_id)
    
    try:
        # Lấy tất cả bài nộp liên quan để xóa file
        submissions = Submission.query.filter_by(project_id=project.id).all()
        
        # Xóa các file bài nộp từ hệ thống file
        for submission in submissions:
            if submission.file_path:
                delete_file(submission.file_path)
        
        # Xóa dự án (và tất cả bài nộp do cascade)
        db.session.delete(project)
        db.session.commit()
        
        flash('Dự án đã được xóa thành công!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Có lỗi xảy ra khi xóa dự án: {str(e)}', 'danger')
    
    return redirect(url_for('main.dashboard'))

@projects_bp.route('/<int:project_id>/submit', methods=['POST'])
@login_required
def submit(project_id):
    """Nộp bài cho dự án (chỉ dành cho học sinh)
    
    - POST: Xử lý nộp bài mới
    
    Args:
        project_id: ID của dự án cần nộp bài
        
    Returns:
        Chuyển hướng đến trang chi tiết dự án
    """
    # Chỉ học sinh mới có thể nộp bài
    if not current_user.is_student():
        flash('Chỉ học sinh mới có thể nộp bài.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    project = Project.query.get_or_404(project_id)
    
    # Kiểm tra xem dự án còn hạn nộp không
    if not project.is_active():
        flash('Dự án đã hết hạn nộp bài.', 'danger')
        return redirect(url_for('projects.view', project_id=project.id))
    
    # Kiểm tra xem học sinh đã nộp bài cho dự án này chưa
    existing_submission = Submission.query.filter_by(
        project_id=project.id, 
        student_id=current_user.id
    ).first()
    
    if existing_submission:
        flash('Bạn đã nộp bài cho dự án này rồi.', 'warning')
        return redirect(url_for('projects.view', project_id=project.id))
    
    form = SubmissionForm()
    
    if form.validate_on_submit():
        try:
            # Kiểm tra xem có file hoặc link không
            if not form.file.data and not form.link.data:
                flash('Vui lòng nộp file hoặc cung cấp link.', 'danger')
                return redirect(url_for('projects.view', project_id=project.id))
            
            # Lưu file (nếu có)
            file_path = None
            if form.file.data:
                # Kiểm tra kích thước file (100MB)
                if len(form.file.data.read()) > 100 * 1024 * 1024:
                    flash('File không được vượt quá 100MB.', 'danger')
                    return redirect(url_for('projects.view', project_id=project.id))
                form.file.data.seek(0)  # Reset con trỏ file
                file_path = save_file(form.file.data)
                if not file_path:
                    flash('Có lỗi xảy ra khi lưu file.', 'danger')
                    return redirect(url_for('projects.view', project_id=project.id))
            
            # Tạo bài nộp mới
            submission = Submission(
                content=form.content.data,
                file_path=file_path,
                link=form.link.data,
                project_id=project.id,
                student_id=current_user.id
            )
            
            db.session.add(submission)
            db.session.commit()
            
            flash('Bài nộp đã được gửi thành công!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Có lỗi xảy ra: {str(e)}', 'danger')
    else:
        # Hiển thị lỗi từ form
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{error}', 'danger')
    
    return redirect(url_for('projects.view', project_id=project.id))

@projects_bp.route('/submissions/<int:submission_id>')
@login_required
def view_submission(submission_id):
    """Xem chi tiết bài nộp
    
    - Hiển thị thông tin chi tiết về bài nộp
    - Nếu là giáo viên, hiển thị form chấm điểm (nếu chưa chấm)
    
    Args:
        submission_id: ID của bài nộp cần xem
        
    Returns:
        Template chi tiết bài nộp
    """
    submission = Submission.query.get_or_404(submission_id)
    project = Project.query.get_or_404(submission.project_id)
    
    # Kiểm tra quyền xem bài nộp
    if current_user.is_teacher():
        # Giáo viên chỉ có thể xem bài nộp của dự án do họ tạo
        if project.teacher_id != current_user.id:
            flash('Bạn không có quyền xem bài nộp này.', 'danger')
            return redirect(url_for('main.dashboard'))
        
        # Nếu bài nộp chưa được chấm điểm, hiển thị form chấm điểm
        form = None
        if submission.score is None:
            form = GradeForm()
        
        return render_template('projects/view_submission_teacher.html', 
                              submission=submission, 
                              project=project, 
                              form=form)
    else:
        # Học sinh chỉ có thể xem bài nộp của chính mình
        if submission.student_id != current_user.id:
            flash('Bạn không có quyền xem bài nộp này.', 'danger')
            return redirect(url_for('main.dashboard'))
        
        return render_template('projects/view_submission_student.html', 
                              submission=submission, 
                              project=project)

@projects_bp.route('/submissions/<int:submission_id>/grade', methods=['POST'])
@login_required
def grade_submission(submission_id):
    """Chấm điểm bài nộp (chỉ dành cho giáo viên)
    
    - POST: Xử lý chấm điểm và phản hồi
    
    Args:
        submission_id: ID của bài nộp cần chấm điểm
        
    Returns:
        Chuyển hướng đến trang chi tiết bài nộp
    """
    # Chỉ giáo viên mới có thể chấm điểm
    if not current_user.is_teacher():
        flash('Chỉ giáo viên mới có thể chấm điểm.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    submission = Submission.query.get_or_404(submission_id)
    project = Project.query.get_or_404(submission.project_id)
    
    # Kiểm tra xem giáo viên có quyền không
    if project.teacher_id != current_user.id:
        flash('Bạn không có quyền chấm điểm bài nộp này.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    form = GradeForm()
    
    if form.validate_on_submit():
        try:
            submission.score = form.score.data
            submission.feedback = form.feedback.data
            
            db.session.commit()
            
            flash('Đã chấm điểm thành công!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Có lỗi xảy ra: {str(e)}', 'danger')
    else:
        # Hiển thị lỗi từ form
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{error}', 'danger')
    
    return redirect(url_for('projects.view_submission', submission_id=submission.id))

@projects_bp.route('/download/<int:submission_id>')
@login_required
def download_file(submission_id):
    """Tải xuống file từ bài nộp
    
    - Kiểm tra quyền và trả về file để tải xuống
    
    Args:
        submission_id: ID của bài nộp có file cần tải xuống
        
    Returns:
        File để tải xuống hoặc chuyển hướng nếu không có quyền
    """
    submission = Submission.query.get_or_404(submission_id)
    project = Project.query.get_or_404(submission.project_id)
    
    # Kiểm tra quyền tải file
    is_authorized = False
    
    if current_user.is_teacher() and project.teacher_id == current_user.id:
        # Giáo viên có thể tải file từ bài nộp của dự án do họ tạo
        is_authorized = True
    elif current_user.is_student() and submission.student_id == current_user.id:
        # Học sinh có thể tải file từ bài nộp của chính mình
        is_authorized = True
    
    if not is_authorized:
        flash('Bạn không có quyền tải xuống file này.', 'danger')
        return redirect(url_for('main.dashboard'))
    
    # Kiểm tra xem bài nộp có file không
    if not submission.file_path:
        flash('Bài nộp này không có file đính kèm.', 'warning')
        return redirect(url_for('projects.view_submission', submission_id=submission.id))
    
    # Lấy đường dẫn đầy đủ đến file
    file_path = get_file_path(submission.file_path)
    
    if not file_path or not os.path.exists(file_path):
        flash('File không tồn tại hoặc đã bị xóa.', 'danger')
        return redirect(url_for('projects.view_submission', submission_id=submission.id))
    
    # Trả về file để tải xuống
    return send_file(file_path, 
                    as_attachment=True, 
                    download_name=os.path.basename(file_path)) 