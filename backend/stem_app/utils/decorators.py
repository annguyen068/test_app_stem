from functools import wraps
from flask import abort, jsonify
from flask_login import current_user

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_teacher:
            return jsonify({'error': 'Yêu cầu quyền giáo viên'}), 403
        return f(*args, **kwargs)
    return decorated_function

def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.is_teacher:
            return jsonify({'error': 'Yêu cầu quyền học sinh'}), 403
        return f(*args, **kwargs)
    return decorated_function

def owner_required(model):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            obj = model.query.get_or_404(kwargs.get('id'))
            if not current_user.is_authenticated or obj.user_id != current_user.id:
                return jsonify({'error': 'Không có quyền truy cập'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator 