from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from application.extensions.base_model import BaseModel

class Post(BaseModel):
    __tablename__ = "posts"
    content = Column(String(255))
    author_id = Column(ForeignKey("users.id"))
    author = relationship("User", foreign_keys=author_id)
    

class Image(BaseModel):
    __tablename__ = "images"
    url= Column(String(255))
    post_id = Column(ForeignKey("posts.id"))
    post = relationship("Post", foreign_keys=post_id)