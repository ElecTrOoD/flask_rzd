# Импортируем все зависимости

from datetime import timedelta

from flask import Flask
from flask_uploads import configure_uploads

from mainapp.extensions import db, migrate, csrf, login_manager, qr
from mainapp.forms.main import pdf
from mainapp.forms.user import photo
from mainapp.models import User


# функция создания экземпляра Flask приложения
def create_app() -> Flask:
    app = Flask(__name__)  # создаём экземпляр Flask приложения
    app.config.from_object('mainapp.config')  # загружаем параметры конфигурации из пакета config

    register_extensions(app)  # инициируем регистрацию расширений
    register_blueprints(app)  # инициируем регистрацию контроллеров,
    return app  # возвращаем сконфигурированный экземпляр Flask приложения


# функция регистрации расширений для Flask приложения
def register_extensions(app):
    db.init_app(app)  # инициализируем SQLAlchemy
    migrate.init_app(app, db, compare_type=True)  # инициализируем Flask-Migrate
    csrf.init_app(app)  # инициализируем Flask-CSRF
    qr.init_app(app)  # инициализируем Flask-QRCode

    login_manager.login_view = 'auth.login'  # конфигурируем контроллер авторизации
    login_manager.login_message = 'Войдите, чтобы получить доступ к этой странице.'  # конфигурируем сообщения авторизации
    login_manager.init_app(app)  # инициализируем Flask-Login
    app.permanent_session_lifetime = timedelta(days=30)  # конфигурируем время жизни сессии авторизации

    # инициализируем и конфигурируем модуль Flask-Uploads для загрузки фото и документов
    configure_uploads(app, pdf)
    configure_uploads(app, photo)

    # конфигурируем функцию получения объекта пользователя по id из сессии
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


# функция регистрации контроллеров
def register_blueprints(app: Flask):
    # импортируем контроллеры
    from mainapp.controllers.auth import auth
    import mainapp.controllers.main as m
    from mainapp.controllers.users import users
    from mainapp.controllers.map import map_c
    from mainapp.controllers.chat import chat
    from mainapp.controllers.forum import forum

    # регистрируем контроллеры
    app.register_blueprint(auth)
    app.register_blueprint(m.main)
    app.register_blueprint(users)
    app.register_blueprint(map_c)
    app.register_blueprint(chat)
    app.register_blueprint(forum)
