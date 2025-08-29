"""
Модель сессий пользователей для отслеживания JWT токенов.
"""
from database.base import Base
from sqlalchemy import Column, BigInteger, String, DateTime, Double, Boolean, ForeignKey
import datetime
from database.models.users import UserModel


class SessionModel(Base):
    """
    Модель для хранения активных сессий пользователей.
    
    Обеспечивает отслеживание активных JWT токенов и позволяет
    их досрочное аннулирование при необходимости.
    
    Attributes:
        id: Уникальный идентификатор сессии
        user_id: ID пользователя (внешний ключ на users.id)
        access_token: JWT токен (уникальный)
        creating_date: Дата создания сессии
    
    Note:
        Каждый активный JWT токен должен соответствовать записи в сессиях
        для прохождения проверки в AuthMiddleware.
    """
    __tablename__ = "sessions"
    
    # Первичный ключ
    id = Column(BigInteger, unique=True, primary_key=True)

    # Ссылка на пользователя и токен
    user_id = Column(BigInteger, ForeignKey(UserModel.id), nullable=False, index=True)
    access_token = Column(String, nullable=False, unique=True, index=True)

    # Метаданные
    creating_date = Column(DateTime, default=datetime.datetime.now, nullable=False)
    
    def __str__(self):
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"

    def __repr__(self):
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"