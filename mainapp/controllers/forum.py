# импортируем зависимости
from sqlite3 import IntegrityError

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from mainapp.extensions import db
from mainapp.forms.forum import CategoryForm, TopicForm, TopicMessageForm
from mainapp.models import Category, Topic, TopicMessage

# создаем и конфигурируем экземпляр "чертежа" приложения форума
forum = Blueprint('forum', __name__, url_prefix='/forum', static_folder='../static')


# контроллер главной страницы форума, отдает страницу с категориями форума
@forum.route('/', )
@login_required
def categories():
    category_objects = Category.query.all()
    return render_template('forum/categories.html', categories=category_objects)


# контроллер страницы отдельной категории форума, отдает страницу с темами выбранной категории
@forum.route('/<string:category_title>/', )
@login_required
def topics(category_title):
    category = Category.query.filter_by(title=category_title).first_or_404()
    return render_template('forum/topics.html', category=category, dates=category.get_dates())


# контроллер страницы отдельной темы форума, отдает страницу с сообщениями выбранной темы отдельной категории форума
@forum.route('/<string:category_title>/t/<string:topic_title>/', )
@login_required
def topic(category_title, topic_title):
    topic_obj = Topic.query.filter_by(title=topic_title).first_or_404()
    form = TopicMessageForm(author_id=current_user.id, topic_id=topic_obj.id)
    return render_template('forum/topic.html', topic=topic_obj, dates=topic_obj.get_dates(), form=form)


# контроллер публикации сообщения в теме форума, срабатывает при POST запросе. Принимает и валидирует данные с формы.
# Если данные валидны, создаёт новое сообщение
@forum.route('/<string:category_title>/t/<string:topic_title>/', methods=['POST'])
@login_required
def topic_post(category_title, topic_title):
    form = TopicMessageForm()
    errors = []
    if form.validate_on_submit():
        message = TopicMessage(
            text=form.text.data,
            topic_id=form.topic_id.data,
            author_id=form.author_id.data
        )

        db.session.add(message)
        try:
            db.session.commit()
        except IntegrityError:
            errors.append('Неизвестная ошибка. Попробуйте снова.')
            return render_template('forum/topic.html', form=form, errors=errors)
        else:
            return redirect(url_for('.topic', category_title=category_title, topic_title=topic_title))

    else:
        return render_template('forum/topic.html', form=form)


# контроллер страницы публикации категории форума, отдаёт форму создания категории
@forum.route('/create', )
@login_required
def create_category():
    form = CategoryForm()
    return render_template('forum/create_category.html', form=form)


# контроллер страницы публикации категории форума, срабатывает при POST запросе. Принимает и валидирует данные с формы.
# Если данные валидны, создаёт новую категорию
@forum.route('/create', methods=['POST'])
@login_required
def create_category_post():
    form = CategoryForm()
    errors = []
    if form.validate_on_submit():
        if Category.query.filter_by(title=form.title.data).count():
            form.title.errors.append('Введите уникальное название')
            return render_template('forum/create_category.html', form=form)
        category = Category(
            title=form.title.data,
            description=form.description.data,
        )

        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            errors.append('Неизвестная ошибка. Попробуйте снова.')
            return render_template('forum/create_category.html', form=form, errors=errors)
        else:
            return redirect(url_for('forum.categories'))

    else:
        return render_template('forum/create_category.html', form=form)


# контроллер страницы публикации темы форума, отдаёт форму создания темы
@forum.route('/<string:category_title>/create', )
@login_required
def create_topic(category_title):
    category = Category.query.filter_by(title=category_title).first_or_404()
    form = TopicForm(author_id=current_user.id, category_id=category.id)
    return render_template('forum/create_topic.html', form=form, category=category)


# контроллер страницы публикации темы форума, срабатывает при POST запросе. Принимает и валидирует данные с формы.
# Если данные валидны, создаёт новую тему
@forum.route('/<string:category_title>/create', methods=['POST'])
@login_required
def create_topic_post(category_title):
    form = TopicForm()
    errors = []
    if form.validate_on_submit():
        if Topic.query.filter_by(title=form.title.data).count():
            form.title.errors.append('Введите уникальное название')
            return render_template('forum/create_topic.html', form=form)
        topic_obj = Topic(
            title=form.title.data,
            description=form.description.data,
            category_id=form.category_id.data,
            author_id=form.author_id.data
        )

        db.session.add(topic_obj)
        try:
            db.session.commit()
            topic_obj = Topic.query.filter_by(title=form.title.data).first_or_404()
            message = TopicMessage(
                text=form.text.data,
                topic_id=topic_obj.id,
                author_id=form.author_id.data
            )
            db.session.add(message)
            db.session.commit()
        except IntegrityError:
            errors.append('Неизвестная ошибка. Попробуйте снова.')
            return render_template('forum/create_topic.html', form=form, errors=errors)
        else:
            return redirect(url_for('forum.topic', category_title=category_title, topic_title=form.title.data))

    else:
        return render_template('forum/create_topic.html', form=form)


@forum.route('/message_delete/<int:message_id>')
@login_required
def delete_message(message_id):
    message = TopicMessage.query.get(message_id)
    topic_obj = Topic.query.get(message.topic_id)
    db.session.delete(message)
    db.session.commit()
    return redirect(url_for('.topic', category_title=topic_obj.category.title, topic_title=topic_obj.title))


@forum.route('/topic_delete/<int:topic_id>')
@login_required
def delete_topic(topic_id):
    topic_obj = Topic.query.get(topic_id)
    db.session.delete(topic_obj)
    db.session.commit()
    return redirect(url_for('.topics', category_title=topic_obj.category.title))
