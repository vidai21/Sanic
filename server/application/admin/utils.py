from application.admin.models import LockedPost, LockedUser
from sqlalchemy import desc, select, delete
from sqlalchemy.orm import selectinload

async def get_list_locked_posts(session):
    stmt = select(LockedPost).order_by(desc(LockedPost.createdAt)).options(selectinload(LockedPost.post))
    result = await session.execute(stmt)
    lists = result.scalars()
    return lists

async def check_post(post_id, session):
    stmt = select(LockedPost).where(LockedPost.post_id == post_id).options(selectinload(LockedPost.post))
    result = await session.execute(stmt)
    locked = result.scalar()
    return locked

async def lock_one_post(post_id, session):
    locked = LockedPost(post_id=post_id)
    session.add(locked)
    await session.commit()
    return locked

async def unlock_one_post(post_id, session):
    try:
        stmt = delete(LockedPost).where(LockedPost.post_id == post_id)
        await session.execute(stmt)
        return True
    except:
        return False

async def get_list_locked_users(session):
    stmt = select(LockedUser).order_by(desc(LockedUser.createdAt)).options(selectinload(LockedUser.user))
    result = await session.execute(stmt)
    lists = result.scalars()
    return lists

async def check_user(user_id, session):
    stmt = select(LockedUser).where(LockedUser.user_id == user_id).options(selectinload(LockedUser.user))
    result = await session.execute(stmt)
    locked = result.scalar()
    return locked

async def lock_one_user(user_id, session):
    locked = LockedUser(user_id=user_id)
    session.add(locked)
    await session.commit()
    return locked

async def unlock_one_user(user_id, session):
    try:
        stmt = delete(LockedUser).where(LockedUser.user_id == user_id)
        await session.execute(stmt)
        return True
    except:
        return False