from sanic import Blueprint, response
from application.extensions.jwt import protected
from application.post.utils import (
    get_posts, get_images_by_post, get_post_by_id, 
    check_uploads_dir, upload_image, create_one_post, create_one_image, 
    update_one_post, delete_one_post,
    check_locked_post ,check_locked_user,
    )

post_blueprint = Blueprint('post', url_prefix='/post')

@post_blueprint.route("/", methods=["GET"])
async def get_all_posts(request):
    session = request.ctx.session
    async with session.begin():
        posts_arr = []
        posts = await get_posts(session)
        for post in posts:
            locked_user = await check_locked_user(post.author_id, session)
            if not locked_user:
                locked = await check_locked_post(post.id, session)
                if not locked:
                    urls = await get_images_by_post(post.id, session)
                    url_arr = []
                    for url in urls:
                        url_arr.append(url.url)
                    data = {
                        "post": post.to_dict(),
                        "author": post.author.to_dict(),
                        "images": url_arr
                    }
                    posts_arr.append(data)
        return response.json({
            "success": True,
            "data": posts_arr
        })

@post_blueprint.route("/<post_id>", methods=["GET"])
async def get_post(request, post_id):
    session = request.ctx.session
    async with session.begin():
        post = await get_post_by_id(post_id, session)
        locked_user = await check_locked_user(post.author_id, session)
        if not locked_user:
            locked = await check_locked_post(post.id, session)
            if not locked:
                urls = await get_images_by_post(post_id, session)
                url_arr = []
                for url in urls:
                    url_arr.append(url.url)

                data = {
                    "post": post.to_dict(),
                    "author": post.author.to_dict(),
                    "images": url_arr
                }
                return response.json({
                    "success": True,
                    "data": data
                }, status=200)
        return response.json({
                "success": False,
                "message": "this post has been locked"
            }, status=400)

@post_blueprint.route("/", methods=["POST"])
@protected
async def create_post(request):
    session = request.ctx.session
    post_body = request.form
    files = request.files.getlist('file')
    files_arr = []

    if files:
        await check_uploads_dir(request.app.config.get("UPLOAD"))
        for file in files:
            file_path = await upload_image(file, request.app.config.get("UPLOAD"))
            files_arr.append(file_path)
    new_post = await create_one_post(post_body, request.ctx.user.get("user")["id"], session)
    urls = []
    if files_arr != []:
        for f in files_arr:
            new_img = await create_one_image(f, new_post.id, session)
            urls.append(new_img.url)

    async with session.begin():
        post = await get_post_by_id(new_post.id, session)
        data = {
            "post": new_post.to_dict(),
            "author": post.author.to_dict(),
            "images": urls
        }
        if post is not None:
            return response.json({
                "success": True,
                "data": data
            })

@post_blueprint.route("/<post_id>", methods=["PUT"])
@protected
async def update_post(request, post_id):
    session = request.ctx.session
    async with session.begin():
        post = request.json
        locked = await check_locked_post(post_id, session)
        if not locked:
            await update_one_post(post, post_id, session)

            urls = await get_images_by_post(post_id, session)
            url_arr = []
            for url in urls:
                url_arr.append(url.url)

            post = await get_post_by_id(post_id, session)
            data = {
                "post": post.to_dict(),
                "author": post.author.to_dict(),
                "images": url_arr
            }
            return response.json({
                "success": True,
                "data": data
            }, status=200)
        return response.json({
            "success": False,
            "message": "this post has been locked"
        }, status=400)

@post_blueprint.route("/<post_id>", methods=["DELETE"])
@protected
async def delete_post(request, post_id):
    session = request.ctx.session
    async with session.begin():
        locked = await check_locked_post(post_id, session)
        if not locked:
            await delete_one_post(post_id, session)
            return response.json({
                "success": True,
                "message": "this post has been deleted!"
            }, status=200)
        return response.json({
            "success": False,
            "message": "this post has been locked"
        }, status=400)