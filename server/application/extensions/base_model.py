from datetime import datetime
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()

def create_uuid():
    return str(uuid.uuid4())

class BaseModel(Base):
    __abstract__ = True
    id = Column(String(255), primary_key=True, default=create_uuid)
    createdAt = Column(DateTime, default=datetime.now)
    updatedAt = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # def to_dict(self):
    #     attributes = set([a for a in dir(self) if not a.startswith('__') and not a.startswith('_') and not callable(getattr(self, a))])
    #     subset = set(['metadata','registry'])
    #     if subset.issubset(attributes):
    #         attributes = attributes - subset
    #     dic = {}
    #     for att in attributes:
    #         if isinstance(getattr(self, att), datetime):
    #            temp = str(getattr(self, att))
    #            dic[att] = temp
    #         else:
    #             if not issubclass(type(getattr(self, att)), BaseModel):
    #                 dic[att] = getattr(self, att)
    #     return dic

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = str(getattr(self, column.name))

        return d