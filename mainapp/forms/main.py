# импортируем зависимости
from flask_uploads import UploadSet
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, validators, SubmitField, URLField

# конфигурируем экземпляр класса UploadSet. Он позволяет сохранять и валидировать загруженные пользователем PDF файлы
pdf = UploadSet('pdf', ('pdf',))


# форма технологической карты. Состоит из 2 полей: название, PDF файл загруженный пользователем
class TechMapForm(FlaskForm):
    name = StringField('Название', [validators.DataRequired(), validators.length(1, 255)])
    pdf = FileField('PDF файл', validators=[
        FileAllowed(pdf, 'Разрешены только .pdf файлы')
    ])
    submit = SubmitField('Создать')


# форма обучающего видео. Состоит из 2 полей: название, ссылка на видео
class VideoTutorialForm(FlaskForm):
    name = StringField('Название', [validators.DataRequired(), validators.length(1, 255)])
    link = URLField('Ссылка на видео', [validators.DataRequired(), validators.length(1, 500)])
    submit = SubmitField('Создать')


# форма QR-кода. Состоит только из ссылки на URL-адрес
class QRCodeForm(FlaskForm):
    link = URLField('Ссылка', [validators.DataRequired(), validators.length(1, 500)])
    submit = SubmitField('Сгенерировать')

