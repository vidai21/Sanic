from sanic import Blueprint, response
from application.extensions.jwt import protected
from application.admin.check_role import protected_admin
from application.admin.utils import (
    get_list_locked_posts, check_post, lock_one_post, unlock_one_post, 
    get_list_locked_users, check_user, lock_one_user, unlock_one_user
)
from application.post.utils import get_post_by_id, get_images_by_post

admin_blueprint = Blueprint('admin', url_prefix='/admin')

@admin_blueprint.route('/locked/post', methods=["GET"])
@protected
@protected_admin
async def lock_post_list(request):
    session = request.ctx.session
    async with session.begin():
        locked_list = await get_list_locked_posts(session)
        lists = []
        for locked in locked_list:
            post = await get_post_by_id(locked.post_id ,session)
            urls_arr = []
            urls = await get_images_by_post(post.id, session)
            for url in urls:
                urls_arr.append(url.url)
            data = {
                "locked": locked.to_dict(),
                "post": post.to_dict(),
                "author": post.author.to_dict(),
                "images": urls_arr
            }
            lists.append(data)
        return response.json({
            "success": True,
            "message": "here is list of locked posts",
            "data": lists
        }, status=200)

@admin_blueprint.route('/lock/post/<post_id>', methods=["POST"])
@protected
@protected_admin
async def lock_post(request, post_id):
    session = request.ctx.session
    locked = await check_post(post_id ,session)
    if not locked:
        new_lock = await lock_one_post(post_id, session)
        post = await get_post_by_id(new_lock.post_id ,session)
        data = {
            "locked": new_lock.to_dict(),
            "post": post.to_dict(),
            "author": post.author.to_dict()
        }
    else:
        post = await get_post_by_id(locked.post_id ,session)
        data = {
            "locked": locked.to_dict(),
            "post": post.to_dict(),
            "author": post.author.to_dict()
        }
    return response.json({
        "success": True,
        "message": "this post has been locked",
        "data": data
    }, status=200)

@admin_blueprint.route('/unlock/post/<post_id>', methods=["POST"])
@protected
@protected_admin
async def unlock_post(request, post_id):
    session = request.ctx.session
    async with session.begin():
        locked = await check_post(post_id ,session)
        if locked:
            unlocked = await unlock_one_post(post_id, session)
            if unlocked is False:
                return response.json({
                    "success": False,
                    "message": "error sql"
                }, status=400)
        else:
            return response.json({
                "success": False,
                "message": "this post is not locked"
            }, status=400)
        return response.json({
            "success": True,
            "message": "this post is unlocked",
        }, status=200)

@admin_blueprint.route('/locked/user', methods=["GET"])
@protected
@protected_admin
async def lock_user_list(request):
    session = request.ctx.session
    locked_list = await get_list_locked_users(session)
    lists = []
    for locked in locked_list:
        data = {
            "locked": locked.to_dict(),
            "user": locked.user.to_dict()
        }
        lists.append(data)
    return response.json({
        "success": True,
        "message": "here is list of locked users",
        "data": lists
    }, status=200)

@admin_blueprint.route('/lock/user/<user_id>', methods=["POST"])
@protected
@protected_admin
async def lock_user(request, user_id):
    session = request.ctx.session
    locked = await check_user(user_id ,session)
    if not locked:
        new_lock = await lock_one_user(user_id, session)
        user = await check_user(new_lock.user_id ,session)
        data = {
            "locked": new_lock.to_dict(),
            "user": user.user.to_dict()
        }
    else:
        data = {
            "locked": locked.to_dict(),
            "user": locked.user.to_dict()
        }
    return response.json({
        "success": True,
        "message": "this user has been locked",
        "data": data
    }, status=200)

@admin_blueprint.route('/unlock/user/<user_id>', methods=["POST"])
@protected
@protected_admin
async def unlock_user(request, user_id):
    session = request.ctx.session
    async with session.begin():
        locked = await check_user(user_id ,session)
        if locked:
            new_lock = await unlock_one_user(user_id, session)
            if new_lock is False:
                return response.json({
                    "success": False,
                    "message": "error sql"
                }, status=400)
        else:
            return response.json({
                "success": False,
                "message": "this user is not locked"
            }, status=400)
        return response.json({
            "success": True,
            "message": "this user is unlocked",
        }, status=200)