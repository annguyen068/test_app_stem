import os
import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from stem_app.models import db
from stem_app.models.project import Project
from stem_app.models.submission import Submission
from stem_app.utils.decorators import teacher_required
from stem_app.utils.file_utils import save_file, allowed_file

submissions_bp = Blueprint('submissions', __name__)

@submissions_bp.route('/project/<int:project_id>/submit', methods=['GET', 'POST'])
@login_required
def create_submission(project_id):
    """Nộp bài cho dự án"""
    if current_user.is_teacher:
        flash('Giáo viên không thể nộp bài', 'danger')
        return redirect(url_for('projects.view_project', project_id=project_id))
    
    # Kiểm tra dự án tồn tại
    project = db.session.get(Project, project_id)
    if not project:
        flash('Dự án không tồn tại', 'danger')
        return redirect(url_for('projects.list_projects'))
    
    # Kiểm tra hạn nộp
    if not project.is_active():
        flash('Dự án đã hết hạn nộp bài', 'danger')
        return redirect(url_for('projects.view_project', project_id=project_id))
    
    # Kiểm tra đã có submission trước đó chưa
    existing_submission = Submission.query.filter_by(
        project_id=project_id,
        student_id=current_user.id
    ).first()
    
    if existing_submission:
        flash('Bạn đã nộp bài cho dự án này. Bạn sẽ cập nhật bài nộp cũ.', 'info')
        return redirect(url_for('submissions.edit_submission', submission_id=existing_submission.id))
    
    # Form handling
    if request.method == 'POST':
        try:
            content = request.form.get('content', '')
            
            # Xử lý file
            file_path = None
            if 'file' in request.files:
                file = request.files['file']
                if file.filename:
                    success, result = save_file(file, 'submissions')
                    if success:
                        file_path = result
                    else:
                        flash(f'Lỗi khi tải file: {result}', 'danger')
                        return redirect(request.url)
            
            # Tạo submission mới
            submission = Submission(
                content=content,
                project_id=project_id,
                student_id=current_user.id,
                file_path=file_path
            )
            
            db.session.add(submission)
            db.session.commit()
            
            flash('Nộp bài thành công!', 'success')
            return redirect(url_for('submissions.view_submission', submission_id=submission.id))
            
        except Exception as e:
            flash(f'Có lỗi xảy ra: {str(e)}', 'danger')
            return redirect(request.url)
    
    return render_template('submissions/create.html', title='Nộp bài', project=project)

@submissions_bp.route('/project/<int:project_id>/submissions', methods=['GET'])
@login_required
@teacher_required
def list_submissions(project_id):
    """Lấy danh sách bài nộp của dự án (chỉ giáo viên)"""
    # Kiểm tra dự án tồn tại
    project = db.session.get(Project, project_id)
    if not project:
        flash('Dự án không tồn tại', 'danger')
        return redirect(url_for('projects.list_projects'))
    
    # Kiểm tra giáo viên có quyền xem bài nộp của dự án này không
    if project.teacher_id != current_user.id:
        flash('Bạn không có quyền xem bài nộp của dự án này', 'danger')
        return redirect(url_for('projects.list_projects'))
    
    submissions = Submission.query.filter_by(project_id=project_id).all()
    
    return render_template('submissions/list.html', title=f'Bài nộp - {project.title}', project=project, submissions=submissions)

@submissions_bp.route('/<int:submission_id>', methods=['GET'])
@login_required
def view_submission(submission_id):
    """Xem chi tiết bài nộp"""
    submission = db.session.get(Submission, submission_id)
    if not submission:
        flash('Bài nộp không tồn tại', 'danger')
        return redirect(url_for('projects.list_projects'))
    
    # Kiểm tra quyền xem bài nộp
    if not current_user.is_teacher and submission.student_id != current_user.id:
        flash('Bạn không có quyền xem bài nộp này', 'danger')
        return redirect(url_for('projects.list_projects'))
    
    return render_template('submissions/view.html', title='Chi tiết bài nộp', submission=submission)

@submissions_bp.route('/<int:submission_id>/grade', methods=['GET', 'POST'])
@login_required
@teacher_required
def grade_submission(submission_id):
    """Chấm điểm bài nộp"""
    submission = db.session.get(Submission, submission_id)
    if not submission:
        flash('Bài nộp không tồn tại', 'danger')
        return redirect(url_for('projects.list_projects'))
    
    # Kiểm tra giáo viên có quyền chấm điểm bài nộp này không
    project = db.session.get(Project, submission.project_id)
    if project.teacher_id != current_user.id:
        flash('Bạn không có quyền chấm điểm bài nộp này', 'danger')
        return redirect(url_for('projects.list_projects'))
    
    if request.method == 'POST':
        try:
            grade = int(request.form.get('grade', 0))
            feedback = request.form.get('feedback', '')
            
            if grade < 0 or grade > 100:
                flash('Điểm phải nằm trong khoảng từ 0 đến 100', 'danger')
                return redirect(request.url)
            
            submission.grade = grade
            submission.feedback = feedback
            db.session.commit()
            
            flash('Chấm điểm thành công!', 'success')
            return redirect(url_for('submissions.view_submission', submission_id=submission.id))
            
        except ValueError:
            flash('Điểm phải là số nguyên', 'danger')
            return redirect(request.url)
        except Exception as e:
            flash(f'Có lỗi xảy ra: {str(e)}', 'danger')
            return redirect(request.url)
    
    return render_template('submissions/grade.html', title='Chấm điểm', submission=submission, project=project)

@submissions_bp.route('/download/<path:filename>', methods=['GET'])
@login_required
def download_file(filename):
    """Tải xuống file bài nộp"""
    # Xác định quyền truy cập file dựa trên đường dẫn
    upload_folder = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(upload_folder, filename, as_attachment=True)

@submissions_bp.route('/all', methods=['GET'])
@login_required
def list_all_submissions():
    """Lấy danh sách tất cả bài nộp"""
    if current_user.is_teacher:
        # Giáo viên thấy bài nộp của các dự án do họ tạo
        submissions = Submission.query.join(Project).filter(Project.teacher_id == current_user.id).all()
    else:
        # Học sinh chỉ thấy bài nộp của họ
        submissions = current_user.submissions.all()
    
    return render_template('submissions/list_all.html', title='Danh sách bài nộp', submissions=submissions) 