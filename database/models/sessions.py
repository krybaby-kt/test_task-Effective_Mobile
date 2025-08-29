from database.base import Base
from sqlalchemy import Column, BigInteger, String, DateTime, Double, Boolean, ForeignKey
import datetime
from database.models.users import UserModel


class SessionModel(Base):
    __tablename__ = "sessions"
    user_id = Column(BigInteger, ForeignKey(UserModel.id), unique=True, primary_key=True)

    session_id = Column(String, nullable=False)
    access_token = Column(String, nullable=False)
    expire_date = Column(DateTime, nullable=False)

    creating_date = Column(DateTime, default=datetime.datetime.now)
    
    def __str__(self):
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"

    def __repr__(self):
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"