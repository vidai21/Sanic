from operator import and_
from application.chat.models import Chat, ChatMember
from application.messager.models import Message
from sqlalchemy import desc, select, delete
from sqlalchemy.orm import selectinload

async def get_chats(me_id, session):
    stmt = select(ChatMember).where(ChatMember.member_id == me_id).order_by(desc(ChatMember.updatedAt))
    result = await session.execute(stmt)
    chats = result.scalars()
    return chats

async def get_user_chat(chat_id, me_id, session):
    stmt = select(ChatMember).where(and_(ChatMember.chat_id == chat_id, ChatMember.member_id != me_id)).options(selectinload(ChatMember.member))
    result = await session.execute(stmt)
    chat_member = result.scalar()
    return chat_member
    

async def get_message_by_chat(chat_id, session):
    stmt = select(Message).where(Message.chat_id == chat_id).order_by(desc(Message.createdAt))
    result = await session.execute(stmt)
    msg = result.scalar()
    return msg

async def check_user_by_chat_member(user_id, chat_id, session):
    stmt = select(ChatMember).where(and_(ChatMember.member_id == user_id, ChatMember.chat_id == chat_id)).options(selectinload(ChatMember.member))
    result = await session.execute(stmt)
    chat_member = result.scalar()
    return chat_member

async def create_one_chat(me_id, user_id, session):
    chat = Chat()
    session.add(chat)
    await session.commit()

    current_user_chat = ChatMember(member_id=me_id, chat_id=chat.id)
    user_chat = ChatMember(member_id=user_id, chat_id=chat.id)
    session.add_all([current_user_chat, user_chat])
    await session.commit()
    return chat

async def delete_one_chat(chat_id, session):
    stmt = delete(Chat).where(Chat.id == chat_id)
    await session.execute(stmt)
    stmt_m = delete(Message).where(Message.chat_id == chat_id)
    await session.execute(stmt_m)
    stmt_c = delete(ChatMember).where(ChatMember.chat_id == chat_id)
    await session.execute(stmt_c)