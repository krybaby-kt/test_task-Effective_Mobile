"""
Модель правил доступа в системе.
"""
from database.base import Base
from sqlalchemy import Column, BigInteger, String, DateTime, Double, Boolean
import datetime


class RuleModel(Base):
    """
    Модель правила доступа с описанием.
    
    Определяет конкретные права, которые могут быть назначены ролям.
    Каждое правило может принадлежать множеству ролей через связь с RoleRuleModel.
    
    Attributes:
        name: Уникальное имя правила (первичный ключ)
        comment: Описание правила для администраторов
        creating_date: Дата создания правила
    
    Example:
        Примеры правил: "admin_panel", "user_panel", "support_panel", "read_users"
    """
    __tablename__ = "rules"
    
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