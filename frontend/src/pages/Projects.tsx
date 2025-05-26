import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import {
    Container,
    Typography,
    Button,
    Grid,
    Card,
    CardContent,
    CardActions,
    Chip,
    Box,
    CircularProgress,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { useFormik } from 'formik';
import * as yup from 'yup';
import api from '../api/config';
import { useAuthStore } from '../store/auth';

interface Project {
    id: number;
    title: string;
    description: string;
    deadline: string;
    created_at: string;
    teacher_id: number;
    submission_count: number;
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
    deadline: yup
        .string()
        .required('Hạn nộp là bắt buộc'),
});

export default function Projects() {
    const navigate = useNavigate();
    const { user } = useAuthStore();
    const [openDialog, setOpenDialog] = useState(false);

    const { data: projects, isLoading, refetch } = useQuery<Project[]>({
        queryKey: ['projects'],
        queryFn: async () => {
            const response = await api.get('/projects');
            return response.data;
        },
    });

    const formik = useFormik({
        initialValues: {
            title: '',
            description: '',
            deadline: '',
        },
        validationSchema: validationSchema,
        onSubmit: async (values) => {
            try {
                await api.post('/projects', values);
                setOpenDialog(false);
                formik.resetForm();
                refetch();
            } catch (error) {
                console.error('Error creating project:', error);
            }
        },
    });

    const handleCreateProject = () => {
        setOpenDialog(true);
    };

    const handleCloseDialog = () => {
        setOpenDialog(false);
        formik.resetForm();
    };

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
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 4 }}>
                <Typography variant="h4">Dự án</Typography>
                {user?.role === 'teacher' && (
                    <Button
                        variant="contained"
                        startIcon={<AddIcon />}
                        onClick={handleCreateProject}
                    >
                        Tạo dự án mới
                    </Button>
                )}
            </Box>

            <Grid container spacing={3}>
                {projects?.map((project) => (
                    <Grid item xs={12} sm={6} md={4} key={project.id}>
                        <Card>
                            <CardContent>
                                <Typography variant="h6" gutterBottom>
                                    {project.title}
                                </Typography>
                                <Typography
                                    variant="body2"
                                    color="text.secondary"
                                    sx={{
                                        overflow: 'hidden',
                                        textOverflow: 'ellipsis',
                                        display: '-webkit-box',
                                        WebkitLineClamp: 3,
                                        WebkitBoxOrient: 'vertical',
                                    }}
                                >
                                    {project.description}
                                </Typography>
                                <Box sx={{ mt: 2 }}>
                                    <Chip
                                        label={`${project.submission_count} bài nộp`}
                                        size="small"
                                        sx={{ mr: 1 }}
                                    />
                                    <Chip
                                        label={`Hạn nộp: ${new Date(project.deadline).toLocaleDateString()}`}
                                        size="small"
                                        color="primary"
                                    />
                                </Box>
                            </CardContent>
                            <CardActions>
                                <Button
                                    size="small"
                                    onClick={() => navigate(`/projects/${project.id}`)}
                                >
                                    Xem chi tiết
                                </Button>
                            </CardActions>
                        </Card>
                    </Grid>
                ))}
            </Grid>

            {/* Dialog tạo dự án mới */}
            <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
                <DialogTitle>Tạo dự án mới</DialogTitle>
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
                        <Button onClick={handleCloseDialog}>Hủy</Button>
                        <Button type="submit" variant="contained">
                            Tạo dự án
                        </Button>
                    </DialogActions>
                </form>
            </Dialog>
        </Container>
    );
} 