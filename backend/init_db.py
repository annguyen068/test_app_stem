#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script để khởi tạo cơ sở dữ liệu và tạo tài khoản mẫu
"""

import os
import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

# Đường dẫn đến file cơ sở dữ liệu
DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'stem_app.db')

# Đảm bảo thư mục instance tồn tại
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Tạo kết nối đến cơ sở dữ liệu
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Tạo bảng users
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    is_teacher BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Tạo bảng projects
cursor.execute('''
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    requirements TEXT,
    deadline TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    teacher_id INTEGER NOT NULL,
    FOREIGN KEY (teacher_id) REFERENCES users (id)
)
''')

# Tạo bảng submissions
cursor.execute('''
CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    file_path VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    grade INTEGER,
    feedback TEXT,
    project_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects (id),
    FOREIGN KEY (student_id) REFERENCES users (id)
)
''')

# Tạo bảng comments
cursor.execute('''
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    submission_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (submission_id) REFERENCES submissions (id)
)
''')

# Tạo tài khoản mẫu
# Kiểm tra xem tài khoản giáo viên đã tồn tại chưa
cursor.execute("SELECT * FROM users WHERE email = ?", ("giaovien@example.com",))
teacher = cursor.fetchone()
if not teacher:
    # Tạo tài khoản giáo viên
    cursor.execute('''
    INSERT INTO users (username, email, password_hash, is_teacher, created_at, last_seen)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        "giaovien",
        "giaovien@example.com",
        generate_password_hash("password123"),
        True,
        datetime.utcnow(),
        datetime.utcnow()
    ))
    teacher_id = cursor.lastrowid
else:
    teacher_id = teacher[0]

# Kiểm tra xem tài khoản học sinh đã tồn tại chưa
cursor.execute("SELECT * FROM users WHERE email = ?", ("hocsinh@example.com",))
student = cursor.fetchone()
if not student:
    # Tạo tài khoản học sinh
    cursor.execute('''
    INSERT INTO users (username, email, password_hash, is_teacher, created_at, last_seen)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        "hocsinh",
        "hocsinh@example.com",
        generate_password_hash("password123"),
        False,
        datetime.utcnow(),
        datetime.utcnow()
    ))
    student_id = cursor.lastrowid
else:
    student_id = student[0]

# Tạo dự án mẫu
cursor.execute("SELECT * FROM projects WHERE title = ?", ("Dự án robot tự hành",))
if not cursor.fetchone():
    deadline1 = datetime.utcnow() + timedelta(days=30)
    cursor.execute('''
    INSERT INTO projects (title, description, requirements, deadline, teacher_id)
    VALUES (?, ?, ?, ?, ?)
    ''', (
        "Dự án robot tự hành",
        "Xây dựng một robot có thể tự di chuyển và tránh chướng ngại vật.",
        "1. Robot phải tự di chuyển\n2. Có khả năng phát hiện và tránh chướng ngại vật\n3. Hoạt động ít nhất 30 phút liên tục",
        deadline1,
        teacher_id
    ))
    project1_id = cursor.lastrowid
    
    deadline2 = datetime.utcnow() + timedelta(days=15)
    cursor.execute('''
    INSERT INTO projects (title, description, requirements, deadline, teacher_id)
    VALUES (?, ?, ?, ?, ?)
    ''', (
        "Ứng dụng học từ vựng tiếng Anh",
        "Phát triển một ứng dụng web giúp học sinh học từ vựng tiếng Anh hiệu quả.",
        "1. Có ít nhất 500 từ vựng\n2. Có chức năng kiểm tra\n3. Lưu trữ tiến độ học tập",
        deadline2,
        teacher_id
    ))
    project2_id = cursor.lastrowid
    
    # Tạo bài nộp mẫu
    cursor.execute('''
    INSERT INTO submissions (content, project_id, student_id, grade, feedback)
    VALUES (?, ?, ?, ?, ?)
    ''', (
        "Em đã hoàn thành robot tự hành sử dụng Arduino và cảm biến siêu âm.",
        project1_id,
        student_id,
        85,
        "Bài làm tốt, robot hoạt động ổn định. Cần cải thiện thêm về thời gian hoạt động."
    ))
    submission1_id = cursor.lastrowid
    
    cursor.execute('''
    INSERT INTO submissions (content, project_id, student_id)
    VALUES (?, ?, ?)
    ''', (
        "Em đã phát triển ứng dụng học từ vựng sử dụng React và Flask.",
        project2_id,
        student_id
    ))
    submission2_id = cursor.lastrowid
    
    # Tạo bình luận mẫu
    cursor.execute('''
    INSERT INTO comments (content, user_id, submission_id)
    VALUES (?, ?, ?)
    ''', (
        "Em có thể giải thích thêm về cách robot phát hiện chướng ngại vật không?",
        teacher_id,
        submission1_id
    ))
    
    cursor.execute('''
    INSERT INTO comments (content, user_id, submission_id)
    VALUES (?, ?, ?)
    ''', (
        "Em đã sử dụng cảm biến siêu âm HC-SR04 để đo khoảng cách và tránh chướng ngại vật.",
        student_id,
        submission1_id
    ))

# Lưu thay đổi và đóng kết nối
conn.commit()
conn.close()

print("Đã khởi tạo cơ sở dữ liệu thành công!")
print("\nTài khoản mẫu:")
print("Giáo viên: giaovien@example.com / password123")
print("Học sinh: hocsinh@example.com / password123") 