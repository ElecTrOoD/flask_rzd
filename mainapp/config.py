# Импортируем все зависимости
import os

from dotenv import load_dotenv

# загружаем переменные окружения
load_dotenv()

ENV = os.getenv('FLASK_ENV')
DEBUG = os.getenv('FLASK_DEBUG')

SECRET_KEY = os.getenv('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOADED_PDF_DEST = os.path.join(os.getcwd(), os.getenv('UPLOADED_PDF_DEST'))
UPLOADED_PHOTO_DEST = os.path.join(os.getcwd(), os.getenv('UPLOADED_PHOTO_DEST'))

WTF_CSRF_ENABLED = True
