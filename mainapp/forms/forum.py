# импортируем зависимости
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, TextAreaField, IntegerField


# форма категории форума. Состоит из 2 полей: название, описание
class CategoryForm(FlaskForm):
    title = StringField('Название', [validators.DataRequired(), validators.length(1, 65)])
    description = TextAreaField('Описание', [validators.DataRequired(), validators.length(1, 255)])
    submit = SubmitField('Создать')


# форма темы в категории форума. Состоит из 5 полей: название, описание, текст первого сообщения в теме,
#                                                    идентификатор автора темы, идентификатор категории
class TopicForm(FlaskForm):
    title = StringField('Название', [validators.DataRequired(), validators.length(1, 65)])
    description = StringField('Описание', [validators.DataRequired(), validators.length(1, 255)])
    text = TextAreaField('Сообщение', [validators.DataRequired()])
    author_id = IntegerField([validators.DataRequired()])
    category_id = IntegerField([validators.DataRequired()])
    submit = SubmitField('Создать')


# форма сообщения в теме форума. Состоит из 3 полей: текст сообщения, идентификатор автора сообщения, идентификатор темы
class TopicMessageForm(FlaskForm):
    text = TextAreaField('Сообщение', [validators.DataRequired()])
    author_id = IntegerField([validators.DataRequired()])
    topic_id = IntegerField([validators.DataRequired()])
    submit = SubmitField('Отправить')
