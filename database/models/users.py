from database.base import Base
from sqlalchemy import Column, BigInteger, String, DateTime, Double, Boolean, ForeignKey
import datetime
from database.models.roles import RoleModel


class UserModel(Base):
    __tablename__ = "users"
    id = Column(BigInteger, unique=True, primary_key=True)
    
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    
    status = Column(String, ForeignKey(RoleModel.name))
    is_active = Column(Boolean, default=True)

    creating_date = Column(DateTime, default=datetime.datetime.now)
    
    def __str__(self):
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"

    def __repr__(self):
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"