# 🎓 STEM Project Management System

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
