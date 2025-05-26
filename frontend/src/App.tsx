import { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

import { useAuthStore } from './store/auth';
import Layout from './components/Layout';
import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import Dashboard from './pages/Dashboard';
import Projects from './pages/Projects';
import ProjectDetail from './pages/ProjectDetail';
import Submissions from './pages/Submissions';
import SubmissionDetail from './pages/SubmissionDetail';

// Tạo theme
const theme = createTheme({
    palette: {
        primary: {
            main: '#1976d2',
        },
        secondary: {
            main: '#dc004e',
        },
    },
});

// Tạo QueryClient
const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            retry: 1,
            refetchOnWindowFocus: false,
        },
    },
});

// Component bảo vệ route
function ProtectedRoute({ children }: { children: React.ReactNode }) {
    const { isAuthenticated, isLoading, getCurrentUser } = useAuthStore();

    useEffect(() => {
        if (!isAuthenticated && !isLoading) {
            getCurrentUser();
        }
    }, [isAuthenticated, isLoading, getCurrentUser]);

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (!isAuthenticated) {
        return <Navigate to="/login" />;
    }

    return <Layout>{children}</Layout>;
}

function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <ThemeProvider theme={theme}>
                <CssBaseline />
                <Router>
                    <Routes>
                        {/* Public routes */}
                        <Route path="/login" element={<Login />} />
                        <Route path="/register" element={<Register />} />

                        {/* Protected routes */}
                        <Route
                            path="/dashboard"
                            element={
                                <ProtectedRoute>
                                    <Dashboard />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/projects"
                            element={
                                <ProtectedRoute>
                                    <Projects />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/projects/:id"
                            element={
                                <ProtectedRoute>
                                    <ProjectDetail />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/submissions"
                            element={
                                <ProtectedRoute>
                                    <Submissions />
                                </ProtectedRoute>
                            }
                        />
                        <Route
                            path="/submissions/:id"
                            element={
                                <ProtectedRoute>
                                    <SubmissionDetail />
                                </ProtectedRoute>
                            }
                        />

                        {/* Redirect to dashboard if authenticated, otherwise to login */}
                        <Route
                            path="/"
                            element={
                                <ProtectedRoute>
                                    <Navigate to="/dashboard" replace />
                                </ProtectedRoute>
                            }
                        />
                    </Routes>
                </Router>
            </ThemeProvider>
        </QueryClientProvider>
    );
}

export default App; 