# Импортируем все зависимости
import re
from datetime import datetime

import requests
from flask_login import UserMixin

from mainapp.app import db


# класс модели пользователя
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    photo = db.Column(db.String(255), unique=True)
    geo_lat = db.Column(db.Float)
    geo_long = db.Column(db.Float)
    geo_updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    topicmessages = db.relationship('TopicMessage', cascade='all,delete', backref='users')
    topics = db.relationship('Topic', cascade='all,delete', backref='users')

    def __init__(self, username, first_name, last_name, photo, password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.photo = photo
        self.password = password

    # метод сериализации данных для карты
    def get_info_for_map(self):
        return {'username': self.username,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'geo_lat': self.geo_lat,
                'geo_long': self.geo_long,
                'geo_updated_at': self.geo_updated_at.strftime('%Y-%m-%dT%H:%M:%SZ')}


# класс модели технологической карты
class TechMap(db.Model):
    __tablename__ = 'techmaps'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    pdf = db.Column(db.String(255), unique=True)


# класс модели обучающего видео
class VideoTutorial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    link = db.Column(db.String(255), unique=True)
    thumbnail_link = db.Column(db.String(255), unique=True)

    def __init__(self, name, link):
        self.name = name
        self.link = self.get_embed_link(link)
        self.thumbnail_link = self.get_thumbnail_link(link)

    # метод получения ссылки на превью видео
    @staticmethod
    def get_thumbnail_link(value):
        if 'rutube' in value:
            video_id = re.search('video/+([\w\d]*)', value)[1]
            req_content = requests.get(f'http://rutube.ru/api/video/{video_id}/?format=xml').content.decode('utf-8')
            thumbnail_ur = re.search('<thumbnail_url>(.*)</thumbnail_url>', req_content)[1]
            return thumbnail_ur
        elif 'youtube' in value:
            video_id = re.search('\?v=+([\w\d]*)', value)[1]
            return f'https://img.youtube.com/vi/{video_id}/0.jpg'
        elif 'youtu.be' in value:
            video_id = re.search('be/+([\w\d]*)', value)[1]
            return f'https://img.youtube.com/vi/{video_id}/0.jpg'

    # метод получения встраиваемой ссылки
    @staticmethod
    def get_embed_link(value):
        rutube = 'https://rutube.ru/play/embed/'
        youtube = 'https://www.youtube.com/embed/'
        if 'rutube' in value:
            new_val = re.search('video/+([\w\d]*)', value)[1]
            return f'{rutube}{new_val}'
        elif 'youtube' in value:
            new_val = re.search('\?v=+([\w\d]*)', value)[1]
            return f'{youtube}{new_val}'
        elif 'youtu.be' in value:
            new_val = re.search('be/+([\w\d]*)', value)[1]
            return f'{youtube}{new_val}'


# класс модели сообщения в чате
class ChatMessage(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(255))
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    # метод сериализации данных в словарь
    def to_dict(self):
        return {'sender': self.sender, 'text': self.text, 'created_at': self.created_at.strftime('%Y-%m-%dT%H:%M:%SZ')}

    # метод получения последних 100 сообщений
    @classmethod
    def get_last_messages(cls):
        messages = cls.query.all()
        return [{'sender': x.sender, 'text': x.text, 'created_at': x.created_at.strftime('%Y-%m-%dT%H:%M:%SZ')}
                for x in messages[-100:]]


# класс модели категории форума
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(65), unique=True)
    description = db.Column(db.String(255))

    topics = db.relationship('Topic', cascade='all, delete', lazy=True, backref='categories', cascade_backrefs=False)

    def __init__(self, title, description):
        self.title = title
        self.description = description

    # метод получения даты и времени последнего сообщения
    def get_dates(self):
        return [x.messages[-1].created_at.strftime('%Y-%m-%dT%H:%M:%SZ') for x in self.topics]


# класс модели темы в категории
class Topic(db.Model):
    __tablename__ = 'topics'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(65), unique=True)
    description = db.Column(db.String(255))

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', back_populates='topics', overlaps='users')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete='cascade'), nullable=False)
    category = db.relationship('Category', back_populates='topics', lazy=True, overlaps='topics')
    messages = db.relationship('TopicMessage', cascade='all, delete', lazy=True, backref='topic')

    def __init__(self, title, description, category_id, author_id):
        self.title = title
        self.description = description
        self.category_id = category_id
        self.author_id = author_id

    # метод получения даты и времени последнего сообщения
    def get_dates(self):
        return [x.created_at.strftime('%Y-%m-%dT%H:%M:%SZ') for x in self.messages]


# класс модели сообщения в теме
class TopicMessage(db.Model):
    __tablename__ = 'topics_messages'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id', ondelete='cascade'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', back_populates='topicmessages', overlaps='users')

    def __init__(self, text, topic_id, author_id):
        self.text = text
        self.topic_id = topic_id
        self.author_id = author_id
