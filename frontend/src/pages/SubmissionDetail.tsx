import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
    Container,
    Typography,
    Box,
    Paper,
    Button,
    Grid,
    CircularProgress,
    TextField,
    Divider,
    Alert,
} from '@mui/material';
import { useFormik } from 'formik';
import * as yup from 'yup';
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
        description: string;
        deadline: string;
    };
    student: {
        id: number;
        username: string;
    };
}

const validationSchema = yup.object({
    grade: yup
        .number()
        .min(0, 'Điểm không được nhỏ hơn 0')
        .max(10, 'Điểm không được lớn hơn 10')
        .required('Điểm là bắt buộc'),
    feedback: yup
        .string()
        .min(10, 'Nhận xét phải có ít nhất 10 ký tự')
        .required('Nhận xét là bắt buộc'),
});

export default function SubmissionDetail() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const { user } = useAuthStore();
    const [error, setError] = useState<string | null>(null);
    const queryClient = useQueryClient();

    const { data: submission, isLoading } = useQuery<Submission>({
        queryKey: ['submission', id],
        queryFn: async () => {
            const response = await api.get(`/submissions/${id}`);
            return response.data;
        },
    });

    const gradeSubmissionMutation = useMutation({
        mutationFn: (values: { grade: number; feedback: string }) =>
            api.post(`/submissions/${id}/grade`, values),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['submission', id] });
            setError(null);
        },
        onError: (error: any) => {
            setError(error.response?.data?.error || 'Có lỗi xảy ra khi chấm điểm');
        },
    });

    const formik = useFormik({
        initialValues: {
            grade: submission?.grade || 0,
            feedback: submission?.feedback || '',
        },
        validationSchema: validationSchema,
        enableReinitialize: true,
        onSubmit: (values) => {
            gradeSubmissionMutation.mutate(values);
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

    if (!submission) {
        return (
            <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
                <Typography variant="h5" color="error">
                    Không tìm thấy bài nộp
                </Typography>
            </Container>
        );
    }

    const isTeacher = user?.role === 'teacher';
    const isStudent = user?.role === 'student';
    const isSubmissionOwner = user?.id === submission.student.id;

    return (
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 4 }}>
                <Typography variant="h4">Chi tiết bài nộp</Typography>
                <Button
                    variant="outlined"
                    onClick={() => navigate(`/projects/${submission.project.id}`)}
                >
                    Xem dự án
                </Button>
            </Box>

            <Grid container spacing={3}>
                <Grid item xs={12} md={8}>
                    <Paper sx={{ p: 3, mb: 3 }}>
                        <Typography variant="h6" gutterBottom>
                            Nội dung bài nộp
                        </Typography>
                        <Typography paragraph>{submission.content}</Typography>

                        {submission.file_path && (
                            <Box sx={{ mt: 2 }}>
                                <Typography variant="subtitle1" gutterBottom>
                                    File đính kèm:
                                </Typography>
                                <Button
                                    variant="contained"
                                    href={submission.file_path}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    Tải xuống
                                </Button>
                            </Box>
                        )}

                        <Box sx={{ mt: 3 }}>
                            <Typography variant="subtitle2" color="text.secondary">
                                Nộp bởi: {submission.student.username}
                            </Typography>
                            <Typography variant="subtitle2" color="text.secondary">
                                Ngày nộp: {new Date(submission.created_at).toLocaleString()}
                            </Typography>
                        </Box>
                    </Paper>

                    {isTeacher && (
                        <Paper sx={{ p: 3 }}>
                            <Typography variant="h6" gutterBottom>
                                Chấm điểm
                            </Typography>
                            {error && (
                                <Alert severity="error" sx={{ mb: 2 }}>
                                    {error}
                                </Alert>
                            )}
                            <form onSubmit={formik.handleSubmit}>
                                <TextField
                                    fullWidth
                                    margin="normal"
                                    id="grade"
                                    name="grade"
                                    label="Điểm"
                                    type="number"
                                    value={formik.values.grade}
                                    onChange={formik.handleChange}
                                    error={formik.touched.grade && Boolean(formik.errors.grade)}
                                    helperText={formik.touched.grade && formik.errors.grade}
                                    InputProps={{
                                        inputProps: { min: 0, max: 10, step: 0.1 },
                                    }}
                                />
                                <TextField
                                    fullWidth
                                    margin="normal"
                                    id="feedback"
                                    name="feedback"
                                    label="Nhận xét"
                                    multiline
                                    rows={4}
                                    value={formik.values.feedback}
                                    onChange={formik.handleChange}
                                    error={formik.touched.feedback && Boolean(formik.errors.feedback)}
                                    helperText={formik.touched.feedback && formik.errors.feedback}
                                />
                                <Button
                                    type="submit"
                                    variant="contained"
                                    sx={{ mt: 2 }}
                                    disabled={gradeSubmissionMutation.isPending}
                                >
                                    {gradeSubmissionMutation.isPending ? 'Đang lưu...' : 'Lưu điểm'}
                                </Button>
                            </form>
                        </Paper>
                    )}

                    {isStudent && isSubmissionOwner && submission.grade !== null && (
                        <Paper sx={{ p: 3 }}>
                            <Typography variant="h6" gutterBottom>
                                Kết quả chấm điểm
                            </Typography>
                            <Divider sx={{ mb: 2 }} />
                            <Typography variant="h4" color="primary" gutterBottom>
                                Điểm: {submission.grade}
                            </Typography>
                            <Typography variant="subtitle1" gutterBottom>
                                Nhận xét:
                            </Typography>
                            <Typography paragraph>{submission.feedback}</Typography>
                        </Paper>
                    )}
                </Grid>

                <Grid item xs={12} md={4}>
                    <Paper sx={{ p: 3 }}>
                        <Typography variant="h6" gutterBottom>
                            Thông tin dự án
                        </Typography>
                        <Divider sx={{ mb: 2 }} />
                        <Typography variant="subtitle1" gutterBottom>
                            {submission.project.title}
                        </Typography>
                        <Typography variant="body2" color="text.secondary" paragraph>
                            {submission.project.description}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                            Hạn nộp: {new Date(submission.project.deadline).toLocaleString()}
                        </Typography>
                    </Paper>
                </Grid>
            </Grid>
        </Container>
    );
} 