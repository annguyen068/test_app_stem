#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script dọn dẹp project và chuẩn bị deploy lên GitHub
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def print_step(step):
    print(f"\n{'='*60}")
    print(f"🔄 {step}")
    print('='*60)

def print_success(msg):
    print(f"✅ {msg}")

def print_info(msg):
    print(f"ℹ️  {msg}")

def print_error(msg):
    print(f"❌ {msg}")

def remove_file_or_dir(path):
    """Xóa file hoặc thư mục"""
    try:
        if os.path.isfile(path):
            os.remove(path)
            print_success(f"Đã xóa file: {path}")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            print_success(f"Đã xóa thư mục: {path}")
        else:
            print_info(f"Không tồn tại: {path}")
    except Exception as e:
        print_error(f"Lỗi xóa {path}: {e}")

def cleanup_test_files():
    """Xóa các file test không cần thiết"""
    print_step("XÓA CÁC FILE TEST VÀ TÀI LIỆU")
    
    # Danh sách file/thư mục cần xóa
    files_to_remove = [
        # Test files
        "backend/test_*.py",
        "backend/run_*_test*.py",
        "backend/list_accounts.py",
        "backend/export_accounts.py",
        "backend/create_test_data.py",
        "backend/create_accounts.py",
        "backend/create_users.py",
        
        # Documentation files
        "backend/DANH_SACH_TAI_KHOAN_TEST.md",
        "backend/TAI_KHOAN_DANG_NHAP.md",
        "backend/FINAL_REPORT.md",
        "backend/tai_khoan_test.csv",
        "backend/dang_nhap_nhanh.txt",
        "backend/*.json",
        "backend/report.html",
        
        # Image files
        "backend/*.png",
        
        # Cache and temp directories
        "backend/__pycache__",
        "backend/.pytest_cache",
        "backend/stem_app.egg-info",
        "__pycache__",
        ".pytest_cache",
        "venv",
        
        # Instance data (database)
        "backend/instance",
        "instance",
        
        # Upload directories
        "backend/uploads",
        "uploads",
        
        # Scripts directory
        "scripts",
        
        # Prompt files
        "Prompt_Cho_Cursor_*.txt",
    ]
    
    # Xóa từng file/pattern
    for pattern in files_to_remove:
        if '*' in pattern:
            # Xử lý wildcard
            import glob
            for file_path in glob.glob(pattern):
                remove_file_or_dir(file_path)
        else:
            remove_file_or_dir(pattern)

def cleanup_backend_tests():
    """Xóa thư mục tests trong backend"""
    print_step("XÓA THỬ MỤC TESTS")
    remove_file_or_dir("backend/tests")

def create_production_gitignore():
    """Tạo .gitignore cho production"""
    print_step("TẠO .GITIGNORE CHO PRODUCTION")
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# Flask
instance/
.env
.flaskenv

# Database
*.db
*.sqlite
*.sqlite3

# Logs
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Uploads
uploads/

# Test files
test_*.py
*_test.py
tests/
.pytest_cache/
.coverage
htmlcov/

# Documentation
*.md
!README.md

# Reports
*.json
*.html
report.*

# Images (except essential ones)
*.png
*.jpg
*.jpeg
*.gif
!logo.*
!favicon.*

# Temporary files
*.tmp
*.temp
*.bak
*.backup

# Node modules (if any)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# React build (if any)
build/
dist/
"""
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    print_success("Đã tạo .gitignore mới")

def create_production_readme():
    """Tạo README.md cho production"""
    print_step("TẠO README.MD CHO PRODUCTION")
    
    readme_content = """# 🎓 STEM Project Management System

Hệ thống quản lý dự án STEM cho giáo viên và học sinh.

## 🚀 Tính năng chính

### 👨‍🏫 Dành cho Giáo viên
- Tạo và quản lý dự án STEM
- Xem danh sách bài nộp của học sinh
- Chấm điểm và đưa ra phản hồi
- Theo dõi tiến độ học sinh

### 👨‍🎓 Dành cho Học sinh
- Xem danh sách dự án có sẵn
- Nộp bài dự án
- Xem điểm số và phản hồi từ giáo viên
- Theo dõi deadline các dự án

## 🛠️ Công nghệ sử dụng

