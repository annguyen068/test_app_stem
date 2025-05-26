import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
import magic

ALLOWED_EXTENSIONS = {
    'pdf', 'doc', 'docx', 'txt', 
    'png', 'jpg', 'jpeg', 'gif',
    'zip', 'rar', '7z',
    'py', 'ipynb', 'java', 'cpp', 'c'
}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_safe_filename(filename):
    """Generate a safe filename while preserving the original extension"""
    if filename:
        # Get the file extension
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        # Generate a random filename with UUID
        safe_filename = f"{uuid.uuid4().hex}.{ext}" if ext else uuid.uuid4().hex
        return safe_filename
    return None

def save_file(file, subdirectory=''):
    """
    Save a file safely with proper validation
    Returns: (success, filename or error_message)
    """
    if not file:
        return False, "No file provided"
    
    if not allowed_file(file.filename):
        return False, "File type not allowed"
    
    try:
        # Generate safe filename
        filename = get_safe_filename(file.filename)
        if not filename:
            return False, "Invalid filename"
        
        # Create full path
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], subdirectory)
        os.makedirs(upload_path, exist_ok=True)
        file_path = os.path.join(upload_path, filename)
        
        # Save file
        file.save(file_path)
        
        # Verify file type using python-magic
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        
        # List of allowed MIME types
        ALLOWED_MIMES = {
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'text/plain',
            'image/png',
            'image/jpeg',
            'image/gif',
            'application/zip',
            'application/x-rar-compressed',
            'application/x-7z-compressed',
            'text/x-python',
            'text/x-java',
            'text/x-c++',
            'text/x-c'
        }
        
        if file_type not in ALLOWED_MIMES:
            os.remove(file_path)
            return False, "Invalid file type detected"
        
        return True, filename
        
    except Exception as e:
        return False, f"Error saving file: {str(e)}"

def delete_file(filename, subdirectory=''):
    """
    Delete a file safely
    Returns: (success, message)
    """
    if not filename:
        return False, "No filename provided"
    
    try:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], subdirectory, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True, "File deleted successfully"
        return False, "File not found"
    except Exception as e:
        return False, f"Error deleting file: {str(e)}" 