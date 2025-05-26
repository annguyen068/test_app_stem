from flask import Blueprint, request, jsonify, current_app, send_from_directory, g
from flask_login import login_required, current_user
from stem_app.models.submission import Submission
from stem_app.models.project import Project
from stem_app.models.comment import Comment
from stem_app.models import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from stem_app.utils.decorators import teacher_required
from stem_app.utils.jwt_middleware import jwt_required, get_current_user
import uuid

submissions_api = Blueprint('submissions_api', __name__)

def allowed_file(filename):
    """
    Kiểm tra xem file có được phép tải lên không
    """
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'zip', 'rar', 'jpg', 'jpeg', 'png'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@submissions_api.route('/project/<int:project_id>', methods=['GET'])
@login_required
def get_submissions_by_project(project_id):
    """
    API endpoint để lấy danh sách bài nộp cho một dự án
    - Giáo viên: xem tất cả bài nộp của dự án họ tạo
    - Học sinh: chỉ xem bài nộp của mình
    """
    project = db.session.get(Project, project_id)
    if not project:
        return jsonify({'error': 'Dự án không tồn tại'}), 404
    
    # Kiểm tra quyền
    if current_user.is_teacher:
        if project.teacher_id != current_user.id:
            return jsonify({'error': 'Không có quyền truy cập dự án này'}), 403
        submissions = Submission.query.filter_by(project_id=project_id).all()
    else:
        submissions = Submission.query.filter_by(
            project_id=project_id, 
            student_id=current_user.id
        ).all()
    
    result = []
    for submission in submissions:
        result.append({
            'id': submission.id,
            'title': submission.title,
            'content': submission.content,
            'file_path': submission.file_path,
            'score': submission.score,
            'feedback': submission.feedback,
            'submitted_at': submission.submitted_at.isoformat(),
            'student': {
                'id': submission.student.id,
                'username': submission.student.username
            } if submission.student else None
        })
    
    return jsonify(result), 200

@submissions_api.route('/<int:submission_id>', methods=['GET'])
@jwt_required
def get_submission(submission_id):
    """
    API endpoint để lấy thông tin chi tiết của một bài nộp
    """
    current_user = get_current_user()
    submission = db.session.get(Submission, submission_id)
    if not submission:
        return jsonify({'error': 'Bài nộp không tồn tại'}), 404
    
    # Kiểm tra quyền
    if current_user.is_teacher:
        project = db.session.get(Project, submission.project_id)
        if not project:
            return jsonify({'error': 'Dự án không tồn tại'}), 404
            
        if project.teacher_id != current_user.id:
            return jsonify({'error': 'Không có quyền truy cập bài nộp này'}), 403
    elif submission.student_id != current_user.id:
        return jsonify({'error': 'Không có quyền truy cập bài nộp này'}), 403
    
    # Lấy các comments
    comments = Comment.query.filter_by(submission_id=submission_id).order_by(Comment.created_at).all()
    comments_data = []
    for comment in comments:
        comments_data.append({
            'id': comment.id,
            'content': comment.content,
            'created_at': comment.created_at.isoformat(),
            'user': {
                'id': comment.user.id,
                'username': comment.user.username,
                'is_teacher': comment.user.is_teacher
            } if comment.user else None
        })
    
    result = {
        'id': submission.id,
        'title': submission.title,
        'content': submission.content,
        'file_path': submission.file_path,
        'score': submission.score,
        'feedback': submission.feedback,
        'submitted_at': submission.submitted_at.isoformat(),
        'student': {
            'id': submission.student.id,
            'username': submission.student.username
        } if submission.student else None,
        'project': {
            'id': submission.project.id,
            'title': submission.project.title
        } if submission.project else None,
        'comments': comments_data
    }
    
    return jsonify(result), 200

