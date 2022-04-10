from application.user.models import User
from application.post.models import Post
from sqlalchemy import desc, select
from sqlalchemy.orm import selectinload

async def get_user_by_id(id, session):
    stmt = select(User).where(User.id == id)
    result = await session.execute(stmt)
    profile = result.scalar()
    return profile

async def get_posts_by_user(id, session):
    stmt = select(Post).where(Post.author_id == id).order_by(desc(Post.createdAt)).options(selectinload(Post.author))
    result = await session.execute(stmt)
    posts = result.scalars()
    return posts