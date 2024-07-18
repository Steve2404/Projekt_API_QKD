import os
import secrets


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(16))
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', secrets.token_hex(16))
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///mydatabase.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
