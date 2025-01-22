import os
from datetime import timedelta



class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
    DATABASE_URL = os.environ.get('DATABASE_URL', '')
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL is not set")
    SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace('postgres://', 'postgresql://')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False