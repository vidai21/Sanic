from datetime import datetime
from sqlalchemy import INTEGER, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship, declarative_base
import uuid

Base = declarative_base()

def create_uuid():
    return str(uuid.uuid4())

class BaseModel(Base):
    __abstract__ = True
    id = Column(String(255), primary_key=True, default=create_uuid)
    createdAt = Column(DateTime, default=datetime.now)
    updatedAt = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class User(BaseModel):
    __tablename__ = "users"
    username = Column(String(50))
    password = Column(String(255))
    email = Column(String(50))
    phone = Column(String(10))
    def to_dict(self):
        return {"id": self.id, "createdAt": str(self.createdAt), 
        "username": self.username, "password": self.password, "email": self.email, "phone": self.phone}

class Post(BaseModel):
    __tablename__ = "posts"
    content = Column(String(255))
    author_id = Column(ForeignKey("users.id"))
    author = relationship("User", foreign_keys=author_id)
    def to_dict(self):
        return {"id": self.id, "createdAt": str(self.createdAt), 
        "content": self.content, "author_id": self.author_id}

class Image(BaseModel):
    __tablename__ = "images"
    url= Column(String(255))
    post_id = Column(ForeignKey("posts.id"))
    post = relationship("Post", foreign_keys=post_id)
    def to_dict(self):
        return {"id": self.id, "createdAt": str(self.createdAt), 
        "url": self.url, "post_id": self.post_id}

class ChatMember(BaseModel):
    __tablename__ = "chatmember"
    member_id = Column(ForeignKey("users.id"))
    member = relationship("User", foreign_keys=member_id)
    chat_id = Column(ForeignKey("chats.id"))
    chat = relationship("Chat", foreign_keys=chat_id)
    def to_dict(self):
        return {"id": self.id, "member_id": self.member_id, "chat_id": self.chat_id}

class Chat(BaseModel):
    __tablename__ = "chats"
    def to_dict(self):
        return {"id": self.id}

class Message(BaseModel):
    __tablename__ = "messages"
    content = Column(String(255))
    chat_id = Column(ForeignKey("chats.id"))
    chat = relationship("Chat", foreign_keys=chat_id)
    sender_id = Column(ForeignKey("users.id"))
    sender = relationship("User", foreign_keys=sender_id)
    def to_dict(self):
        return {"id": self.id, "createdAt": str(self.createdAt), 
        "content": self.content, "chat_id": self.chat_id, "sender_id": self.sender_id}

# class Favourite(BaseModel):
#     __tablename__ = "favourites"