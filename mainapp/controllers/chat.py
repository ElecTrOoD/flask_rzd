from flask import Blueprint, render_template
from flask_login import login_required

from mainapp.extensions import csrf

chat = Blueprint('chat', __name__, url_prefix='/chat', static_folder='../static')


@chat.route('/')
@login_required
def chat_page():
    return render_template('chat/chat.html')
