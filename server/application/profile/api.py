from sanic import Blueprint, response
from application.profile.utils import get_user_by_id, get_posts_by_user
from application.post.utils import get_images_by_post, check_locked_user
profile_blueprint = Blueprint('profile', url_prefix='/profile')

@profile_blueprint.route("/<user_id>", methods=["GET"])
async def get_profile(request, user_id):
    session = request.ctx.session
    async with session.begin():
        locked = await check_locked_user(user_id, session)
        if not locked:
            profile = await get_user_by_id(user_id, session)
            if profile is not None:
                return response.json({
                    "success": True,
                    "data": profile.to_dict()
                }, status=200)
        return response.json({
                "success": False,
                "message": "this user has been locked"
            }, status=400)

@profile_blueprint.route("/post/<user_id>", methods=["GET"])
async def get_posts_profile(request, user_id):
    session = request.ctx.session
    async with session.begin():
        locked = await check_locked_user(user_id, session)
        if not locked:
            posts = await get_posts_by_user(user_id, session)
            posts_arr = []
            for post in posts:
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
        return response.json({
                "success": False,
                "message": "this user has been locked"
            }, status=400)