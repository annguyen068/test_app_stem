from app import create_app, db
from app.models.user import User
from app.models.project import Project, Submission

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Cung cấp context cho flask shell command.
    Cho phép truy cập các đối tượng này trực tiếp khi chạy `flask shell`
    """
    return {
        'db': db, 
        'User': User, 
        'Project': Project, 
        'Submission': Submission
    }

if __name__ == '__main__':
    app.run(debug=True) 