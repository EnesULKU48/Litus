import os
from pathlib import Path

# Temel yapılandırma
BASE_DIR = Path(__file__).parent
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR / "litus.db"}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Dosya yükleme ayarları
UPLOAD_FOLDER = BASE_DIR / 'static' / 'images' / 'products'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# Admin bilgileri
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'

