"""
Инструменты для работы с моделью пользователей.

Обеспечивает CRUD операции, хеширование паролей и миграцию системы хеширования.
"""
from database.basic_tools import AsyncBaseIdSQLAlchemyCRUD
from database.models.users import UserModel
from asyncio import Lock
import random
import string
import hashlib
import bcrypt
from utils.exception_handler.handler import handle_async


class UserTool(AsyncBaseIdSQLAlchemyCRUD):
    """
    Класс для управления пользователями с расширенным функционалом.
    
    Наследует базовые CRUD операции и добавляет специализированные
    методы для аутентификации и работы с паролями.
    
    Attributes:
        model: Модель UserModel
        field_id: Поле "id" как первичный ключ
        lock: Блокировка для потокобезопасной работы
    
    Note:
        Поддерживает миграцию паролей с SHA-256 на bcrypt для обратной совместимости.
    """
    model = UserModel
    field_id = "id"
    lock: Lock = Lock()

    @staticmethod
    async def get_by_email(email: str) -> UserModel:
        """
        Получает пользователя по адресу электронной почты.
        
        Args:
            email: Адрес электронной почты пользователя
            
        Returns:
            Объект пользователя или None если не найден
        """
        dbUsers: list[UserModel] = await UserTool.get_all_with_filters(filters=[UserModel.email == email])
        if len(dbUsers) == 0:
            return None
        return dbUsers[0]
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Хеширует пароль с использованием bcrypt и секретного ключа
        
        Args:
            password: Пароль для хеширования
            
        Returns:
            str: Хешированный пароль
        """
        
        # Генерируем соль и хешируем пароль
        salt = bcrypt.gensalt(rounds=12)  # Настройка сложности (12 раундов)
        hashed = bcrypt.hashpw(password.encode(), salt)
        
        # Возвращаем хеш в виде строки
        return hashed.decode('utf-8')

    @staticmethod
    def check_password(provided_password: str, stored_password: str) -> bool:
        """
        Проверяет пароль по хешу
        
        Args:
            provided_password: Предоставленный пароль
            stored_password: Хешированный пароль из базы данных
            
        Returns:
            bool: True, если пароль верный
        """
        
        # Проверяем пароль
        try:
            return bcrypt.checkpw(provided_password.encode(), stored_password.encode())
        except Exception as ex_:
            # Обработка ошибок (например, неверный формат хеша)
            return False

    @staticmethod
    async def migrate_password_if_needed(user_id: int, password: str) -> None:
        """
        Проверяет, нужно ли мигрировать пароль на новую систему хеширования
        
        Args:
            user_id: ID пользователя
            password: Пароль в открытом виде
        """
        # Получаем пользователя
        user = await UserTool(user_id).get()
        if not user:
            return
        
        # Проверяем, использует ли пароль старую систему хеширования (SHA-256)
        # SHA-256 хеш имеет длину 64 символа и состоит только из шестнадцатеричных символов
        if len(user.password) == 64 and all(c in '0123456789abcdef' for c in user.password.lower()):
            # Это старый хеш, нужно мигрировать на bcrypt
            new_hash = UserTool.hash_password(password)
            await UserTool(user_id).update(data={"password": new_hash})
            
    @classmethod
    async def verify_and_migrate_password(cls, user: UserModel, provided_password: str) -> bool:
        """
        Проверяет пароль и при необходимости мигрирует его на новую систему хеширования
        
        Args:
            user: Модель пользователя
            provided_password: Предоставленный пароль
            
        Returns:
            bool: True, если пароль верный
        """
        # Проверяем, использует ли пароль старую систему хеширования (SHA-256)
        if len(user.password) == 64 and all(c in '0123456789abcdef' for c in user.password.lower()):
            # Проверяем по старой системе
            old_hash = hashlib.sha256(provided_password.encode()).hexdigest()
            if old_hash == user.password:
                # Пароль верный, мигрируем на новую систему
                new_hash = cls.hash_password(provided_password)
                await UserTool(user.id).update(data={"password": new_hash})
                return True
            return False
        else:
            # Проверяем по новой системе
            return cls.check_password(provided_password, user.password)
