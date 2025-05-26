import { useQuery } from '@tanstack/react-query';
import {
    Container,
    Grid,
    Paper,
    Typography,
    Box,
    CircularProgress,
} from '@mui/material';
import {
    Assignment as AssignmentIcon,
    School as SchoolIcon,
    Timer as TimerIcon,
} from '@mui/icons-material';
import api from '../api/config';
import { useAuthStore } from '../store/auth';

interface DashboardStats {
    totalProjects: number;
    activeProjects: number;
    totalSubmissions: number;
    pendingSubmissions: number;
}

export default function Dashboard() {
    const { user } = useAuthStore();

    const { data: stats, isLoading } = useQuery<DashboardStats>({
        queryKey: ['dashboardStats'],
        queryFn: async () => {
            const response = await api.get('/dashboard/stats');
            return response.data;
        },
    });

    if (isLoading) {
        return (
            <Box
                display="flex"
                justifyContent="center"
                alignItems="center"
                minHeight="80vh"
            >
                <CircularProgress />
            </Box>
        );
    }

    return (
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Typography variant="h4" gutterBottom>
                Xin chào, {user?.username}!
            </Typography>
            <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                {user?.role === 'teacher'
                    ? 'Đây là trang quản lý dự án của bạn'
                    : 'Đây là trang theo dõi bài nộp của bạn'}
            </Typography>

            <Grid container spacing={3} sx={{ mt: 2 }}>
                {/* Tổng số dự án */}
                <Grid item xs={12} sm={6} md={3}>
                    <Paper
                        sx={{
                            p: 2,
                            display: 'flex',
                            flexDirection: 'column',
                            height: 140,
                        }}
                    >
                        <Box
                            sx={{
                                display: 'flex',
                                alignItems: 'center',
                                mb: 2,
                            }}
                        >
                            <AssignmentIcon color="primary" sx={{ mr: 1 }} />
                            <Typography component="h2" variant="h6" color="primary">
                                Tổng số dự án
                            </Typography>
                        </Box>
                        <Typography component="p" variant="h4">
                            {stats?.totalProjects || 0}
                        </Typography>
                    </Paper>
                </Grid>

                {/* Dự án đang hoạt động */}
                <Grid item xs={12} sm={6} md={3}>
                    <Paper
                        sx={{
                            p: 2,
                            display: 'flex',
                            flexDirection: 'column',
                            height: 140,
                        }}
                    >
                        <Box
                            sx={{
                                display: 'flex',
                                alignItems: 'center',
                                mb: 2,
                            }}
                        >
                            <TimerIcon color="primary" sx={{ mr: 1 }} />
                            <Typography component="h2" variant="h6" color="primary">
                                Dự án đang hoạt động
                            </Typography>
                        </Box>
                        <Typography component="p" variant="h4">
                            {stats?.activeProjects || 0}
                        </Typography>
                    </Paper>
                </Grid>

                {/* Tổng số bài nộp */}
                <Grid item xs={12} sm={6} md={3}>
                    <Paper
                        sx={{
                            p: 2,
                            display: 'flex',
                            flexDirection: 'column',
                            height: 140,
                        }}
                    >
                        <Box
                            sx={{
                                display: 'flex',
                                alignItems: 'center',
                                mb: 2,
                            }}
                        >
                            <SchoolIcon color="primary" sx={{ mr: 1 }} />
                            <Typography component="h2" variant="h6" color="primary">
                                Tổng số bài nộp
                            </Typography>
                        </Box>
                        <Typography component="p" variant="h4">
                            {stats?.totalSubmissions || 0}
                        </Typography>
                    </Paper>
                </Grid>

                {/* Bài nộp chờ chấm điểm */}
                <Grid item xs={12} sm={6} md={3}>
                    <Paper
                        sx={{
                            p: 2,
                            display: 'flex',
                            flexDirection: 'column',
                            height: 140,
                        }}
                    >
                        <Box
                            sx={{
                                display: 'flex',
                                alignItems: 'center',
                                mb: 2,
                            }}
                        >
                            <SchoolIcon color="secondary" sx={{ mr: 1 }} />
                            <Typography component="h2" variant="h6" color="secondary">
                                Bài nộp chờ chấm điểm
                            </Typography>
                        </Box>
                        <Typography component="p" variant="h4">
                            {stats?.pendingSubmissions || 0}
                        </Typography>
                    </Paper>
                </Grid>
            </Grid>
        </Container>
    );
} 