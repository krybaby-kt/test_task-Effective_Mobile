from database.base import Base
from sqlalchemy import Column, BigInteger, String, DateTime, Double, Boolean, ForeignKey
import datetime
from database.models.users import UserModel


class SessionModel(Base):
    __tablename__ = "sessions"
    id = Column(BigInteger, unique=True, primary_key=True)

    user_id = Column(BigInteger, ForeignKey(UserModel.id))
    access_token = Column(String, nullable=False, unique=True)

    creating_date = Column(DateTime, default=datetime.datetime.now)
    
    def __str__(self):
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"

    def __repr__(self):
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"