@submissions_api.route('/project/<int:project_id>', methods=['POST'])
@jwt_required
def create_submission(project_id):
    """
    API endpoint để tạo bài nộp mới
    Học sinh nộp bài cho dự án
    """
    current_user = get_current_user()
    if current_user.is_teacher:
        return jsonify({'error': 'Giáo viên không thể nộp bài'}), 403
    
    project = db.session.get(Project, project_id)
    if not project:
        return jsonify({'error': 'Dự án không tồn tại'}), 404
    
    # Kiểm tra dự án có đang hoạt động không
    if not project.is_active:
        return jsonify({'error': 'Dự án không còn hoạt động'}), 400
    
    # Kiểm tra deadline
    if not project.check_deadline():
        return jsonify({'error': 'Đã quá hạn nộp bài'}), 400
    
    # Xử lý JSON data
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Không có dữ liệu được gửi'}), 400
    
    title = data.get('title')
    content = data.get('content')
    description = data.get('description', '')  # Sử dụng description làm content nếu có
    
    if not title:
        return jsonify({'error': 'Thiếu tiêu đề bài nộp'}), 400
    
    # Nếu có description, sử dụng nó làm content
    if description and not content:
        content = description
    
    submission = Submission(
        title=title,
        content=content,
        project_id=project_id,
        student_id=current_user.id
    )
    
    db.session.add(submission)
    try:
        db.session.commit()
        return jsonify({
            'id': submission.id,
            'title': submission.title,
            'content': submission.content,
            'submitted_at': submission.submitted_at.isoformat(),
            'project_id': submission.project_id,
            'student_id': submission.student_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Có lỗi xảy ra khi nộp bài: {str(e)}'}), 500

@submissions_api.route('/<int:submission_id>', methods=['PUT'])
@jwt_required
def update_submission(submission_id):
    """
    API endpoint để cập nhật bài nộp
    - Học sinh: cập nhật nội dung bài nộp của mình
    - Giáo viên: chấm điểm và đưa ra nhận xét
    """
    current_user = get_current_user()
    submission = db.session.get(Submission, submission_id)
    if not submission:
        return jsonify({'error': 'Bài nộp không tồn tại'}), 404
    
    if current_user.is_teacher:
        # Giáo viên chấm điểm
        project = db.session.get(Project, submission.project_id)
        if not project:
            return jsonify({'error': 'Dự án không tồn tại'}), 404
            
        if project.teacher_id != current_user.id:
            return jsonify({'error': 'Không có quyền chấm điểm bài nộp này'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Không có dữ liệu được gửi'}), 400
        
        if 'score' in data:
            try:
                score = float(data['score'])
                if score < 0 or score > 10:
                    return jsonify({'error': 'Điểm phải từ 0 đến 10'}), 400
                submission.score = score
            except ValueError:
                return jsonify({'error': 'Điểm không hợp lệ'}), 400
        
        if 'feedback' in data:
            submission.feedback = data['feedback']
    else:
        # Học sinh cập nhật bài nộp
        if submission.student_id != current_user.id:
            return jsonify({'error': 'Không có quyền cập nhật bài nộp này'}), 403
        
        # Kiểm tra deadline
        project = Project.query.get(submission.project_id)
        if project.deadline and datetime.now() > project.deadline:
            return jsonify({'error': 'Đã quá hạn cập nhật bài nộp'}), 400
        
        # Xử lý form data
        title = request.form.get('title')
        content = request.form.get('content')
        
        if title:
            submission.title = title
        
        if content:
            submission.content = content
        
        # Xử lý file tải lên
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Tạo tên file duy nhất
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                
                # Xóa file cũ nếu có
                if submission.file_path:
                    old_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], submission.file_path)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                
                submission.file_path = unique_filename
    
    try:
        db.session.commit()
        return jsonify({
            'id': submission.id,
            'title': submission.title,
            'content': submission.content,
            'score': submission.score,
            'feedback': submission.feedback,
            'submitted_at': submission.submitted_at.isoformat(),
            'project_id': submission.project_id,
            'student_id': submission.student_id
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Có lỗi xảy ra khi cập nhật bài nộp: {str(e)}'}), 500

@submissions_api.route('/<int:submission_id>/comment', methods=['POST'])
@login_required
def add_comment(submission_id):
    """
    API endpoint để thêm bình luận vào bài nộp
    """
    submission = db.session.get(Submission, submission_id)
    if not submission:
        return jsonify({'error': 'Bài nộp không tồn tại'}), 404
    
    # Kiểm tra quyền
    if current_user.is_teacher:
        project = db.session.get(Project, submission.project_id)
        if not project:
            return jsonify({'error': 'Dự án không tồn tại'}), 404
            
        if project.teacher_id != current_user.id:
            return jsonify({'error': 'Không có quyền bình luận bài nộp này'}), 403
    elif submission.student_id != current_user.id:
        return jsonify({'error': 'Không có quyền bình luận bài nộp này'}), 403
    
    data = request.get_json()
    
    if not data or 'content' not in data or not data['content']:
        return jsonify({'error': 'Thiếu nội dung bình luận'}), 400
    
    comment = Comment(
        content=data['content'],
        submission_id=submission_id,
        user_id=current_user.id
    )
    
    db.session.add(comment)
    try:
        db.session.commit()
        return jsonify({
            'message': 'Thêm bình luận thành công',
            'comment_id': comment.id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Có lỗi xảy ra khi thêm bình luận: {str(e)}'}), 500

@submissions_api.route('/download/<path:filename>', methods=['GET'])
@login_required
def download_file(filename):
    """
    API endpoint để tải xuống file đính kèm của bài nộp
    """
    # Tìm submission có file_path tương ứng
    submission = Submission.query.filter_by(file_path=filename).first()
    if not submission:
        return jsonify({'error': 'File không tồn tại'}), 404
    
    # Kiểm tra quyền
    if current_user.is_teacher:
        project = db.session.get(Project, submission.project_id)
        if not project:
            return jsonify({'error': 'Dự án không tồn tại'}), 404
            
        if project.teacher_id != current_user.id:
            return jsonify({'error': 'Không có quyền tải file này'}), 403
    elif submission.student_id != current_user.id:
        return jsonify({'error': 'Không có quyền tải file này'}), 403
    
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename) 