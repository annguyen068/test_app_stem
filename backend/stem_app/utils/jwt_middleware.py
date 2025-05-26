import jwt
import os
from functools import wraps
from flask import request, jsonify, current_app, g
from stem_app.models.user import User

def jwt_required(f):
    """Decorator để yêu cầu JWT token hợp lệ"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Lấy token từ header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Token format không hợp lệ'}), 401
        
        if not token:
            return jsonify({'error': 'Token không được cung cấp'}), 401
        
        try:
            # Decode JWT token
            data = jwt.decode(
                token, 
                os.environ.get('JWT_SECRET_KEY', 'dev-key'), 
                algorithms=['HS256']
            )
            
            # Lấy thông tin user từ token
            user_id = data.get('id')
            user_email = data.get('email')
            is_teacher = data.get('is_teacher', False)
            
            # Tạo mock user object cho Flask-Login
            class MockUser:
                def __init__(self, id, email, is_teacher):
                    self.id = id
                    self.email = email
                    self.is_teacher = is_teacher
                    self.is_authenticated = True
                    self.is_active = True
                    self.is_anonymous = False
                
                def get_id(self):
                    return str(self.id)
            
            # Set current_user trong g context
            g.current_user = MockUser(user_id, user_email, is_teacher)
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token đã hết hạn'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token không hợp lệ'}), 401
        except Exception as e:
            current_app.logger.error(f"JWT decode error: {str(e)}")
            return jsonify({'error': 'Lỗi xử lý token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

def get_current_user():
    """Lấy current user từ JWT token"""
    return getattr(g, 'current_user', None) 