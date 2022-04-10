from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from application.extensions.base_model import BaseModel

class Message(BaseModel):
    __tablename__ = "messages"
    content = Column(String(255))
    chat_id = Column(ForeignKey("chats.id"))
    chat = relationship("Chat", foreign_keys=chat_id)
    sender_id = Column(ForeignKey("users.id"))
    sender = relationship("User", foreign_keys=sender_id)