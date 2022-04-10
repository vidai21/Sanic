from sanic import Blueprint, response
from application.search.utils import search_many_users
from application.chat.utils import get_chats, get_user_chat, get_message_by_chat
from application.extensions.jwt import protected

search_blueprint = Blueprint('search', url_prefix='/search')

@search_blueprint.route("/user", methods=["GET"])
@protected
async def search_users(request):
    session = request.ctx.session
    query = request.args.get("query")
    users = await search_many_users(query, session)
    users_arr = []
    for user in users:
        users_arr.append(user.to_dict())
    return response.json({
        "success": True,
        "data": users_arr
    }, status=200)

@search_blueprint.route("/chat", methods=["GET"])
@protected
async def search_users(request):
    session = request.ctx.session
    me_id = request.ctx.user.get("user")["id"]
    query = request.args.get("query")
    check_search = await search_many_users(query, session)
    search_arr = []
    for s in check_search:
        search_arr.append(s.to_dict())

    chats = await get_chats(me_id, session)
    new_chats = []

    if chats is not None:
        for chat_member in chats:
            chat_member = await get_user_chat(chat_member.chat_id, me_id, session)
            if chat_member.member.to_dict() in search_arr:
                data = {
                    "chat": chat_member.to_dict(),
                    "member": chat_member.member.to_dict()
                }

                msg = await get_message_by_chat(chat_member.chat_id, session)
                latestMessage = None
                if msg is not None:
                    latestMessage = msg.to_dict()

                new_data = {
                        "latestMessage": latestMessage,
                        "chat_user": data
                    }
                new_chats.append(new_data)
            
    return response.json({
        "success": True,
        "data": new_chats
    }, status=200)