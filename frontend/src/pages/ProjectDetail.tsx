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
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    Chip,
    Divider,
} from '@mui/material';
import {
    Edit as EditIcon,
    Delete as DeleteIcon,
    Upload as UploadIcon,
} from '@mui/icons-material';
import { useFormik } from 'formik';
import * as yup from 'yup';
import api from '../api/config';
import { useAuthStore } from '../store/auth';

interface Project {
    id: number;
    title: string;
    description: string;
    requirements: string;
    deadline: string;
    created_at: string;
    updated_at: string;
    teacher_id: number;
    submission_count: number;
}

interface Submission {
    id: number;
    content: string;
    file_path: string | null;
    grade: number | null;
    feedback: string | null;
    created_at: string;
    student: {
        id: number;
        username: string;
    };
}

const validationSchema = yup.object({
    title: yup
        .string()
        .min(3, 'Tiêu đề phải có ít nhất 3 ký tự')
        .max(100, 'Tiêu đề không được vượt quá 100 ký tự')
        .required('Tiêu đề là bắt buộc'),
    description: yup
        .string()
        .min(10, 'Mô tả phải có ít nhất 10 ký tự')
        .required('Mô tả là bắt buộc'),
    requirements: yup.string(),
    deadline: yup
        .string()
        .required('Hạn nộp là bắt buộc'),
});

