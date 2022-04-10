from operator import and_
from application.favourite.models import Favourite
from sqlalchemy import desc, select, delete
from sqlalchemy.orm import selectinload

async def get_favourites_by_user(user_id, session):
    stmt = select(Favourite).where(Favourite.user_id == user_id).order_by(desc(Favourite.createdAt)).options(selectinload(Favourite.post))
    result = await session.execute(stmt)
    favourites = result.scalars()
    return favourites

async def check_favourites_by_user(post_id, user_id, session):
    stmt = select(Favourite).where(and_(Favourite.post_id == post_id, Favourite.user_id == user_id)).options(selectinload(Favourite.post))
    result = await session.execute(stmt)
    favourite = result.scalar()
    return favourite

async def add_one_favourite(post_id, user_id, session):
    new_favourite = Favourite(post_id=post_id, user_id=user_id)
    session.add(new_favourite)
    await session.commit()
    return new_favourite

async def get_favourite(favourite_id, session):
    stmt1 = select(Favourite).where(Favourite.id == favourite_id).options(selectinload(Favourite.post))
    result1 = await session.execute(stmt1)
    favourite_selected = result1.scalar()
    return favourite_selected

async def delete_one_favourite(post_id, session):
    stmt = delete(Favourite).where(Favourite.post_id == post_id)
    await session.execute(stmt)