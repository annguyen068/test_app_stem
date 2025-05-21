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

config.py              # Cấu hình chung cho ứng dụng
run.py                 # Entry point để chạy ứng dụng
tests/                 # Thư mục chứa test cases
uploads/               # Thư mục lưu trữ file uploads
```

## Yêu cầu hệ thống

- Python 3.8+
- Các thư viện được liệt kê trong `requirements.txt`

## Cài đặt

1. Clone repository:
```bash
git clone <repository-url>
cd stem-project-manager
```

2. Tạo và kích hoạt môi trường ảo (khuyến nghị):
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Cài đặt các phụ thuộc:
```bash
pip install -r requirements.txt
```

4. Khởi tạo cơ sở dữ liệu:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. Chạy ứng dụng:
```bash
python run.py
```

Sau khi chạy, ứng dụng sẽ có thể truy cập tại [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Kiểm thử

Chạy kiểm thử tự động:
```bash
python -m pytest tests/
```

## Thông tin bảo mật

Trong môi trường sản xuất:
1. Thay đổi `SECRET_KEY` trong file `.env` hoặc biến môi trường
2. Cấu hình cơ sở dữ liệu an toàn (thay vì SQLite)
3. Cấu hình HTTPS

## Giấy phép

[MIT](LICENSE) 