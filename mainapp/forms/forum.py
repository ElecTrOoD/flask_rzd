from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, TextAreaField, IntegerField, HiddenField


class CategoryForm(FlaskForm):
    title = StringField('Название', [validators.DataRequired(), validators.length(1, 65)])
    description = TextAreaField('Описание', [validators.DataRequired(), validators.length(1, 255)])
    submit = SubmitField('Создать')


class TopicForm(FlaskForm):
    title = StringField('Название', [validators.DataRequired(), validators.length(1, 65)])
    description = StringField('Описание', [validators.DataRequired(), validators.length(1, 255)])
    text = TextAreaField('Сообщение', [validators.DataRequired()])
    author_id = IntegerField([validators.DataRequired()])
    category_id = IntegerField([validators.DataRequired()])
    submit = SubmitField('Создать')


class TopicMessageForm(FlaskForm):
    text = TextAreaField('Сообщение', [validators.DataRequired()])
    author_id = IntegerField([validators.DataRequired()])
    topic_id = IntegerField([validators.DataRequired()])
    submit = SubmitField('Отправить')
