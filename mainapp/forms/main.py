from flask_uploads import UploadSet
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, validators, SubmitField, URLField

pdf = UploadSet('pdf', ('pdf',))


class TechMapForm(FlaskForm):
    name = StringField('Название', [validators.DataRequired(), validators.length(1, 255)])
    pdf = FileField('PDF файл', validators=[
        FileAllowed(pdf, 'Разрешены только .pdf файлы')
    ])
    submit = SubmitField('Создать')


class VideoTutorialForm(FlaskForm):
    name = StringField('Название', [validators.DataRequired(), validators.length(1, 255)])
    link = URLField('Ссылка на видео', [validators.DataRequired(), validators.length(1, 500)])
    submit = SubmitField('Создать')


class QRCodeForm(FlaskForm):
    link = URLField('Ссылка', [validators.DataRequired(), validators.length(1, 500)])
    submit = SubmitField('Сгенерировать')

