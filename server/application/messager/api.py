from sanic import Blueprint, response
from application.extensions.jwt import protected
from application.messager.utils import get_user_by_chat, get_messages, create_one_message, update_latest_message

messager_blueprint = Blueprint('messager', url_prefix='/messager')


@messager_blueprint.route("/<chat_id>", methods=["GET"])
@protected
async def get_all_messages(request, chat_id):
    session = request.ctx.session
    async with session.begin():
        m = await get_user_by_chat(chat_id, request.ctx.user.get("user")["id"], session)
        member = m.member.to_dict()

        messages = await get_messages(chat_id, session)
        
        message = []
        for msg in messages:
            m = {
                "messages": msg.to_dict(),
                "sender": msg.sender.to_dict()
            }
            message.append(m)
        if len(message) > 0:
            data = {
                "message": message,
                "member": member,
                "lenght": len(message)
            }
        else:
            data = {
                "member": member,
                "lenght": 0
            }
        return response.json({
                "status": "success",
                "data": data
            })

@messager_blueprint.route("/<chat_id>", methods=["POST"])
@protected
async def create_message(request, chat_id):
    session = request.ctx.session
    message = request.json
    new_message = await create_one_message(message, chat_id, request.ctx.user.get("user")["id"], session)
    async with session.begin():
        await update_latest_message(chat_id, session)

        data = {
            "message": new_message.to_dict(),
        }
        return response.json({
            "status": "success",
            "data": data
        })