from gevent import monkey

monkey.patch_all()

from flask_socketio import SocketIO

from mainapp.app import create_app

app = create_app()
socketio = SocketIO(app,debug=True, ping_timeout=20)

import mainapp.socket_handlers


