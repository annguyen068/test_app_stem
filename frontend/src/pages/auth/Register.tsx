import { useState } from 'react';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import { useFormik } from 'formik';
import * as yup from 'yup';
import {
    Container,
    Box,
    Typography,
    TextField,
    Button,
    Link,
    Alert,
    Paper,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
} from '@mui/material';
import { useAuthStore } from '../../store/auth';

const validationSchema = yup.object({
    email: yup
        .string()
        .email('Email không hợp lệ')
        .required('Email là bắt buộc'),
    username: yup
        .string()
        .min(3, 'Tên đăng nhập phải có ít nhất 3 ký tự')
        .matches(/^[a-zA-Z0-9_]+$/, 'Tên đăng nhập chỉ được chứa chữ cái, số và dấu gạch dưới')
        .required('Tên đăng nhập là bắt buộc'),
    password: yup
        .string()
        .min(6, 'Mật khẩu phải có ít nhất 6 ký tự')
        .required('Mật khẩu là bắt buộc'),
    confirmPassword: yup
        .string()
        .oneOf([yup.ref('password')], 'Mật khẩu không khớp')
        .required('Xác nhận mật khẩu là bắt buộc'),
    role: yup
        .string()
        .oneOf(['teacher', 'student'], 'Vai trò không hợp lệ')
        .required('Vai trò là bắt buộc'),
});

export default function Register() {
    const navigate = useNavigate();
    const { register, error, isLoading } = useAuthStore();
    const [registerError, setRegisterError] = useState<string | null>(null);

    const formik = useFormik({
        initialValues: {
            email: '',
            username: '',
            password: '',
            confirmPassword: '',
            role: 'student',
        },
        validationSchema: validationSchema,
        onSubmit: async (values) => {
            try {
                await register(values.email, values.username, values.password, values.role as 'teacher' | 'student');
                navigate('/login');
            } catch (err: any) {
                setRegisterError(err.response?.data?.error || 'Đăng ký thất bại');
            }
        },
    });

    return (
        <Container component="main" maxWidth="xs">
            <Box
                sx={{
                    marginTop: 8,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}
            >
                <Paper
                    elevation={3}
                    sx={{
                        padding: 4,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        width: '100%',
                    }}
                >
                    <Typography component="h1" variant="h5">
                        Đăng ký tài khoản
                    </Typography>

                    {(error || registerError) && (
                        <Alert severity="error" sx={{ mt: 2, width: '100%' }}>
                            {error || registerError}
                        </Alert>
                    )}

                    <Box
                        component="form"
                        onSubmit={formik.handleSubmit}
                        sx={{ mt: 1, width: '100%' }}
                    >
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="email"
                            label="Email"
                            name="email"
                            autoComplete="email"
                            autoFocus
                            value={formik.values.email}
                            onChange={formik.handleChange}
                            error={formik.touched.email && Boolean(formik.errors.email)}
                            helperText={formik.touched.email && formik.errors.email}
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="username"
                            label="Tên đăng nhập"
                            name="username"
                            autoComplete="username"
                            value={formik.values.username}
                            onChange={formik.handleChange}
                            error={formik.touched.username && Boolean(formik.errors.username)}
                            helperText={formik.touched.username && formik.errors.username}
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="password"
                            label="Mật khẩu"
                            type="password"
                            id="password"
                            autoComplete="new-password"
                            value={formik.values.password}
                            onChange={formik.handleChange}
                            error={formik.touched.password && Boolean(formik.errors.password)}
                            helperText={formik.touched.password && formik.errors.password}
                        />
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            name="confirmPassword"
                            label="Xác nhận mật khẩu"
                            type="password"
                            id="confirmPassword"
                            value={formik.values.confirmPassword}
                            onChange={formik.handleChange}
                            error={formik.touched.confirmPassword && Boolean(formik.errors.confirmPassword)}
                            helperText={formik.touched.confirmPassword && formik.errors.confirmPassword}
                        />
                        <FormControl fullWidth margin="normal">
                            <InputLabel id="role-label">Vai trò</InputLabel>
                            <Select
                                labelId="role-label"
                                id="role"
                                name="role"
                                value={formik.values.role}
                                label="Vai trò"
                                onChange={formik.handleChange}
                                error={formik.touched.role && Boolean(formik.errors.role)}
                            >
                                <MenuItem value="student">Học sinh</MenuItem>
                                <MenuItem value="teacher">Giáo viên</MenuItem>
                            </Select>
                        </FormControl>
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                            disabled={isLoading}
                        >
                            {isLoading ? 'Đang đăng ký...' : 'Đăng ký'}
                        </Button>
                        <Box sx={{ textAlign: 'center' }}>
                            <Link component={RouterLink} to="/login" variant="body2">
                                Đã có tài khoản? Đăng nhập
                            </Link>
                        </Box>
                    </Box>
                </Paper>
            </Box>
        </Container>
    );
} 