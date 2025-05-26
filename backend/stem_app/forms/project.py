from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

class ProjectForm(FlaskForm):
    title = StringField('Tiêu đề', validators=[
        DataRequired(message='Tiêu đề không được để trống'),
        Length(min=3, max=100, message='Tiêu đề phải có độ dài từ 3 đến 100 ký tự')
    ])
    
    description = TextAreaField('Mô tả', validators=[
        DataRequired(message='Mô tả không được để trống'),
        Length(min=10, message='Mô tả phải có ít nhất 10 ký tự')
    ])
    
    requirements = TextAreaField('Yêu cầu', validators=[
        Length(max=2000, message='Yêu cầu không được vượt quá 2000 ký tự')
    ])
    
    deadline = DateTimeField('Hạn nộp', validators=[
        DataRequired(message='Hạn nộp không được để trống')
    ], format='%Y-%m-%dT%H:%M')
    
    submit = SubmitField('Lưu dự án')
    
    def validate_deadline(self, field):
        if field.data < datetime.now():
            raise ValidationError('Hạn nộp không thể nằm trong quá khứ') 