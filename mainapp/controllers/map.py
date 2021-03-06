# импортируем зависимости
from flask import Blueprint, render_template
from flask_login import login_required

from mainapp.models import User

# создаем и конфигурируем экземпляр "чертежа" приложения карты
map_c = Blueprint('map', __name__, url_prefix='/map', static_folder='../static')


# контроллер страницы карты. При обычном запросе возвращает карту с актуальными метками всех пользователей.
# Если в запросе передаётся ID конкретного пользователя, то возвращает карту с меткой только этого пользователя
@map_c.route('/')
@map_c.route('/<int:user_id>')
@login_required
def map_page(user_id=None):
    if user_id:
        data = [User.query.get(user_id)]
    else:
        data = User.query.all()
    map_info = [user.get_info_for_map() for user in data if user.geo_lat]
    return render_template('map/map.html', map_info=map_info)
