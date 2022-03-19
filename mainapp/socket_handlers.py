from wsgi import socketio
from datetime import datetime

from flask_socketio import emit

from .extensions import db
from .models import User, ChatMessage


@socketio.on('message')
def handle_message_event(json, methods=('GET', 'POST')):
    message = ChatMessage(sender=json['sender'], text=json['text'], created_at=datetime.utcnow())
    db.session.add(message)
    db.session.commit()
    socketio.emit('message_response', message.to_dict())


@socketio.on('get_messages')
def handle_get_messages_event(json, methods=('GET', 'POST')):
    response = ChatMessage.get_last_messages()
    emit('messages_list_response', {'data': response}, broadcast=False)


@socketio.on('delete_messages')
def handle_delete_messages_event(json, methods=('GET', 'POST')):
    ChatMessage.query.delete()
    db.session.commit()
    socketio.emit('refresh')


@socketio.on('location')
def handle_location_event(json, methods=('GET', 'POST')):
    user = User.query.get(json['user_id'])
    user.geo_lat, user.geo_long = json['latitude'], json['longitude']
    user.geo_updated_at = datetime.utcnow()
    db.session.add(user)
    db.session.commit()
