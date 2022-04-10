from sanic import Blueprint, response
from application.user.hash_password import hash_password
from application.extensions.jwt import protected
from application.user.utils import check_user, get_role, create_token, create_user, create_user_role

user_blueprint = Blueprint('user', url_prefix='/user')

@user_blueprint.route("/login", methods=["POST"])
async def login_auth(request):
    session = request.ctx.session
    async with session.begin():
        login = request.json
        user = await check_user(login.get("email"), session)
        if user is not None:
            hash = hash_password(str(login.get("password")).encode("utf-8"))
            if(user.password == hash):
                role = await get_role(user, session)
                token = await create_token(user, role, request.app.config.SECRET)
                if token is not None:
                    return response.json({
                        "success": True,
                        "message": "login is successfully!",
                        "data": user.to_dict(),
                        "token": token
                    })
            else:
                return response.json({
                    "success": False,
                    "message": "password is not correct!"
                })
        else:
            return response.json({
                "success": False,
                "message": "email do not exists!"
            })

@user_blueprint.route("/register", methods=["POST"])
async def register_auth(request):
    session = request.ctx.session
    register = request.json
    user = await check_user(register.get("email"), session)
    if user is None:
        register["password"] = hash_password(str(register["password"]).encode("utf-8"))
        user = await create_user(register, session)
        user_role = await create_user_role(user, session)
        if user is not None:
            token = await create_token(user, user_role, request.app.config.SECRET)
            return response.json({
                "success": True,
                "message": "your account has been successfully resgistered!",
                "data": user.to_dict(),
                "token": token
            })
    else:
        return response.json({
            "success": False,
            "message": "email already exists!"
        })  

@user_blueprint.route("/", methods=["GET"])
@protected
async def secret(request):
    user = request.ctx.user
    return response.json({
        "success": True,
        "data": user
    })
