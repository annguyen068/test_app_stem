import { create } from 'zustand';
import api from '../api/config';

interface User {
    id: number;
    email: string;
    username: string;
    is_teacher: boolean;
}

interface AuthState {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    error: string | null;
    login: (email: string, password: string) => Promise<void>;
    register: (email: string, username: string, password: string, is_teacher: boolean) => Promise<void>;
    logout: () => void;
    getCurrentUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
    user: null,
    isAuthenticated: false,
    isLoading: false,
    error: null,

    login: async (email: string, password: string) => {
        set({ isLoading: true, error: null });
        try {
            const response = await api.post('/auth/login', { email, password });
            const { token, user } = response.data;

            localStorage.setItem('access_token', token);

            set({ user, isAuthenticated: true, isLoading: false });
        } catch (error: any) {
            set({
                error: error.response?.data?.error || 'Đăng nhập thất bại',
                isLoading: false
            });
            throw error;
        }
    },

    register: async (email: string, username: string, password: string, is_teacher: boolean) => {
        set({ isLoading: true, error: null });
        try {
            const response = await api.post('/auth/register', {
                email,
                username,
                password,
                is_teacher,
            });

            set({ isLoading: false });
        } catch (error: any) {
            set({
                error: error.response?.data?.error || 'Đăng ký thất bại',
                isLoading: false
            });
            throw error;
        }
    },

    logout: async () => {
        try {
            await api.post('/auth/logout');
        } catch (error) {
            console.error('Lỗi khi đăng xuất:', error);
        } finally {
            localStorage.removeItem('access_token');
            set({ user: null, isAuthenticated: false });
        }
    },

    getCurrentUser: async () => {
        const token = localStorage.getItem('access_token');
        if (!token) {
            set({ isAuthenticated: false, isLoading: false });
            return;
        }

        set({ isLoading: true, error: null });
        try {
            const response = await api.get('/auth/user');
            set({
                user: response.data,
                isAuthenticated: true,
                isLoading: false
            });
        } catch (error: any) {
            localStorage.removeItem('access_token');
            set({
                error: error.response?.data?.error || 'Không thể lấy thông tin người dùng',
                isLoading: false,
                isAuthenticated: false
            });
        }
    },
})); 