from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Health check endpoint
@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint để kiểm tra trạng thái API"""
    return jsonify({
        'status': 'healthy',
        'message': 'STEM App API is running'
    }), 200

# Import các API routes
from stem_app.api.auth import auth_api
from stem_app.api.projects import projects_api
from stem_app.api.submissions import submissions_api

# Đăng ký các blueprints
api_bp.register_blueprint(auth_api, url_prefix='/auth')
api_bp.register_blueprint(projects_api, url_prefix='/projects')
api_bp.register_blueprint(submissions_api, url_prefix='/submissions') 