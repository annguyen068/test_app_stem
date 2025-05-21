import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename

def save_file(file):
    """Lưu file đã upload với tên an toàn và duy nhất
    
    Args:
        file: Đối tượng FileStorage từ request.files
        
    Returns:
        Đường dẫn tương đối của file đã lưu, or None nếu không có file
    """
    if file and file.filename:
        # Đảm bảo tên file an toàn
        filename = secure_filename(file.filename)
        # Thêm UUID vào tên file để đảm bảo tính duy nhất
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        # Lưu file
        upload_path = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
        file_path = os.path.join(upload_path, unique_filename)
        
        # Đảm bảo thư mục upload tồn tại
        os.makedirs(upload_path, exist_ok=True)
        
        try:
            file.save(file_path)
            # Trả về đường dẫn tương đối
            return os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        except Exception as e:
            current_app.logger.error(f"Lỗi khi lưu file: {str(e)}")
            return None
    
    return None

def get_file_path(relative_path):
    """Lấy đường dẫn tuyệt đối đến file
    
    Args:
        relative_path: Đường dẫn tương đối của file (được lưu trong database)
        
    Returns:
        Đường dẫn tuyệt đối đến file, hoặc None nếu file không tồn tại
    """
    if not relative_path:
        return None
    
    file_path = os.path.join(current_app.root_path, relative_path)
    if os.path.exists(file_path):
        return file_path
    
    return None

def delete_file(relative_path):
    """Xóa file từ hệ thống file
    
    Args:
        relative_path: Đường dẫn tương đối của file cần xóa
        
    Returns:
        True nếu xóa thành công, False nếu không
    """
    if not relative_path:
        return False
    
    file_path = os.path.join(current_app.root_path, relative_path)
    
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        current_app.logger.error(f"Lỗi khi xóa file: {str(e)}")
    
    return False 