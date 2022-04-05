from sanic import Blueprint

auth = Blueprint("auth", url_prefix="/auth")
profile = Blueprint("profile", url_prefix="/profile")
favourite = Blueprint("favourite", url_prefix="/favourite")
post = Blueprint("post", url_prefix="/post")
chat = Blueprint("chat", url_prefix="/chat")
messager = Blueprint("messager", url_prefix="/messager")

api = Blueprint.group(auth, profile, favourite, post, chat, messager, url_prefix="/api/v1")

def init_api(app):
    app.blueprint(api)