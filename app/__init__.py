from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import os

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
socketio = SocketIO(app)

from app import routes, models
