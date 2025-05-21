import os
import sys
import time
import requests
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

def test_endpoint(session, url, username, password):
    """Kiểm tra một endpoint cụ thể"""
    try:
        # Đăng nhập
        login_data = {
            'username': username,
            'password': password
        }
        response = session.post(f"{url}/auth/login", data=login_data)
        if response.status_code != 200:
            return f"Lỗi đăng nhập: {response.status_code}"
        
        # Kiểm tra trang chủ
        start_time = time.time()
        response = session.get(url)
        home_time = time.time() - start_time
        
        # Kiểm tra trang dashboard
        start_time = time.time()
        response = session.get(f"{url}/dashboard")
        dashboard_time = time.time() - start_time
        
        # Kiểm tra danh sách dự án
        start_time = time.time()
        response = session.get(f"{url}/projects")
        projects_time = time.time() - start_time
        
        # Kiểm tra danh sách bài nộp
        start_time = time.time()
        response = session.get(f"{url}/submissions")
        submissions_time = time.time() - start_time
        
        return {
            'username': username,
            'home_time': home_time,
            'dashboard_time': dashboard_time,
            'projects_time': projects_time,
            'submissions_time': submissions_time
        }
    except Exception as e:
        return f"Lỗi: {str(e)}"

def run_performance_test(base_url="http://127.0.0.1:5000", num_users=10):
    """Chạy kiểm tra hiệu năng với nhiều người dùng đồng thời"""
    print(f"Bắt đầu kiểm tra hiệu năng với {num_users} người dùng đồng thời...")
    
    # Tạo danh sách người dùng để test
    users = []
    for i in range(num_users):
        if i % 2 == 0:
            users.append({
                'username': f'student{i+1}',
                'password': 'password123'
            })
        else:
            users.append({
                'username': f'teacher{(i//2)+1}',
                'password': 'password123'
            })
    
    results = []
    with ThreadPoolExecutor(max_workers=num_users) as executor:
        futures = []
        for user in users:
            session = requests.Session()
            futures.append(
                executor.submit(
                    test_endpoint,
                    session,
                    base_url,
                    user['username'],
                    user['password']
                )
            )
        
        for future in futures:
            result = future.result()
            if isinstance(result, dict):
                results.append(result)
            else:
                print(result)
    
    if results:
        print("\nKết quả kiểm tra hiệu năng:")
        print(f"Số lượng người dùng đồng thời: {num_users}")
        print("\nThời gian phản hồi trung bình (giây):")
        avg_home = sum(r['home_time'] for r in results) / len(results)
        avg_dashboard = sum(r['dashboard_time'] for r in results) / len(results)
        avg_projects = sum(r['projects_time'] for r in results) / len(results)
        avg_submissions = sum(r['submissions_time'] for r in results) / len(results)
        
        print(f"- Trang chủ: {avg_home:.3f}")
        print(f"- Dashboard: {avg_dashboard:.3f}")
        print(f"- Danh sách dự án: {avg_projects:.3f}")
        print(f"- Danh sách bài nộp: {avg_submissions:.3f}")
        
        print("\nThời gian phản hồi tối đa (giây):")
        max_home = max(r['home_time'] for r in results)
        max_dashboard = max(r['dashboard_time'] for r in results)
        max_projects = max(r['projects_time'] for r in results)
        max_submissions = max(r['submissions_time'] for r in results)
        
        print(f"- Trang chủ: {max_home:.3f}")
        print(f"- Dashboard: {max_dashboard:.3f}")
        print(f"- Danh sách dự án: {max_projects:.3f}")
        print(f"- Danh sách bài nộp: {max_submissions:.3f}")

if __name__ == '__main__':
    # Kiểm tra với 10 người dùng đồng thời
    run_performance_test(num_users=10) 