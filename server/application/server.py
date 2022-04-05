import socketio
from sanic import Sanic
from .config import Config
from sanic.response import json, text, file

app = Sanic(name="mySanicApp")
app.config.from_object(Config)
sio = socketio.AsyncServer(async_mode='sanic', cors_allowed_origins="*")
sio.attach(app)

#from application.extensions import init_extentions
from application.controllers import init_controllers
from application.api import init_api
# import application.extensions.middleware

#init_extentions(app)
init_controllers(app)
init_api(app)

if app.config.get("ENV") == "production":
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print("////", parentdir)
    @app.get('*')
    async def dir(request):
        return file(parentdir)