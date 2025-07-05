import os
from datetime import timedelta

class Config:
    """Base configuration class."""
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Application settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Logging configuration
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'logs/webtest_framework.log'
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 10
    
    # Testing configuration
    MAX_LINKS_TO_CHECK = 30
    MAX_THREADS = 20
    REQUEST_TIMEOUT = 30  # seconds
    
    # ChromeDriver configuration
    CHROME_DRIVER_PATH = os.environ.get('CHROME_DRIVER_PATH') or r"C:\Users\SHREYA\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    
    # CORS configuration
    CORS_ORIGINS = [
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

class DevelopmentConfig(Config):
    """Development configuration."""
    
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    
    # Development-specific settings
    MAX_LINKS_TO_CHECK = 10  # Smaller limit for faster development
    MAX_THREADS = 5  # Fewer threads for development

class ProductionConfig(Config):
    """Production configuration."""
    
    # Production security settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'change-this-in-production'
    
    @classmethod
    def validate(cls):
        """Validate production configuration."""
        if cls.SECRET_KEY == 'change-this-in-production':
            raise ValueError("SECRET_KEY environment variable must be set in production")
    
    # Production performance settings
    MAX_LINKS_TO_CHECK = 50
    MAX_THREADS = 30
    REQUEST_TIMEOUT = 60
    
    # Production logging
    LOG_LEVEL = 'WARNING'
    
    # Production CORS - restrict to your domain
    CORS_ORIGINS = [
        os.environ.get('ALLOWED_ORIGIN', 'https://yourdomain.com')
    ]

class TestingConfig(Config):
    """Testing configuration."""
    
    TESTING = True
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    
    # Testing-specific settings
    MAX_LINKS_TO_CHECK = 5
    MAX_THREADS = 2
    REQUEST_TIMEOUT = 10
    
    # Use in-memory database for testing
    WTF_CSRF_ENABLED = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 