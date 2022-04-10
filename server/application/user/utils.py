from sqlalchemy import select
from application.user.models import User
from application.role.models import UserRole
from application.extensions.jwt import jwt

async def check_user(email, session):
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    user = result.scalar()
    return user

async def get_role(user, session):
    stmt1 = select(UserRole).where(UserRole.user_id == user.id)
    result1 = await session.execute(stmt1)
    role = result1.scalar()
    return role

async def create_token(user, role, secret):
    token = jwt.encode({"user": user.to_dict(), "role": role.role_id}, secret)
    return token

async def create_user(register, session):
    try:
        user = User(username=register["username"], password=register["password"], email=register["email"], phone=register["phone"])
        session.add(user)
        await session.commit()
        return user
    except:
        print("error")

async def create_user_role(user, session):
    try:
        user_role = UserRole(role_id=3, user_id=user.id)
        session.add(user_role)
        await session.commit()
        return user_role
    except:
        print("error")