from operator import and_
from application.user.models import User
from sqlalchemy import select

async def search_many_users(query, session):
    stmt = select(User).where(User.username.like("%"+ query + "%"))
    result = await session.execute(stmt)
    users = result.scalars()
    return users