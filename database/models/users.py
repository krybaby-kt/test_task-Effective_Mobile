"""
Модель пользователя системы.
"""
from database.base import Base
from sqlalchemy import Column, BigInteger, String, DateTime, Double, Boolean, ForeignKey
import datetime
from database.models.roles import RoleModel


class UserModel(Base):
    """
    Модель пользователя с аутентификацией и ролями.
    
    Обеспечивает хранение учетных данных пользователей, ссылку на роль
    и статус активности аккаунта.
    
    Attributes:
        id: Уникальный числовой идентификатор пользователя
        email: Адрес электронной почты (уникальный, используется для входа)
        password: Хешированный пароль (поддерживает SHA-256 и bcrypt)
        role: Имя роли (внешний ключ на roles.name)
        is_active: Флаг активности аккаунта
        creating_date: Дата создания аккаунта
    
    Note:
        Пароли хранятся в хешированном виде с поддержкой миграции
        с старых SHA-256 хешей на более безопасные bcrypt.
    """
    __tablename__ = "users"
    
    # Первичный ключ и основные данные
    id = Column(BigInteger, unique=True, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    
    # Отношения и статус
    role = Column(String, ForeignKey(RoleModel.name), nullable=False, default="user")
    is_active = Column(Boolean, default=True, nullable=False)

    # Метаданные
    creating_date = Column(DateTime, default=datetime.datetime.now, nullable=False)
    
    def __str__(self):
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"

    def __repr__(self):
        attributes = ", ".join(f"{column.name}={getattr(self, column.name)}" for column in self.__table__.columns)
        return f"{self.__class__.__name__}: {attributes}"