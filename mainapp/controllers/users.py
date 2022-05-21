# импортируем зависимости
import os

from flask import Blueprint, render_template, redirect, url_for, send_from_directory
from flask_login import login_required

from mainapp.config import UPLOADED_PHOTO_DEST
from mainapp.extensions import db
from mainapp.models import User

# создаем и конфигурируем экземпляр "чертежа" приложения пользователей
users = Blueprint('users', __name__, url_prefix='/users', static_folder='../static')


# контроллер страницы пользователей. Отдаёт страницу со списком всех пользователей
@users.route('/')
def users_page():
    user_objects = User.query.all()
    dates = [user.geo_updated_at.strftime('%Y-%m-%dT%H:%M:%SZ') for user in user_objects]
    return render_template('users/users.html', users=user_objects, dates=dates)


# контроллер фотографии пользователя. Отдаёт файлом фотографию пользователя
@users.route('/uploads/<path:filename>')
def get_photo(filename):
    return send_from_directory(UPLOADED_PHOTO_DEST, filename, as_attachment=True)


# контроллер удаления пользователя
@users.route('/user_delete/<int:user_id>')
@login_required
def user_delete(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    if user.photo:
        os.remove(f'{UPLOADED_PHOTO_DEST}{user.photo}')
    return redirect(url_for('.users_page'))
