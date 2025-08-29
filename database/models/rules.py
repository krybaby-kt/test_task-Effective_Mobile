from database.base import Base
from sqlalchemy import Column, BigInteger, String, DateTime, Double, Boolean
import datetime


class RuleModel(Base):
    __tablename__ = "rules"
    name = Column(String, unique=True, primary_key=True)
    
    comment = Column(String, nullable=False)
    
    creating_date = Column(DateTime, default=datetime.datetime.now)
    
    def __str__(self):
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"

    def __repr__(self):
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"