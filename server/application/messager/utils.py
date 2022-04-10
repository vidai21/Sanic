from application.messager.models import Message
from application.chat.models import ChatMember
from sqlalchemy import asc, select, delete, update
from sqlalchemy.orm import selectinload
from operator import and_

async def get_user_by_chat(chat_id, user_id, session):
    stmt2 = select(ChatMember).where(and_(ChatMember.chat_id == chat_id, ChatMember.member_id != user_id)).options(selectinload(ChatMember.member))
    result2 = await session.execute(stmt2)
    user = result2.scalar()
    return user

async def get_messages(chat_id, session):
    stmt = select(Message).where(Message.chat_id == chat_id).order_by(asc(Message.createdAt)).options(selectinload(Message.chat)).options(selectinload(Message.sender))
    result = await session.execute(stmt)
    messages = result.scalars()
    return messages

async def create_one_message(message, chat_id, user_id, session):
    new_message = Message(content=message["content"], chat_id=chat_id, sender_id=user_id)
    session.add(new_message)
    await session.commit()
    return new_message

async def update_latest_message(chat_id, session):
    stmt = update(ChatMember).where(ChatMember.chat_id == chat_id)
    await session.execute(stmt)