from wtforms.validators import ValidationError
import os
from werkzeug.utils import secure_filename

def allowed_file(filename, allowed_extensions):
    """Kiểm tra phần mở rộng của file có được phép không
    
    Args:
        filename: Tên file cần kiểm tra
        allowed_extensions: Set các phần mở rộng được phép
        
    Returns:
        bool: True nếu file được phép, False nếu không
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def validate_file_upload(form, field):
    """Validator cho file upload
    
    Kiểm tra:
    - File có tồn tại
    - Phần mở rộng file hợp lệ
    - Kích thước file trong giới hạn
    
    Args:
        form: Form chứa field
        field: Field chứa file
        
    Raises:
        ValidationError: Nếu file không hợp lệ
    """
    if not field.data:
        raise ValidationError('Vui lòng chọn file để tải lên.')
        
    file = field.data
    if not allowed_file(file.filename, {'pdf', 'doc', 'docx', 'txt'}):
        raise ValidationError('Loại file không được phép. Chỉ chấp nhận PDF, DOC, DOCX, TXT.')
        
    # Kiểm tra kích thước file (max 10MB)
    if len(file.read()) > 10 * 1024 * 1024:
        raise ValidationError('File quá lớn. Kích thước tối đa là 10MB.')
    file.seek(0)  # Reset con trỏ file

def validate_unique_username(form, field):
    """Validator kiểm tra username có bị trùng không
    
    Args:
        form: Form chứa field
        field: Field chứa username
        
    Raises:
        ValidationError: Nếu username đã tồn tại
    """
    from app.models.user import User
    user = User.query.filter_by(username=field.data).first()
    if user is not None:
        raise ValidationError('Tên đăng nhập này đã được sử dụng.')

def validate_unique_email(form, field):
    """Validator kiểm tra email có bị trùng không
    
    Args:
        form: Form chứa field
        field: Field chứa email
        
    Raises:
        ValidationError: Nếu email đã tồn tại
    """
    from app.models.user import User
    user = User.query.filter_by(email=field.data).first()
    if user is not None:
        raise ValidationError('Email này đã được sử dụng.') 