- **Backend**: Flask (Python)
- **Database**: SQLite với SQLAlchemy ORM
- **Authentication**: JWT tokens
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **API**: RESTful API

## 📦 Cài đặt

### Yêu cầu hệ thống
- Python 3.8+
- pip

### Cài đặt dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Khởi động ứng dụng
```bash
cd backend
python app.py
```

Ứng dụng sẽ chạy tại: http://127.0.0.1:5000

## 🔑 Tài khoản mặc định

### Giáo viên
- Username: `giaovien`
- Password: `123456`

### Học sinh
- Username: `hocsinh`
- Password: `123456`

## 📁 Cấu trúc project

```
test_app_stem_react/
├── backend/
│   ├── stem_app/           # Core application
│   │   ├── models/         # Database models
│   │   ├── api/           # API endpoints
│   │   ├── templates/     # HTML templates
│   │   └── static/        # CSS, JS, images
│   ├── app.py             # Main application file
│   ├── requirements.txt   # Python dependencies
│   └── wsgi.py           # WSGI entry point
└── README.md
```

## 🌐 API Endpoints

### Authentication
- `POST /api/auth/register` - Đăng ký tài khoản
- `POST /api/auth/login` - Đăng nhập

### Projects
- `GET /api/projects/` - Lấy danh sách dự án
- `POST /api/projects/` - Tạo dự án mới (giáo viên)
- `GET /api/projects/{id}` - Xem chi tiết dự án

### Submissions
- `POST /api/submissions/project/{id}` - Nộp bài (học sinh)
- `GET /api/submissions/` - Xem bài nộp
- `PUT /api/submissions/{id}` - Chấm điểm (giáo viên)

## 🚀 Deploy

### Development
```bash
cd backend
python app.py
```

### Production
```bash
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

## 📝 License

MIT License

## 👥 Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng tạo issue hoặc pull request.

## 📞 Liên hệ

- GitHub: [@annguyen068](https://github.com/annguyen068)
- Repository: [test_app_stem_react](https://github.com/annguyen068/test_app_stem_react)
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print_success("Đã tạo README.md mới")

def git_operations():
    """Thực hiện các thao tác Git"""
    print_step("THỰC HIỆN CÁC THAO TÁC GIT")
    
    try:
        # Kiểm tra Git repository
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode != 0:
            print_info("Khởi tạo Git repository...")
            subprocess.run(['git', 'init'], check=True)
        
        # Add remote nếu chưa có
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], capture_output=True, text=True)
        if result.returncode != 0:
            print_info("Thêm remote origin...")
            subprocess.run([
                'git', 'remote', 'add', 'origin', 
                'https://github.com/annguyen068/test_app_stem_react.git'
            ], check=True)
        
        # Add all files
        print_info("Thêm tất cả files...")
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Commit
        print_info("Commit changes...")
        subprocess.run([
            'git', 'commit', '-m', 
            'feat: Clean up project and prepare for production deployment\n\n- Remove test files and documentation\n- Update .gitignore for production\n- Create production README\n- Clean project structure'
        ], check=True)
        
        # Push to GitHub
        print_info("Push to GitHub...")
        subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
        
        print_success("Đã push thành công lên GitHub!")
        
    except subprocess.CalledProcessError as e:
        print_error(f"Lỗi Git: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🧹 DỌNG DẸP VÀ DEPLOY PROJECT LÊN GITHUB")
    print("="*60)
    
    # Xác nhận từ người dùng
    response = input("\n⚠️  Bạn có chắc muốn xóa tất cả file test và tài liệu? (y/N): ")
    if response.lower() != 'y':
        print("❌ Hủy bỏ thao tác")
        return
    
    # Thực hiện cleanup
    cleanup_test_files()
    cleanup_backend_tests()
    
    # Tạo file production
    create_production_gitignore()
    create_production_readme()
    
    # Git operations
    if git_operations():
        print_step("HOÀN THÀNH")
        print_success("Project đã được dọn dẹp và push lên GitHub thành công!")
        print_info("Repository: https://github.com/annguyen068/test_app_stem_react")
        print_info("Để chạy ứng dụng: cd backend && python app.py")
    else:
        print_error("Có lỗi xảy ra trong quá trình Git operations")

if __name__ == "__main__":
    main() 