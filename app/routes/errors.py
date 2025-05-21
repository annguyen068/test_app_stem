from flask import render_template

def handle_404(error):
    """Xử lý lỗi 404 - Không tìm thấy trang
    
    Args:
        error: Đối tượng lỗi
        
    Returns:
        Template HTML và mã trạng thái 404
    """
    return render_template('errors/404.html'), 404

def handle_500(error):
    """Xử lý lỗi 500 - Lỗi máy chủ nội bộ
    
    Args:
        error: Đối tượng lỗi
        
    Returns:
        Template HTML và mã trạng thái 500
    """
    return render_template('errors/500.html'), 500 