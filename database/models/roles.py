from database.base import Base
from sqlalchemy import Column, BigInteger, String, DateTime, Double, Boolean, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy.orm import mapped_column
from database.models.rules import RuleModel


class RoleModel(Base):
    __tablename__ = "roles"
    name = Column(String, unique=True, primary_key=True)
    
    rules = mapped_column(ForeignKey(RuleModel.name))
    comment = Column(String, nullable=False)
    
    creating_date = Column(DateTime, default=datetime.datetime.now)
    
    def __str__(self):
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"

    def __repr__(self):
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"