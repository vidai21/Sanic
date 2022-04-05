from application.api import auth
from application.models.models import User
from application.server import json
from application.extensions.hash_password import hash_password
from application.extensions.jwt import jwt, protected
from sqlalchemy import select

@auth.post("/login")
async def login_auth(request):
    session = request.ctx.session
    async with session.begin():
        login = request.json
        stmt = select(User).where(User.email == login.get("email"))
        result = await session.execute(stmt)
        user = result.scalar()
        if user is not None:
            hash = hash_password(str(login.get("password")).encode("utf-8"))
            if(user.password == hash):
                token = jwt.encode({"userId": user.id}, request.app.config.SECRET)
                if token is not None:
                    return json({
                        "status": "success",
                        "data": user.to_dict(),
                        "token": token
                    })
            else:
                return json({
                    "status": "failure",
                    "message": "password is not correct!"
                })
        else:
            return json({
                "status": "failure",
                "message": "email do not exists!"
            })

@auth.post("/register")
async def register_auth(request):
    session = request.ctx.session
    async with session.begin():
        register = request.json
        stmt = select(User).where(User.email == register["email"])
        result = await session.execute(stmt)
        user = result.scalar()
        if user is None:
            register["password"] = hash_password(str(register["password"]).encode("utf-8"))
            user = User(username=register["username"], password=register["password"], email=register["email"], phone=register["phone"])
            session.add(user)
            await session.commit()
            if user is not None:
                token = jwt.encode({"userId": user.id}, request.app.config.SECRET)
                return json({
                    "status": "success",
                    "data": user.to_dict(),
                    "token": token
                })
        else:
            return json({
                "status": "failure",
                "message": "email already exists!"
            })  

@auth.get("/")
@protected
async def secret(request):
    session = request.ctx.session
    async with session.begin():
        stmt = select(User).where(User.id == request.ctx.userId)
        result = await session.execute(stmt)
        user = result.scalar()
        return json({
            "status": "success",
            "data": user.to_dict()
        })

