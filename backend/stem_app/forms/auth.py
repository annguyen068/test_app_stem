from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from stem_app.models.user import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    remember_me = BooleanField('Ghi nhớ đăng nhập')
    submit = SubmitField('Đăng nhập')

class RegistrationForm(FlaskForm):
    username = StringField('Tên người dùng', validators=[
        DataRequired(),
        Length(min=3, max=64, message='Tên người dùng phải có độ dài từ 3 đến 64 ký tự')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Địa chỉ email không hợp lệ')
    ])
    password = PasswordField('Mật khẩu', validators=[
        DataRequired(),
        Length(min=6, message='Mật khẩu phải có ít nhất 6 ký tự')
    ])
    password2 = PasswordField('Xác nhận mật khẩu', validators=[
        DataRequired(),
        EqualTo('password', message='Mật khẩu xác nhận không khớp')
    ])
    is_teacher = SelectField('Vai trò', choices=[
        ('0', 'Học sinh'),
        ('1', 'Giáo viên')
    ], validators=[DataRequired()])
    submit = SubmitField('Đăng ký')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('Tên người dùng đã được sử dụng.')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('Email đã được sử dụng.') 