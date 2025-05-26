from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from stem_app.models import db
from stem_app.models.project import Project
from stem_app.utils.decorators import teacher_required
from stem_app.forms.project import ProjectForm

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/create', methods=['GET', 'POST'])
@login_required
@teacher_required
def create_project():
    """Tạo dự án mới (chỉ giáo viên)"""
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            description=form.description.data,
            requirements=form.requirements.data,
            deadline=form.deadline.data,
            teacher_id=current_user.id
        )
        
        db.session.add(project)
        db.session.commit()
        
        flash('Dự án đã được tạo thành công!', 'success')
        return redirect(url_for('projects.view_project', project_id=project.id))
    
    return render_template('projects/create.html', title='Tạo dự án mới', form=form)

@projects_bp.route('/', methods=['GET'])
@login_required
def list_projects():
    """Lấy danh sách dự án"""
    if current_user.is_teacher:
        # Giáo viên thấy các dự án của mình
        projects = Project.query.filter_by(teacher_id=current_user.id).all()
    else:
        # Học sinh thấy tất cả dự án
        projects = Project.query.all()
    
    return render_template('projects/list.html', title='Danh sách dự án', projects=projects)

@projects_bp.route('/<int:project_id>', methods=['GET'])
@login_required
def view_project(project_id):
    """Xem chi tiết dự án"""
    project = db.session.get(Project, project_id)
    if not project:
        flash('Dự án không tồn tại', 'danger')
        return redirect(url_for('projects.list_projects'))
    
    return render_template('projects/view.html', title=project.title, project=project)

@projects_bp.route('/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    """Chỉnh sửa dự án (chỉ giáo viên tạo dự án)"""
    project = db.session.get(Project, project_id)
    if not project:
        flash('Dự án không tồn tại', 'danger')
        return redirect(url_for('projects.list_projects'))
    
    if not current_user.can_edit_project(project):
        flash('Bạn không có quyền chỉnh sửa dự án này', 'danger')
        return redirect(url_for('projects.view_project', project_id=project_id))
    
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        form.populate_obj(project)
        db.session.commit()
        
        flash('Dự án đã được cập nhật thành công!', 'success')
        return redirect(url_for('projects.view_project', project_id=project.id))
    
    return render_template('projects/edit.html', title=f'Chỉnh sửa: {project.title}', project=project, form=form)

@projects_bp.route('/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    """Xóa dự án (chỉ giáo viên tạo dự án)"""
    project = db.session.get(Project, project_id)
    if not project:
        flash('Dự án không tồn tại', 'danger')
        return redirect(url_for('projects.list_projects'))
    
    if not current_user.can_edit_project(project):
        flash('Bạn không có quyền xóa dự án này', 'danger')
        return redirect(url_for('projects.view_project', project_id=project_id))
    
    db.session.delete(project)
    db.session.commit()
    
    flash('Dự án đã được xóa thành công', 'success')
    return redirect(url_for('projects.list_projects')) 