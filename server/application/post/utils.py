from sqlalchemy import desc, select, delete, true, update
from sqlalchemy.orm import selectinload
from application.post.models import Post, Image
from application.favourite.models import Favourite
from application.admin.models import LockedPost, LockedUser
import aiofiles
import os
import datetime

async def get_posts(session):
    stmt = select(Post).order_by(desc(Post.createdAt)).options(selectinload(Post.author))
    result = await session.execute(stmt)
    posts = result.scalars()
    return posts

async def get_images_by_post(post_id, session):
    stmt1 = select(Image).where(Image.post_id == post_id).order_by(desc(Image.createdAt))
    result1 = await session.execute(stmt1)
    urls = result1.scalars()
    return urls

async def get_post_by_id(post_id, session):
    stmt = select(Post).where(Post.id == post_id).options(selectinload(Post.author))
    result = await session.execute(stmt)
    post = result.scalar()
    return post

async def check_uploads_dir(upload):
    if not os.path.exists(upload):
        os.makedirs(upload)

async def upload_image(file, upload_config):
    file_parameters = {
        'body': file.body,
        'name': file.name,
        'type': file.type,
    }
    dt = datetime.datetime.now()
    file_path = f'{upload_config}/{str(datetime.datetime.timestamp(dt))}.{file_parameters["name"].split(".")[-1]}'
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(file_parameters['body'])
    f.close()
    print('file wrote to disk')
    return file_path

async def create_one_post(post_body, author_id, session):
    new_post = Post(content=post_body.get("content"), author_id=author_id)
    session.add(new_post)
    await session.commit()
    return new_post

async def create_one_image(file, post_id, session):
    new_img = Image(url=file, post_id=post_id)
    session.add(new_img)
    await session.commit()
    return new_img

async def update_one_post(post, post_id, session):
    stmt = update(Post).where(Post.id == post_id).values(content=post["content"])
    await session.execute(stmt)

async def delete_one_post(post_id, session):
    stmt2 = delete(Favourite).where(Favourite.post_id == post_id)
    await session.execute(stmt2)
    stmt1 = delete(Image).where(Image.post_id == post_id)
    await session.execute(stmt1)
    stmt = delete(Post).where(Post.id == post_id)
    await session.execute(stmt)

async def check_locked_post(post_id, session):
    stmt = select(LockedPost).where(LockedPost.post_id == post_id)
    result = await session.execute(stmt)
    locked = result.scalar()
    return locked

async def check_locked_user(user_id, session):
    stmt = select(LockedUser).where(LockedUser.user_id == user_id)
    result = await session.execute(stmt)
    lockeds = result.scalar()
    return lockeds