from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, TextAreaField, SelectField, DateTimeField, FloatField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional, NumberRange, URL
from datetime import datetime

from app.models.user import User

class RegistrationForm(FlaskForm):
    """Form đăng ký người dùng
    
    Attributes:
        username: Tên người dùng (required)
        email: Email (required, định dạng email)
        password: Mật khẩu (required, ít nhất 6 ký tự)
        confirm_password: Xác nhận mật khẩu (phải trùng với password)
        role: Vai trò (student hoặc teacher)
        submit: Nút submit
    """
    username = StringField('Tên đăng nhập', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mật khẩu', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Xác nhận mật khẩu', 
                                    validators=[DataRequired(), EqualTo('password', message='Mật khẩu phải trùng khớp')])
    role = SelectField('Vai trò', choices=[('student', 'Học sinh'), ('teacher', 'Giáo viên')], validators=[DataRequired()])
    submit = SubmitField('Đăng ký')
    
    def validate_username(self, username):
        """Kiểm tra xem username đã tồn tại chưa
        
        Args:
            username: Field username cần kiểm tra
            
        Raises:
            ValidationError: Nếu username đã tồn tại
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Tên đăng nhập đã được sử dụng. Vui lòng chọn tên khác.')
            
    def validate_email(self, email):
        """Kiểm tra xem email đã tồn tại chưa
        
        Args:
            email: Field email cần kiểm tra
            
        Raises:
            ValidationError: Nếu email đã tồn tại
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email đã được sử dụng. Vui lòng sử dụng email khác.')


class LoginForm(FlaskForm):
    """Form đăng nhập
    
    Attributes:
        username: Tên đăng nhập (required)
        password: Mật khẩu (required)
        submit: Nút submit
    """
    username = StringField('Tên đăng nhập', validators=[DataRequired()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    submit = SubmitField('Đăng nhập')


class ProjectForm(FlaskForm):
    """Form tạo/chỉnh sửa dự án
    
    Attributes:
        title: Tiêu đề dự án (required)
        description: Mô tả chi tiết (required)
        deadline: Hạn nộp bài (required)
        submit: Nút submit
    """
    title = StringField('Tiêu đề', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Mô tả', validators=[DataRequired()])
    deadline = DateTimeField('Hạn nộp (YYYY-MM-DD HH:MM:SS)', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    submit = SubmitField('Lưu dự án')
    
    def validate_deadline(self, deadline):
        """Kiểm tra xem deadline có trong tương lai không
        
        Args:
            deadline: Field deadline cần kiểm tra
            
        Raises:
            ValidationError: Nếu deadline trong quá khứ
        """
        if deadline.data < datetime.utcnow():
            raise ValidationError('Hạn nộp phải nằm trong tương lai.')


class SubmissionForm(FlaskForm):
    """Form nộp bài
    
    Attributes:
        content: Nội dung bài nộp (optional)
        file: File bài nộp (jpg, jpeg, png, gif, pdf, doc, docx, ppt, pptx, zip) tối đa 100MB
        link: Link đến bài nộp (optional)
        submit: Nút submit
    """
    content = TextAreaField('Mô tả bài nộp', validators=[Optional()])
    file = FileField('File đính kèm (tối đa 100MB)', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx', 'ppt', 'pptx', 'zip'], 
                    'Chỉ cho phép các định dạng: jpg, jpeg, png, gif, pdf, doc, docx, ppt, pptx, zip')
    ])
    link = StringField('Link bài nộp', validators=[Optional(), URL(message='Link không hợp lệ')])
    submit = SubmitField('Nộp bài')
    
    def validate_file(self, file):
        """Kiểm tra xem có ít nhất một trong hai field content hoặc file
        
        Args:
            file: Field file cần kiểm tra
            
        Raises:
            ValidationError: Nếu cả content và file đều trống
        """
        if not file.data and not self.content.data:
            raise ValidationError('Vui lòng điền mô tả hoặc tải lên file.')


class GradeForm(FlaskForm):
    """Form chấm điểm bài nộp
    
    Attributes:
        score: Điểm số (0-10)
        feedback: Phản hồi cho học sinh
        submit: Nút submit
    """
    score = FloatField('Điểm (0-10)', validators=[
        DataRequired(), 
        NumberRange(min=0, max=10, message='Điểm phải từ 0 đến 10')
    ])
    feedback = TextAreaField('Phản hồi', validators=[Optional()])
    submit = SubmitField('Lưu điểm') 