# Ứng dụng Quản lý Dự án STEM

Ứng dụng web quản lý dự án STEM sử dụng Python và Flask.

## Cài đặt

1. Clone repository:
```bash
git clone <repository-url>
cd test_app_stem
```

2. Tạo và kích hoạt môi trường ảo:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Cài đặt các gói phụ thuộc:
```bash
cd backend
pip install -r requirements.txt
```

4. Tạo file `.env` trong thư mục `backend` với nội dung sau:
```
FLASK_APP=app.py
FLASK_ENV=development
FLASK_CONFIG=development
SECRET_KEY=super-secret-key-for-development
DATABASE_URL=sqlite:///instance/stem_app.db
UPLOAD_FOLDER=uploads
JWT_SECRET_KEY=jwt-secret-key-for-development
```

## Khởi tạo cơ sở dữ liệu

```bash
cd backend
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Chạy ứng dụng

```bash
cd backend
python app.py
```

Ứng dụng sẽ chạy tại http://localhost:5000

## Chức năng

- **Giáo viên**: Tạo và quản lý dự án STEM, chấm điểm bài nộp của học sinh
- **Học sinh**: Xem dự án, nộp bài và nhận phản hồi

## Cấu trúc thư mục

```
backend/
├── app.py                  # Entry point
├── stem_app/               # Main application package
│   ├── __init__.py         # App factory
│   ├── config.py           # Configuration
│   ├── forms/              # Form definitions
│   ├── models/             # Database models
│   ├── routes/             # Route handlers
│   ├── static/             # Static files
│   ├── templates/          # HTML templates
│   └── utils/              # Utility functions
├── instance/               # Instance-specific data
└── uploads/                # Uploaded files
```

## API Endpoints

### Authentication
- POST `/api/auth/register` - Đăng ký tài khoản mới
- POST `/api/auth/login` - Đăng nhập
- POST `/api/auth/logout` - Đăng xuất

### Projects
- GET `/api/projects` - Lấy danh sách dự án
- POST `/api/projects` - Tạo dự án mới
- GET `/api/projects/<id>` - Xem chi tiết dự án
- PUT `/api/projects/<id>` - Cập nhật dự án
- DELETE `/api/projects/<id>` - Xóa dự án

### Submissions
- GET `/api/submissions` - Lấy danh sách bài nộp
- POST `/api/submissions` - Nộp bài mới
- GET `/api/submissions/<id>` - Xem chi tiết bài nộp
- PUT `/api/submissions/<id>` - Cập nhật bài nộp
- DELETE `/api/submissions/<id>` - Xóa bài nộp

## Bảo mật

1. Tất cả các mật khẩu được mã hóa trước khi lưu vào cơ sở dữ liệu
2. JWT được sử dụng cho xác thực API
3. CORS được cấu hình để chỉ cho phép frontend truy cập
4. Tất cả các file tải lên được kiểm tra và lưu trữ an toàn
5. Các biến môi trường nhạy cảm được lưu trong file `.env`

## Phát triển

1. Đảm bảo tuân thủ PEP 8 cho code Python
2. Viết test cho các chức năng mới
3. Cập nhật tài liệu khi thêm/thay đổi API
4. Kiểm tra bảo mật trước khi triển khai 