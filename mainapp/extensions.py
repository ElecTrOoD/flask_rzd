# Импортируем все зависимости
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_qrcode import QRcode
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

# получаем объекты расширений
login_manager = LoginManager()  # менеджер аутентификации и авторизации пользователей
db = SQLAlchemy()  # ORM для работы с базой данных
migrate = Migrate()  # система миграций в базу данных для создания и обновления моделей
csrf = CSRFProtect()  # CSRF защита форм
qr = QRcode()  # модуль для генерации QR-кодов
