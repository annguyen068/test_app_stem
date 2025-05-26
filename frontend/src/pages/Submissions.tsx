import { useQuery } from '@tanstack/react-query';
import {
    Container,
    Typography,
    Box,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Chip,
    CircularProgress,
    Button,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import api from '../api/config';
import { useAuthStore } from '../store/auth';

interface Submission {
    id: number;
    content: string;
    file_path: string | null;
    grade: number | null;
    feedback: string | null;
    created_at: string;
    project: {
        id: number;
        title: string;
        deadline: string;
    };
    student: {
        id: number;
        username: string;
    };
}

export default function Submissions() {
    const navigate = useNavigate();
    const { user } = useAuthStore();

    const { data: submissions, isLoading } = useQuery<Submission[]>({
        queryKey: ['submissions'],
        queryFn: async () => {
            const response = await api.get('/submissions');
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

    const isTeacher = user?.role === 'teacher';

    return (
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Typography variant="h4" gutterBottom>
                Bài nộp
            </Typography>

            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Dự án</TableCell>
                            {isTeacher && <TableCell>Học sinh</TableCell>}
                            <TableCell>Ngày nộp</TableCell>
                            <TableCell>Trạng thái</TableCell>
                            <TableCell>Điểm</TableCell>
                            <TableCell>Thao tác</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {submissions?.map((submission) => (
                            <TableRow key={submission.id}>
                                <TableCell>
                                    <Button
                                        color="primary"
                                        onClick={() => navigate(`/projects/${submission.project.id}`)}
                                    >
                                        {submission.project.title}
                                    </Button>
                                </TableCell>
                                {isTeacher && (
                                    <TableCell>{submission.student.username}</TableCell>
                                )}
                                <TableCell>
                                    {new Date(submission.created_at).toLocaleString()}
                                </TableCell>
                                <TableCell>
                                    <Chip
                                        label={submission.grade !== null ? 'Đã chấm điểm' : 'Chờ chấm điểm'}
                                        color={submission.grade !== null ? 'success' : 'warning'}
                                    />
                                </TableCell>
                                <TableCell>
                                    {submission.grade !== null ? submission.grade : '-'}
                                </TableCell>
                                <TableCell>
                                    <Button
                                        variant="outlined"
                                        size="small"
                                        onClick={() => navigate(`/submissions/${submission.id}`)}
                                    >
                                        Xem chi tiết
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Container>
    );
} 