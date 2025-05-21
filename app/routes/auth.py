from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models.user import User
from app.utils.forms import LoginForm, RegistrationForm

# Tạo blueprint cho routes xác thực
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Xử lý đăng ký người dùng mới
    
    - GET: Hiển thị form đăng ký
    - POST: Xử lý đăng ký, tạo tài khoản mới
    
    Returns:
        Template đăng ký hoặc chuyển hướng đến trang đăng nhập sau khi đăng ký thành công
    """
    # Nếu người dùng đã đăng nhập, chuyển hướng đến trang chủ
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    
    # Xử lý khi form được submit và hợp lệ
    if form.validate_on_submit():
        try:
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
                role=form.role.data
            )
            db.session.add(user)
            db.session.commit()
            
            flash('Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Có lỗi xảy ra: {str(e)}', 'danger')
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Xử lý đăng nhập người dùng
    
    - GET: Hiển thị form đăng nhập
    - POST: Xử lý đăng nhập
    
    Returns:
        Template đăng nhập hoặc chuyển hướng đến trang chủ sau khi đăng nhập thành công
    """
    # Nếu người dùng đã đăng nhập, chuyển hướng đến trang chủ
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    
    # Xử lý khi form được submit và hợp lệ
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        # Kiểm tra user tồn tại và mật khẩu khớp
        if user and user.check_password(form.password.data):
            # Đăng nhập user
            login_user(user)
            
            # Chuyển hướng đến trang yêu cầu gốc (nếu có) hoặc trang chủ
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Đăng nhập không thành công. Vui lòng kiểm tra tên đăng nhập và mật khẩu.', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """Xử lý đăng xuất người dùng
    
    Returns:
        Chuyển hướng đến trang chủ sau khi đăng xuất
    """
    logout_user()
    flash('Bạn đã đăng xuất thành công.', 'info')
    return redirect(url_for('main.index')) 