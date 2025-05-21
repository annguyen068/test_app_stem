# Ứng Dụng Quản Lý Dự Án STEM

Ứng dụng web quản lý dự án STEM được phát triển bằng Python và Flask, cho phép giáo viên tạo và quản lý dự án, học sinh nộp bài và nhận đánh giá.

## Tính năng

### Dành cho Giáo viên
- Tạo và quản lý dự án STEM
- Xem danh sách bài nộp của học sinh
- Chấm điểm và cung cấp phản hồi cho học sinh

### Dành cho Học sinh
- Xem danh sách dự án có sẵn
- Nộp bài cho các dự án đang mở
- Tải lên file đính kèm cho bài nộp
- Xem điểm và phản hồi từ giáo viên

## Công nghệ sử dụng

- Python 3.8+
- Flask 3.0.2
- SQLAlchemy 2.0.28
- WTForms 3.1.2
- Bootstrap 5
- SQLite (có thể thay đổi sang PostgreSQL/MySQL)

## Cấu trúc dự án

```
app/
├── __init__.py        # Khởi tạo ứng dụng Flask và các extensions
├── config.py          # Cấu hình ứng dụng
├── models/            # Mô hình dữ liệu
│   ├── user.py        # Mô hình User
│   └── project.py     # Mô hình Project và Submission
├── routes/            # Các routes của ứng dụng
│   ├── auth.py        # Routes xác thực (đăng ký, đăng nhập)
│   ├── errors.py      # Routes xử lý lỗi
│   ├── main.py        # Routes chính
│   └── projects.py    # Routes liên quan đến dự án
├── static/            # Files tĩnh (CSS, JS, images)
├── templates/         # Templates HTML
│   ├── auth/          # Templates xác thực
│   ├── errors/        # Templates lỗi
│   ├── main/          # Templates chính
│   └── projects/      # Templates dự án
└── utils/             # Các tiện ích
    ├── forms.py       # Định nghĩa forms
    └── file_utils.py  # Xử lý file upload
```

## Cài đặt và Chạy

1. Clone repository:
```bash
git clone https://github.com/annguyen068/test_app_stem.git
cd test_app_stem
```

2. Tạo và kích hoạt môi trường ảo:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

4. Tạo file .env với nội dung:
```
SECRET_KEY=your_secret_key_here
SQLALCHEMY_DATABASE_URI=sqlite:///stem_projects.db
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=10485760  # 10MB
```

5. Khởi tạo database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. Chạy ứng dụng:
```bash
python run.py
```

Truy cập ứng dụng tại: http://127.0.0.1:5000

## Kiểm thử

Chạy kiểm thử tự động:
```bash
python -m pytest tests/
```

## Đóng góp

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## Giấy phép

[MIT](LICENSE)

## Tác giả

An Nguyen - [@annguyen068](https://github.com/annguyen068) 