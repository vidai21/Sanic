from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from application.extensions.base_model import BaseModel

class Chat(BaseModel):
    __tablename__ = "chats"

class ChatMember(BaseModel):
    __tablename__ = "chatmember"
    member_id = Column(ForeignKey("users.id"))
    member = relationship("User", foreign_keys=member_id)
    chat_id = Column(ForeignKey("chats.id"))
    chat = relationship("Chat", foreign_keys=chat_id)