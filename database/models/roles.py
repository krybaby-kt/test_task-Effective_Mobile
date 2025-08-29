"""
Модель ролей пользователей в системе.
"""
from database.base import Base
from sqlalchemy import Column, BigInteger, String, DateTime, Double, Boolean, ForeignKey
import datetime


class RoleModel(Base):
    """
    Модель роли пользователя с описанием.
    
    Определяет роли, которые могут быть назначены пользователям в системе.
    Каждая роль может содержать множество прав через связь с RoleRuleModel.
    
    Attributes:
        name: Уникальное имя роли (первичный ключ)
        comment: Описание роли для администраторов
        creating_date: Дата создания роли
    
    Example:
        Примеры ролей: "admin", "user", "moderator", "support"
    """
    __tablename__ = "roles"
    
    # Первичный ключ и основные данные
    name = Column(String, unique=True, primary_key=True)
    comment = Column(String, nullable=False)
    
    # Метаданные
    creating_date = Column(DateTime, default=datetime.datetime.now, nullable=False)
    
    def __str__(self):
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"

    def __repr__(self):
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"