from application.api import profile
from application.models.models import User, Post
from application.server import json
from sqlalchemy import desc, select

@profile.get("/<user_id>")
async def get_profile(request, user_id):
    session = request.ctx.session
    async with session.begin():
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        profile = result.scalar()
        if profile is not None:
            return json({
                "status": "success",
                "data": profile.to_dict()
            })

@profile.get("/posts/<user_id>")
async def get_posts_profile(request, user_id):
    session = request.ctx.session
    async with session.begin():
        stmt = select(Post, User).join(Post.author).where(Post.author_id == user_id).order_by(desc(Post.createdAt))
        result = await session.execute(stmt)
        posts = []
        for post in result.scalars():
            data = {
                "post": post.to_dict(),
                "author": post.author.to_dict()
            }
            posts.append(data)
        return json({
            "status": "success",
            "data": posts
        })