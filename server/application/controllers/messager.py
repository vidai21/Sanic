from operator import and_
from application.api import messager
from application.models.models import Message, Chat, User, ChatMember
from application.server import json
from application.extensions.jwt import protected 
from sqlalchemy import asc, select, delete, update
from sqlalchemy.orm import selectinload


@messager.get("/<chat_id>")
@protected
async def get_all_messages(request, chat_id):
    session = request.ctx.session
    async with session.begin():
        stmt2 = select(ChatMember).where(and_(ChatMember.chat_id == chat_id, ChatMember.member_id != request.ctx.userId)).options(selectinload(ChatMember.member))
        result2 = await session.execute(stmt2)
        m = result2.scalar()
        member = m.member.to_dict()

        stmt = select(Message, Chat, User).join(Message.chat).join(Message.sender).where(Message.chat_id == chat_id).order_by(asc(Message.createdAt)).options(selectinload(Message.chat)).options(selectinload(Message.sender))
        result = await session.execute(stmt)
        
        message = []
        for msg in result.scalars():
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
        return json({
                "status": "success",
                "data": data
            })

@messager.post("/<chat_id>")
@protected
async def create_message(request, chat_id):
    session = request.ctx.session
    message = request.json
    new_message = Message(content=message["content"], chat_id=chat_id, sender_id=request.ctx.userId)
    session.add(new_message)
    await session.commit()
    async with session.begin():
        stmt = update(ChatMember).where(ChatMember.chat_id == chat_id)
        await session.execute(stmt)

        select_stmt = select(Chat).where(Chat.id == chat_id)
        result_select = await session.execute(select_stmt)
        selected_chat = result_select.scalar()
        data = {
            "message": new_message.to_dict(),
            "chat": selected_chat.to_dict()
        }
        return json({
            "status": "success",
            "data": data
        })