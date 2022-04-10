import socketio
from sanic import Sanic, Blueprint
from .config import Config

from application.user.api import user_blueprint
from application.profile.api import profile_blueprint
from application.post.api import post_blueprint
from application.messager.api import messager_blueprint
from application.favourite.api import favourite_blueprint
from application.chat.api import chat_blueprint
from application.admin.api import admin_blueprint
from application.search.api import search_blueprint

app = Sanic(name="SanicApp")
app.config.from_object(Config)
sio = socketio.AsyncServer(async_mode='sanic', cors_allowed_origins="*")
sio.attach(app)

import application.extensions.middleware

app.static("/uploads", "./uploads")

api = Blueprint.group(user_blueprint, profile_blueprint, post_blueprint, messager_blueprint, favourite_blueprint, chat_blueprint, admin_blueprint, search_blueprint, url_prefix="/api/v1")

app.blueprint(api)

import application.extensions.socketio