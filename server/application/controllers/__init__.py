from ntpath import join
from sanic_motor import BaseModel
from application.server import json

def init_controllers(app):
    import application.controllers.favourite
    import application.controllers.post
    import application.controllers.user
    import application.controllers.profile
    import application.controllers.chat
    import application.controllers.messager

    @app.route('/')
    def index(request):
        return join("ok")