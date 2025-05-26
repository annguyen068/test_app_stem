from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Trang chủ"""
    if current_user.is_authenticated:
        if current_user.is_teacher:
            return render_template('main/teacher_dashboard.html', title='Bảng điều khiển giáo viên')
        else:
            return render_template('main/student_dashboard.html', title='Bảng điều khiển học sinh')
    return render_template('main/index.html', title='Trang chủ')

@main_bp.route('/test-api')
@login_required
def test_api():
    """Trang test API"""
    return render_template('test_api.html', title='Test API') 