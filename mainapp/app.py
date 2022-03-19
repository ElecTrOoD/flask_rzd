from datetime import timedelta

from flask import Flask
from flask_uploads import configure_uploads

from mainapp.extensions import db, migrate, csrf, login_manager, qr
from mainapp.forms.main import pdf
from mainapp.forms.user import photo
from mainapp.models import User


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object('mainapp.config')

    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    csrf.init_app(app)
    qr.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Войдите, чтобы получить доступ к этой странице.'
    login_manager.init_app(app)
    app.permanent_session_lifetime = timedelta(days=30)

    configure_uploads(app, pdf)
    configure_uploads(app, photo)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app: Flask):
    from mainapp.controllers.auth import auth
    import mainapp.controllers.main as m
    from mainapp.controllers.users import users
    from mainapp.controllers.map import map_c
    from mainapp.controllers.chat import chat
    from mainapp.controllers.forum import forum

    app.register_blueprint(auth)
    app.register_blueprint(m.main)
    app.register_blueprint(users)
    app.register_blueprint(map_c)
    app.register_blueprint(chat)
    app.register_blueprint(forum)
