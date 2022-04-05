from calendar import c
from operator import and_
from application.api import chat
from application.server import json
from application.models.models import Chat, ChatMember, Message, User
from application.extensions.jwt import protected 
from sqlalchemy import desc, select, delete
from sqlalchemy.orm import selectinload

#get all chats
@chat.get("/")
@protected
async def get_all_chats(request):
    session = request.ctx.session
    meId = request.ctx.userId
    stmt_chats_member = select(ChatMember).where(ChatMember.member_id == meId).order_by(desc(ChatMember.updatedAt))
    result = await session.execute(stmt_chats_member)
    new_chats = []

    if result is not None:
        for chat_member in result.scalars():
            stmt_chat_user = select(ChatMember).where(and_(ChatMember.chat_id == chat_member.chat_id, ChatMember.member_id != meId)).options(selectinload(ChatMember.member))
            chat_user_result = await session.execute(stmt_chat_user)
            chat_member = chat_user_result.scalar()
            data = {
                "chat": chat_member.to_dict(),
                "member": chat_member.member.to_dict()
            }

            stmt_msg = select(Message).where(Message.chat_id == chat_member.chat_id).order_by(desc(Message.createdAt))
            result_msg = await session.execute(stmt_msg)
            msg = result_msg.scalar()
            latestMessage = None
            if msg is not None:
                latestMessage = msg.to_dict()

            new_data = {
                    "latestMessage": latestMessage,
                    "chat_user": data
                }
            new_chats.append(new_data)
            
    return json({
        "status": "success",
        "data": new_chats
    })

#create chat
@chat.post("/<user_id>")
@protected
async def create_chat(request, user_id):
    session = request.ctx.session
    stmt = select(ChatMember).where(ChatMember.member_id == request.ctx.userId)
    result = await session.execute(stmt)
    all_chat_member = result.scalars()
    fetch_chat = []

    if all_chat_member is not None:
        for c in all_chat_member:
            stmt1 = select(ChatMember).where(and_(ChatMember.member_id == user_id, ChatMember.chat_id == c.chat_id)).options(selectinload(ChatMember.member))
            result1 = await session.execute(stmt1)
            chat_member = result1.scalar()
            if chat_member is not None:
                data = {
                    "chat": chat_member.to_dict(),
                    "member": chat_member.member.to_dict()
                }
                fetch_chat.append(data)
    
    if fetch_chat == []:
        chat = Chat()
        session.add(chat)
        await session.commit()

        current_user_chat = ChatMember(member_id=request.ctx.userId, chat_id=chat.id)
        user_chat = ChatMember(member_id=user_id, chat_id=chat.id)
        session.add_all([current_user_chat, user_chat])
        await session.commit()

        async with session.begin():
            stmt2 = select(ChatMember).where(and_(ChatMember.member_id == user_id, ChatMember.chat_id == chat.id)).options(selectinload(ChatMember.member))
            result2 = await session.execute(stmt2)
            chat_member1 = result2.scalar()
            data = {
                "chat": chat_member1.to_dict(),
                "member": chat_member1.member.to_dict()
            }
            fetch_chat.append(data)

    new_data = {
        "latestMessage": None,
        "chat_user": fetch_chat
    }
    return json({
        "status": "success",
        "data": new_data
    })

#delete chat
@chat.delete("/<chat_id>")
@protected
async def delete_chat(request, chat_id):
    session = request.ctx.session
    async with session.begin():
        stmt = delete(Chat).where(Chat.id == chat_id)
        await session.execute(stmt)
        stmt_m = delete(Message).where(Message.chat_id == chat_id)
        await session.execute(stmt_m)
        stmt_c = delete(ChatMember).where(ChatMember.chat_id == chat_id)
        await session.execute(stmt_c)
        return json({
            "status": "success",
            "message": "this chat has been deleted!"
        })