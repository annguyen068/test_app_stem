# Ứng dụng Quản lý Dự án STEM

Ứng dụng web quản lý dự án STEM cho phép giáo viên và học sinh tương tác trong quá trình học tập STEM.

## Tính năng chính

- Xác thực và phân quyền người dùng (giáo viên/học sinh)
- Quản lý dự án STEM
- Nộp bài và chấm điểm
- Upload/download file và link bài nộp
- Giao diện responsive với Bootstrap
- Xử lý lỗi và bảo mật

## Cài đặt

1. Clone repository:
```bash
git clone <your-repo-url>
cd test_app_stem
```

2. Tạo môi trường ảo và cài đặt dependencies:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Khởi tạo database:
```bash
flask db upgrade
```

4. Chạy ứng dụng:
```bash
python run.py
```

Truy cập http://localhost:5000 để sử dụng ứng dụng.

## Cấu trúc thư mục

```
test_app_stem/
├── app/
│   ├── models/         # Database models
│   ├── routes/         # Route handlers
│   ├── static/         # Static files
│   ├── templates/      # HTML templates
│   └── utils/          # Utility functions
├── migrations/         # Database migrations
├── scripts/           # Helper scripts
├── requirements.txt   # Python dependencies
└── run.py            # Application entry point
```

## Đóng góp

Mọi đóng góp đều được hoan nghênh. Vui lòng tạo issue hoặc pull request.

## Tác giả

An Nguyen - [@annguyen068](https://github.com/annguyen068) 