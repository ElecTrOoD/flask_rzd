# импортируем зависимости
from flask import Blueprint, render_template
from flask_login import login_required

# создаем и конфигурируем экземпляр "чертежа" приложения чата
chat = Blueprint('chat', __name__, url_prefix='/chat', static_folder='../static')


# контроллер отдающий страницу чата. Требует авторизации
@chat.route('/')
@login_required
def chat_page():
    return render_template('chat/chat.html')
