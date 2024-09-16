from config import Config
from flask import Flask
from flask_socketio import SocketIO
from .messaging import Message
from .users import User
from redis_om import Migrator

Migrator().run()

app = Flask(__name__)
app.config.from_object(Config)
socketio = SocketIO(app)

from app import routes

if __name__ == '__main__':
    socketio.run(app)
