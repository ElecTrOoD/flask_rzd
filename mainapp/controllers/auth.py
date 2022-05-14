# импортируем зависимости
from datetime import timedelta

from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import logout_user, login_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from mainapp.extensions import db
from mainapp.forms.user import UserRegisterForm, UserLoginForm, photo
from mainapp.models import User

# создаем и конфигурируем экземпляр "чертежа" приложения авторизации
auth = Blueprint('auth', __name__, static_folder='../static')


# контроллер продливающий сессию пользователя при каждом новом запросе
@auth.before_request
def before_request():
    session.permanent = True
    auth.permanent_session_lifetime = timedelta(days=30)


# контроллер авторизации,  срабатывает при GET запросе на страницу авторизации. Отдаёт страницу авторизации.
# Если пользователь уже авторизован - перенаправляет на главную страницу
@auth.route('/login', methods=('GET',))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.tech_maps'))

    form = UserLoginForm(request.form)

    return render_template(
        'auth/login.html',
        form=form
    )


# контроллер авторизации, срабатывает при POST запросе на страницу авторизации.
# Если отправленные пользователем данные валидны - авторзует пользователя, иначе информирует пользователя о неверных данных
@auth.route('/login', methods=('POST',))
def login_post():
    form = UserLoginForm(request.form)
    user = User.query.filter_by(username=form.username.data).first()

    if not user or not check_password_hash(user.password, form.password.data):
        flash('Проверьте введенные данные')
        return redirect(url_for('.login'))

    login_user(user)
    return redirect(url_for('main.tech_maps'))


# контроллер регистрации, срабатывает при GET запросе на страницу регистрации. Отдаёт страницу регистрации.
# Если пользователь уже авторизован - перенаправляет на главную страницу
@auth.route('/register', methods=['GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.tech_maps'))

    form = UserRegisterForm(request.form)

    return render_template('auth/register.html', form=form)


# контроллер регистрации, срабатывает при POST запросе на страницу регистрации.
# Если отправленные пользователем данные валидны и такой пользователь ещё не зарегистрирован -
# создаёт новый объект пользователя, сохраняет запись в базе данных и авторизует пользователя, иначе информирует его об ошибке
@auth.route('/register', methods=['POST'])
def register_post():
    form = UserRegisterForm(request.form)
    errors = []
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).count():
            form.username.errors.append('Имя пользователя уже занято')
            return render_template('auth/register.html', form=form)
        photo_name = None
        if request.files['photo']:
            photo_name = photo.save(request.files['photo'])
        user = User(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            photo=photo_name,
            password=generate_password_hash(form.password.data)
        )

        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError:
            errors.append('Unexpected error. Try again.')
            return render_template('auth/register.html', form=form, errors=errors)
        else:
            login_user(user)
            return redirect(url_for('main.tech_maps'))

    else:
        return render_template('auth/register.html', form=form)


# контроллер деавторизующий пользователя
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.tech_maps'))
