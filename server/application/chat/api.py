from sanic import Blueprint, response
from application.extensions.jwt import protected
from application.chat.utils import get_chats, get_user_chat, get_message_by_chat, check_user_by_chat_member, create_one_chat, delete_one_chat

chat_blueprint = Blueprint('chat', url_prefix='/chat')

#get all chats
@chat_blueprint.route("/", methods=["GET"])
@protected
async def get_all_chats(request):
    session = request.ctx.session
    me_id = request.ctx.user.get("user")["id"]
    chats = await get_chats(me_id, session)
    new_chats = []

    if chats is not None:
        for chat_member in chats:
            chat_member = await get_user_chat(chat_member.chat_id, me_id, session)
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

#create chat
@chat_blueprint.route("/<user_id>", methods=["POST"])
@protected
async def create_chat(request, user_id):
    session = request.ctx.session
    all_chat_member = await get_chats(request.ctx.user.get("user")["id"], session)
    fetch_chat = []

    if all_chat_member is not None:
        for c in all_chat_member:
            chat_member = await check_user_by_chat_member(user_id, c.chat_id, session)
            if chat_member is not None:
                data = {
                    "chat": chat_member.to_dict(),
                    "member": chat_member.member.to_dict()
                }
                fetch_chat.append(data)
    
    if fetch_chat == []:
        chat = await create_one_chat(request.ctx.user.get("user")["id"], user_id, session)

        async with session.begin():
            chat_member1 = await get_user_chat(chat.id, user_id, session)
            data = {
                "chat": chat_member1.to_dict(),
                "member": chat_member1.member.to_dict()
            }
            fetch_chat.append(data)

    new_data = {
        "latestMessage": None,
        "chat_user": fetch_chat
    }
    return response.json({
        "success": True,
        "data": new_data
    }, status=200)

#delete chat
@chat_blueprint.route("/<chat_id>", methods=["DELETE"])
@protected
async def delete_chat(request, chat_id):
    session = request.ctx.session
    async with session.begin():
        await delete_one_chat()
        return response.json({
            "success": True,
            "message": "this chat has been deleted!"
        }, status=200)