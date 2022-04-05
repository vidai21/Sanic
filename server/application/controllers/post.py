from application.api import post
from application.models.models import Post, User, Image
from application.server import json, app
from application.extensions.jwt import protected
from sqlalchemy import desc, select, delete, update
from sqlalchemy.orm import selectinload
import aiofiles
import os
import datetime
import urllib.parse

@post.get("/")
async def get_all_posts(request):
    session = request.ctx.session
    async with session.begin():
        stmt = select(Post).order_by(desc(Post.createdAt)).options(selectinload(Post.author))
        result = await session.execute(stmt)
        posts = []
        for post in result.scalars():
            stmt1 = select(Image).where(Image.post_id == post.id).order_by(desc(Image.createdAt))
            result1 = await session.execute(stmt1)
            urls = result1.scalars()
            url_arr = []
            for url in urls:
                url_arr.append(url.url)
            data = {
                "post": post.to_dict(),
                "author": post.author.to_dict(),
                "images": url_arr
            }
            posts.append(data)
        return json({
            "status": "success",
            "data": posts
        })

@post.get("/<post_id>")
async def get_post(request, post_id):
    session = request.ctx.session
    async with session.begin():
        stmt = select(Post).where(Post.id == post_id).options(selectinload(Post.author))
        result = await session.execute(stmt)
        post = result.scalar()

        stmt1 = select(Image).where(Image.post_id == post.id).order_by(desc(Image.createdAt))
        result1 = await session.execute(stmt1)
        urls = result1.scalars()
        url_arr = []
        for url in urls:
            url_arr.append(url.url)

        data = {
            "post": post.to_dict(),
            "author": post.author.to_dict(),
            "images": url_arr
        }
        return json({
            "status": "success",
            "data": data
        })

@post.post("/")
@protected
async def create_post(request):
    session = request.ctx.session
    post_body = request.form
    files = request.files.getlist('file')
    files_arr = []

    if files:
        if not os.path.exists(app.config.get("UPLOAD")):
            os.makedirs(app.config.get("UPLOAD"))
        for i in files:
            file_parameters = {
                'body': i.body,
                'name': i.name,
                'type': i.type,
            }
            file_path = f'{app.config.get("UPLOAD")}/{str(datetime.datetime.now())}.{file_parameters["name"].split(".")[-1]}'
            file_path = urllib.parse.quote(file_path)
            files_arr.append(file_path)
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(file_parameters['body'])
            f.close()
            print('file wrote to disk')
    
    new_post = Post(content=post_body.get("content"), author_id=request.ctx.userId)
    session.add(new_post)
    await session.commit()
    urls = []
    if files_arr != []:
        for f in files_arr:
            new_img = Image(url=f, post_id=new_post.id)
            session.add(new_img)
            await session.commit()
            urls.append(new_img.url)

    async with session.begin():
        stmt = select(Post).where(Post.id == new_post.id).options(selectinload(Post.author))
        result = await session.execute(stmt)
        post = result.scalar()
        data = {
            "post": new_post.to_dict(),
            "author": post.author.to_dict(),
            "images": urls
        }
        if result is not None:
            return json({
                "status": "success",
                "data": data
            })

@post.put("/<post_id>")
@protected
async def update_post(request, post_id):
    session = request.ctx.session
    async with session.begin():
        post = request.json
        stmt = update(Post).where(Post.id == post_id).values(content=post["content"])
        await session.execute(stmt)

        stmt1 = select(Image).where(Image.post_id == post_id).order_by(desc(Image.createdAt))
        result1 = await session.execute(stmt1)
        urls = result1.scalars()
        url_arr = []
        for url in urls:
            url_arr.append(url.url)

        stmt_update = select(Post).where(Post.id == post_id).options(selectinload(Post.author))
        result = await session.execute(stmt_update)
        post = result.scalar()
        data = {
            "post": post.to_dict(),
            "author": post.author.to_dict(),
            "images": url_arr
        }
        return json({
            "status": "success",
            "data": data
        })

@post.delete("/<post_id>")
@protected
async def delete_post(request, post_id):
    session = request.ctx.session
    async with session.begin():
        stmt1 = delete(Image).where(Image.post_id == post_id)
        await session.execute(stmt1)
        stmt = delete(Post).where(Post.id == post_id)
        await session.execute(stmt)
        return json({
            "status": "success",
            "data": "this post has been deleted!"
        })