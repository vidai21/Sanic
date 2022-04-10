from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from application.extensions.base_model import BaseModel

class Favourite(BaseModel):
    __tablename__ = "favourites"
    post_id = Column(ForeignKey("posts.id"))
    post = relationship("Post", foreign_keys=post_id)
    user_id = Column(ForeignKey("users.id"))
    user = relationship("User", foreign_keys=user_id)