/**
 * API Helper cho ứng dụng STEM
 * Xử lý JWT token và gọi API endpoints
 */

class StemAPI {
    constructor() {
        this.baseURL = '';
        this.token = null;
    }

    /**
     * Lấy JWT token từ session hiện tại
     */
    async getToken() {
        try {
            const response = await fetch('/api/auth/token');
            if (response.ok) {
                const data = await response.json();
                this.token = data.token;
                return this.token;
            }
        } catch (error) {
            console.error('Error getting token:', error);
        }
        return null;
    }

    /**
     * Gọi API với JWT token
     */
    async apiCall(endpoint, options = {}) {
        // Lấy token nếu chưa có
        if (!this.token) {
            await this.getToken();
        }

        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
                ...(this.token && { 'Authorization': `Bearer ${this.token}` })
            }
        };

        const finalOptions = {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        };

        try {
            const response = await fetch(endpoint, finalOptions);

            // Nếu token hết hạn, thử lấy token mới
            if (response.status === 401) {
                this.token = null;
                await this.getToken();
                if (this.token) {
                    finalOptions.headers['Authorization'] = `Bearer ${this.token}`;
                    return await fetch(endpoint, finalOptions);
                }
            }

            return response;
        } catch (error) {
            console.error('API call error:', error);
            throw error;
        }
    }

    /**
     * Lấy danh sách dự án
     */
    async getProjects() {
        const response = await this.apiCall('/api/projects/');
        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to get projects');
    }

    /**
     * Tạo dự án mới
     */
    async createProject(projectData) {
        const response = await this.apiCall('/api/projects/', {
            method: 'POST',
            body: JSON.stringify(projectData)
        });
        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to create project');
    }

    /**
     * Lấy danh sách bài nộp cho dự án
     */
    async getSubmissions(projectId) {
        const response = await this.apiCall(`/api/submissions/project/${projectId}`);
        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to get submissions');
    }

    /**
     * Nộp bài cho dự án
     */
    async submitProject(projectId, submissionData) {
        const response = await this.apiCall(`/api/submissions/project/${projectId}`, {
            method: 'POST',
            body: JSON.stringify(submissionData)
        });
        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to submit project');
    }

    /**
     * Chấm điểm bài nộp
     */
    async gradeSubmission(submissionId, gradeData) {
        const response = await this.apiCall(`/api/submissions/${submissionId}`, {
            method: 'PUT',
            body: JSON.stringify(gradeData)
        });
        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to grade submission');
    }

    /**
     * Lấy thông tin chi tiết bài nộp
     */
    async getSubmission(submissionId) {
        const response = await this.apiCall(`/api/submissions/${submissionId}`);
        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to get submission');
    }
}

// Tạo instance global
window.stemAPI = new StemAPI();

/**
 * Utility functions
 */
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alertDiv, container.firstChild);

    // Auto dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

function showSuccess(message) {
    showAlert(message, 'success');
}

function showError(message) {
    showAlert(message, 'danger');
}

function showInfo(message) {
    showAlert(message, 'info');
} 