export default function ProjectDetail() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const { user } = useAuthStore();
    const [openEditDialog, setOpenEditDialog] = useState(false);
    const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
    const queryClient = useQueryClient();

    const { data: project, isLoading: isLoadingProject } = useQuery<Project>({
        queryKey: ['project', id],
        queryFn: async () => {
            const response = await api.get(`/projects/${id}`);
            return response.data;
        },
    });

    const { data: submissions, isLoading: isLoadingSubmissions } = useQuery<Submission[]>({
        queryKey: ['submissions', id],
        queryFn: async () => {
            const response = await api.get(`/submissions/project/${id}`);
            return response.data;
        },
    });

    const updateProjectMutation = useMutation({
        mutationFn: (values: any) => api.put(`/projects/${id}`, values),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['project', id] });
            setOpenEditDialog(false);
        },
    });

    const deleteProjectMutation = useMutation({
        mutationFn: () => api.delete(`/projects/${id}`),
        onSuccess: () => {
            navigate('/projects');
        },
    });

    const formik = useFormik({
        initialValues: {
            title: project?.title || '',
            description: project?.description || '',
            requirements: project?.requirements || '',
            deadline: project?.deadline ? new Date(project.deadline).toISOString().slice(0, 16) : '',
        },
        validationSchema: validationSchema,
        enableReinitialize: true,
        onSubmit: (values) => {
            updateProjectMutation.mutate(values);
        },
    });

    const handleEdit = () => {
        setOpenEditDialog(true);
    };

    const handleDelete = () => {
        setOpenDeleteDialog(true);
    };

    const handleCloseEditDialog = () => {
        setOpenEditDialog(false);
        formik.resetForm();
    };

    const handleCloseDeleteDialog = () => {
        setOpenDeleteDialog(false);
    };

    if (isLoadingProject || isLoadingSubmissions) {
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

    if (!project) {
        return (
            <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
                <Typography variant="h5" color="error">
                    Không tìm thấy dự án
                </Typography>
            </Container>
        );
    }

    const isTeacher = user?.role === 'teacher';
    const isProjectOwner = user?.id === project.teacher_id;
    const canEdit = isTeacher && isProjectOwner;

    return (
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 4 }}>
                <Typography variant="h4">{project.title}</Typography>
                {canEdit && (
                    <Box>
                        <Button
                            variant="outlined"
                            startIcon={<EditIcon />}
                            onClick={handleEdit}
                            sx={{ mr: 1 }}
                        >
                            Chỉnh sửa
                        </Button>
                        <Button
                            variant="outlined"
                            color="error"
                            startIcon={<DeleteIcon />}
                            onClick={handleDelete}
                        >
                            Xóa
                        </Button>
                    </Box>
                )}
            </Box>

            <Grid container spacing={3}>
                <Grid item xs={12} md={8}>
                    <Paper sx={{ p: 3, mb: 3 }}>
                        <Typography variant="h6" gutterBottom>
                            Mô tả
                        </Typography>
                        <Typography paragraph>{project.description}</Typography>

                        {project.requirements && (
                            <>
                                <Typography variant="h6" gutterBottom>
                                    Yêu cầu
                                </Typography>
                                <Typography paragraph>{project.requirements}</Typography>
                            </>
                        )}

                        <Box sx={{ mt: 2 }}>
                            <Chip
                                label={`Hạn nộp: ${new Date(project.deadline).toLocaleString()}`}
                                color="primary"
                                sx={{ mr: 1 }}
                            />
                            <Chip
                                label={`${project.submission_count} bài nộp`}
                                color="secondary"
                            />
                        </Box>
                    </Paper>

                    {user?.role === 'student' && (
                        <Button
                            variant="contained"
                            startIcon={<UploadIcon />}
                            onClick={() => navigate(`/submissions/new?projectId=${project.id}`)}
                        >
                            Nộp bài
                        </Button>
                    )}
                </Grid>

                <Grid item xs={12} md={4}>
                    <Paper sx={{ p: 3 }}>
                        <Typography variant="h6" gutterBottom>
                            Bài nộp
                        </Typography>
                        <Divider sx={{ mb: 2 }} />
                        {submissions?.map((submission) => (
                            <Box key={submission.id} sx={{ mb: 2 }}>
                                <Typography variant="subtitle1">
                                    {submission.student.username}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                    Nộp lúc: {new Date(submission.created_at).toLocaleString()}
                                </Typography>
                                {submission.grade !== null && (
                                    <Typography variant="body2" color="primary">
                                        Điểm: {submission.grade}
                                    </Typography>
                                )}
                                <Button
                                    size="small"
                                    onClick={() => navigate(`/submissions/${submission.id}`)}
                                >
                                    Xem chi tiết
                                </Button>
                            </Box>
                        ))}
                    </Paper>
                </Grid>
            </Grid>

            {/* Dialog chỉnh sửa dự án */}
            <Dialog open={openEditDialog} onClose={handleCloseEditDialog} maxWidth="sm" fullWidth>
                <DialogTitle>Chỉnh sửa dự án</DialogTitle>
                <form onSubmit={formik.handleSubmit}>
                    <DialogContent>
                        <TextField
                            fullWidth
                            margin="normal"
                            id="title"
                            name="title"
                            label="Tiêu đề"
                            value={formik.values.title}
                            onChange={formik.handleChange}
                            error={formik.touched.title && Boolean(formik.errors.title)}
                            helperText={formik.touched.title && formik.errors.title}
                        />
                        <TextField
                            fullWidth
                            margin="normal"
                            id="description"
                            name="description"
                            label="Mô tả"
                            multiline
                            rows={4}
                            value={formik.values.description}
                            onChange={formik.handleChange}
                            error={formik.touched.description && Boolean(formik.errors.description)}
                            helperText={formik.touched.description && formik.errors.description}
                        />
                        <TextField
                            fullWidth
                            margin="normal"
                            id="requirements"
                            name="requirements"
                            label="Yêu cầu"
                            multiline
                            rows={4}
                            value={formik.values.requirements}
                            onChange={formik.handleChange}
                        />
                        <TextField
                            fullWidth
                            margin="normal"
                            id="deadline"
                            name="deadline"
                            label="Hạn nộp"
                            type="datetime-local"
                            value={formik.values.deadline}
                            onChange={formik.handleChange}
                            error={formik.touched.deadline && Boolean(formik.errors.deadline)}
                            helperText={formik.touched.deadline && formik.errors.deadline}
                            InputLabelProps={{
                                shrink: true,
                            }}
                        />
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={handleCloseEditDialog}>Hủy</Button>
                        <Button
                            type="submit"
                            variant="contained"
                            disabled={updateProjectMutation.isPending}
                        >
                            {updateProjectMutation.isPending ? 'Đang lưu...' : 'Lưu thay đổi'}
                        </Button>
                    </DialogActions>
                </form>
            </Dialog>

            {/* Dialog xác nhận xóa */}
            <Dialog open={openDeleteDialog} onClose={handleCloseDeleteDialog}>
                <DialogTitle>Xác nhận xóa</DialogTitle>
                <DialogContent>
                    <Typography>
                        Bạn có chắc chắn muốn xóa dự án này? Hành động này không thể hoàn tác.
                    </Typography>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCloseDeleteDialog}>Hủy</Button>
                    <Button
                        onClick={() => deleteProjectMutation.mutate()}
                        color="error"
                        variant="contained"
                        disabled={deleteProjectMutation.isPending}
                    >
                        {deleteProjectMutation.isPending ? 'Đang xóa...' : 'Xóa'}
                    </Button>
                </DialogActions>
            </Dialog>
        </Container>
    );
} 