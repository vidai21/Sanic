from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from application.extensions.base_model import BaseModel

class Role(BaseModel):
    __tablename__ = "roles"
    role = Column(String(25))


class UserRole(BaseModel):
    __tablename__ = "userRoles"
    role_id = Column(ForeignKey("roles.id"))
    role = relationship("Role", foreign_keys=role_id)
    user_id = Column(ForeignKey("users.id"))
    user = relationship("User", foreign_keys=user_id)