import { create } from 'zustand';
import axios from 'axios';

interface User {
    id: number;
    username: string;
    email: string;
    role: 'teacher' | 'student';
}

interface AuthState {
    user: User | null;
    token: string | null;
    login: (email: string, password: string) => Promise<void>;
    register: (username: string, email: string, password: string, role: 'teacher' | 'student') => Promise<void>;
    logout: () => void;
}

const API_URL = 'http://localhost:5000/api';

export const useAuth = create<AuthState>((set) => ({
    user: null,
    token: localStorage.getItem('token'),

    login: async (email: string, password: string) => {
        try {
            const response = await axios.post(`${API_URL}/auth/login`, {
                email,
                password,
            });

            const { token, user } = response.data;
            localStorage.setItem('token', token);

            set({ token, user });
        } catch (error) {
            throw new Error('Đăng nhập thất bại');
        }
    },

    register: async (username: string, email: string, password: string, role: 'teacher' | 'student') => {
        try {
            const response = await axios.post(`${API_URL}/auth/register`, {
                username,
                email,
                password,
                role,
            });

            const { token, user } = response.data;
            localStorage.setItem('token', token);

            set({ token, user });
        } catch (error) {
            throw new Error('Đăng ký thất bại');
        }
    },

    logout: () => {
        localStorage.removeItem('token');
        set({ token: null, user: null });
    },
})); 