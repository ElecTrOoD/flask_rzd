from gevent import monkey

monkey.patch_all()

from flask_socketio import SocketIO
from mainapp.app import create_app
import logging

app = create_app()

logging.basicConfig(filename='info.log',level=logging.INFO)
logging.basicConfig(filename='error.log',level=logging.ERROR)

socketio = SocketIO(app, ping_timeout=20)

import mainapp.socket_handlers

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=9999)
    # socketio.run(app, host='0.0.0.0', port=9999)
