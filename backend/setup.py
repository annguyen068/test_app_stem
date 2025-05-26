from setuptools import setup, find_packages

setup(
    name="stem-app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-migrate',
        'flask-jwt-extended',
        'flask-cors',
        'flask-restx',
        'python-dotenv',
        'pytest',
        'werkzeug'
    ]
) 