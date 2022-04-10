from sqlalchemy import Column, String
from application.extensions.base_model import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    username = Column(String(50))
    password = Column(String(255))
    email = Column(String(50))
    phone = Column(String(10))