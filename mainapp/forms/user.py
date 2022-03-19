from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, validators, PasswordField, SubmitField

photo = UploadSet('photo', IMAGES)


class UserRegisterForm(FlaskForm):
    username = StringField('Имя пользователя', [validators.DataRequired(), validators.length(1, 25)])
    first_name = StringField('Имя', [validators.DataRequired(), validators.length(1, 50)])
    last_name = StringField('Фамилия', [validators.DataRequired(), validators.length(1, 50)])
    photo = FileField('Фото', validators=[
        FileAllowed(photo, 'Разрешены только картинки')
    ])
    password = PasswordField('Пароль', [validators.DataRequired(), validators.length(1, 25),
                                        validators.EqualTo('password_confirm',
                                                           message='Пароли должны совпадать')])
    password_confirm = PasswordField('Потдвердите пароль', [validators.DataRequired(), validators.length(1, 25)])
    submit = SubmitField('Зарегестрироваться')


class UserLoginForm(FlaskForm):
    username = StringField('Имя пользователя', [validators.DataRequired()])
    password = PasswordField('Пароль', [validators.DataRequired(), validators.length(1, 25)])
    submit = SubmitField('Войти')
