import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

def get_unique_filename(filename):
    """Tạo tên file duy nhất bằng cách thêm UUID
    
    Args:
        filename: Tên file gốc
        
    Returns:
        str: Tên file duy nhất
    """
    # Lấy phần mở rộng file
    ext = filename.rsplit('.', 1)[1].lower()
    # Tạo tên file mới với UUID
    return f"{uuid.uuid4().hex}.{ext}"

def save_file(file, folder=None):
    """Lưu file upload vào thư mục an toàn
    
    Args:
        file: FileStorage object từ form
        folder: Thư mục con trong UPLOAD_FOLDER (optional)
        
    Returns:
        str: Đường dẫn tương đối đến file đã lưu
    """
    try:
        filename = secure_filename(file.filename)
        unique_filename = get_unique_filename(filename)
        
        # Tạo đường dẫn upload
        upload_path = current_app.config['UPLOAD_FOLDER']
        if folder:
            upload_path = os.path.join(upload_path, folder)
            
        # Tạo thư mục nếu chưa tồn tại
        os.makedirs(upload_path, exist_ok=True)
        
        # Lưu file
        file_path = os.path.join(upload_path, unique_filename)
        file.save(file_path)
        
        return os.path.join(folder, unique_filename) if folder else unique_filename
        
    except Exception as e:
        current_app.logger.error(f"Lỗi khi lưu file: {str(e)}")
        raise

def delete_file(filename):
    """Xóa file từ hệ thống
    
    Args:
        filename: Tên file cần xóa (đường dẫn tương đối trong UPLOAD_FOLDER)
    """
    try:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            
    except Exception as e:
        current_app.logger.error(f"Lỗi khi xóa file: {str(e)}")
        raise

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