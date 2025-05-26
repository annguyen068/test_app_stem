from flask import current_app
from flask_mail import Message
from threading import Thread
from app import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('Đặt lại mật khẩu',
               sender=current_app.config['MAIL_DEFAULT_SENDER'],
               recipients=[user.email],
               text_body=f'''Để đặt lại mật khẩu, vui lòng truy cập link sau:
{url_for('auth.reset_password', token=token, _external=True)}

Nếu bạn không yêu cầu đặt lại mật khẩu, vui lòng bỏ qua email này.
''',
               html_body=f'''
<p>Để đặt lại mật khẩu, vui lòng click vào link sau:</p>
<p><a href="{url_for('auth.reset_password', token=token, _external=True)}">
    Đặt lại mật khẩu
</a></p>
<p>Nếu bạn không yêu cầu đặt lại mật khẩu, vui lòng bỏ qua email này.</p>
''') 