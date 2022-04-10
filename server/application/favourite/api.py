from sanic import Blueprint, response
from application.extensions.jwt import protected
from application.favourite.utils import (
    get_favourites_by_user, check_favourites_by_user, 
    add_one_favourite, get_favourite, delete_one_favourite)
from application.post.utils import get_post_by_id, get_images_by_post

favourite_blueprint = Blueprint('favourite', url_prefix='/favourite')


@favourite_blueprint.route("/", methods=["GET"])
@protected
async def get_all_favourites(request):
    session = request.ctx.session
    favourites = await get_favourites_by_user(request.ctx.user.get("user")["id"], session)
    favourites_arr = []
    for favourite in favourites:
        post = await get_post_by_id(favourite.post_id, session)
        urls_arr = []
        urls = await get_images_by_post(post.id, session)
        for url in urls:
            urls_arr.append(url.url)
        data = {
            "favourite": favourite.to_dict(),
            "post": favourite.post.to_dict(),
            "author": post.author.to_dict(),
            "images": urls_arr
        }
        favourites_arr.append(data)
    return response.json({
        "success": True,
        "data": favourites_arr
    }, status=200)

@favourite_blueprint.route("/<post_id>", methods=["POST"])
@protected
async def add_favourite(request, post_id):
    session = request.ctx.session
    favourite = await check_favourites_by_user(post_id, request.ctx.user.get("user")["id"], session)
    if favourite is None:
        new_favourite = await add_one_favourite(post_id, request.ctx.user.get("user")["id"], session)
        async with session.begin():
            favourite_selected = await get_favourite(new_favourite.id, session)
            data = {
                "favourite": favourite_selected.to_dict(),
                "post": favourite_selected.post.to_dict()
            }
    else:
        data = {
            "favourite": favourite.to_dict(),
            "post": favourite.post.to_dict()
        }
    return response.json({
            "success": True,
            "data": data
        }, status=200)

@favourite_blueprint.route("/<post_id>", methods=["DELETE"])
@protected
async def delete_favourite(request, post_id):
    session = request.ctx.session
    async with session.begin():
        try:
            await delete_one_favourite(post_id, session)
            return response.json({
                "success": True,
                "message": "this post has been deleted from your favourite!"
            }, status=200)
        except:
            return response.json({
                "status": False,
            }, status=400)