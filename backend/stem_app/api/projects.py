from flask import Blueprint, request, jsonify, current_app, g
from flask_login import login_required, current_user
from stem_app.models.project import Project
from stem_app.models.user import User
from stem_app.models import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from stem_app.utils.decorators import teacher_required
from stem_app.utils.jwt_middleware import jwt_required, get_current_user

projects_api = Blueprint('projects_api', __name__)

@projects_api.route('/', methods=['GET'])
@jwt_required
def get_projects():
    """
    API endpoint để lấy danh sách dự án
    - Giáo viên: xem tất cả dự án họ tạo
    - Học sinh: xem tất cả dự án đang hoạt động
    """
    current_user = get_current_user()
    if current_user.is_teacher:
        projects = Project.query.filter_by(teacher_id=current_user.id).all()
    else:
        projects = Project.query.filter_by(is_active=True).all()
    
    result = []
    for project in projects:
        result.append({
            'id': project.id,
            'title': project.title,
            'description': project.description,
            'deadline': project.deadline.isoformat() if project.deadline else None,
            'is_active': project.is_active,
            'created_at': project.created_at.isoformat(),
            'teacher': {
                'id': project.teacher.id,
                'username': project.teacher.username
            } if project.teacher else None
        })
    
    return jsonify(result), 200

@projects_api.route('/<int:project_id>', methods=['GET'])
@login_required
def get_project(project_id):
    """
    API endpoint để lấy thông tin chi tiết của một dự án
    """
    project = db.session.get(Project, project_id)
    if not project:
        return jsonify({'error': 'Dự án không tồn tại'}), 404
    
    # Học sinh chỉ có thể xem dự án đang hoạt động
    if not current_user.is_teacher and not project.is_active:
        return jsonify({'error': 'Không có quyền truy cập dự án này'}), 403
    
    # Giáo viên chỉ có thể xem dự án của mình
    if current_user.is_teacher and project.teacher_id != current_user.id:
        return jsonify({'error': 'Không có quyền truy cập dự án này'}), 403
    
    result = {
        'id': project.id,
        'title': project.title,
        'description': project.description,
        'deadline': project.deadline.isoformat() if project.deadline else None,
        'is_active': project.is_active,
        'created_at': project.created_at.isoformat(),
        'teacher': {
            'id': project.teacher.id,
            'username': project.teacher.username
        } if project.teacher else None
    }
    
    return jsonify(result), 200

@projects_api.route('/', methods=['POST'])
@jwt_required
def create_project():
    """
    API endpoint để tạo dự án mới
    Chỉ giáo viên mới có thể tạo dự án
    """
    current_user = get_current_user()
    
    # Kiểm tra quyền giáo viên
    if not current_user.is_teacher:
        return jsonify({'error': 'Chỉ giáo viên mới có thể tạo dự án'}), 403
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Không có dữ liệu được gửi'}), 400
    
    required_fields = ['title', 'description']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Thiếu trường {field}'}), 400
    
    project = Project(
        title=data['title'],
        description=data['description'],
        teacher_id=current_user.id
    )
    
    # Các trường tùy chọn
    if 'deadline' in data and data['deadline']:
        try:
            project.deadline = datetime.fromisoformat(data['deadline'])
        except ValueError:
            return jsonify({'error': 'Định dạng deadline không hợp lệ'}), 400
    
    if 'is_active' in data:
        project.is_active = bool(data['is_active'])
    
    db.session.add(project)
    try:
        db.session.commit()
        return jsonify({
            'id': project.id,
            'title': project.title,
            'description': project.description,
            'deadline': project.deadline.isoformat() if project.deadline else None,
            'is_active': project.is_active,
            'created_at': project.created_at.isoformat(),
            'teacher_id': project.teacher_id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Có lỗi xảy ra khi tạo dự án: {str(e)}'}), 500

@projects_api.route('/<int:project_id>', methods=['PUT'])
@login_required
@teacher_required
def update_project(project_id):
    """
    API endpoint để cập nhật thông tin dự án
    Chỉ giáo viên tạo dự án mới có thể cập nhật
    """
    project = db.session.get(Project, project_id)
    if not project:
        return jsonify({'error': 'Dự án không tồn tại'}), 404
    
    # Kiểm tra quyền
    if project.teacher_id != current_user.id:
        return jsonify({'error': 'Không có quyền cập nhật dự án này'}), 403
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Không có dữ liệu được gửi'}), 400
    
    # Cập nhật các trường
    if 'title' in data:
        project.title = data['title']
    
    if 'description' in data:
        project.description = data['description']
    
    if 'deadline' in data:
        if data['deadline']:
            try:
                project.deadline = datetime.fromisoformat(data['deadline'])
            except ValueError:
                return jsonify({'error': 'Định dạng deadline không hợp lệ'}), 400
        else:
            project.deadline = None
    
    if 'is_active' in data:
        project.is_active = bool(data['is_active'])
    
    try:
        db.session.commit()
        return jsonify({'message': 'Cập nhật dự án thành công'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Có lỗi xảy ra khi cập nhật dự án: {str(e)}'}), 500

@projects_api.route('/<int:project_id>', methods=['DELETE'])
@login_required
@teacher_required
def delete_project(project_id):
    """
    API endpoint để xóa dự án
    Chỉ giáo viên tạo dự án mới có thể xóa
    """
    project = db.session.get(Project, project_id)
    if not project:
        return jsonify({'error': 'Dự án không tồn tại'}), 404
    
    # Kiểm tra quyền
    if project.teacher_id != current_user.id:
        return jsonify({'error': 'Không có quyền xóa dự án này'}), 403
    
    try:
        db.session.delete(project)
        db.session.commit()
        return jsonify({'message': 'Xóa dự án thành công'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Có lỗi xảy ra khi xóa dự án: {str(e)}'}), 500 