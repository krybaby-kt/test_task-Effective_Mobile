from abc import ABC, abstractmethod
from typing import Any, Optional, List, Dict, TypeVar, Type
from sqlalchemy import BinaryExpression, select, update, delete, inspect, and_, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from database.base import AsyncSessionLocal
from utils.exception_handler.handler import handle_async
import random
import string

# Создаем типовую переменную для модели
T = TypeVar('T')


class AsyncAbstractRepository(ABC):
    """Абстрактный класс для работы с репозиториями."""

    @classmethod
    @abstractmethod
    async def raw_create(cls, session: AsyncSession, data: Dict[str, Any]):
        """
        Создает новую запись в базе данных.
        
        Args:
            session: Сессия базы данных
            data: Данные для создания записи
        """
        raise NotImplementedError

    @abstractmethod
    async def raw_get(self, session: AsyncSession, filter_: BinaryExpression):
        """
        Получает запись из базы данных по фильтру.
        
        Args:
            session: Сессия базы данных
            filter_: Условие фильтрации
        """
        raise NotImplementedError

    @abstractmethod
    async def raw_update(self, session: AsyncSession, data: Dict[str, Any], filter_: BinaryExpression):
        """
        Обновляет запись в базе данных.
        
        Args:
            session: Сессия базы данных
            data: Данные для обновления
            filter_: Условие фильтрации
        """
        raise NotImplementedError

    @abstractmethod
    async def raw_delete(self, session: AsyncSession, filter_: BinaryExpression):
        """
        Удаляет запись из базы данных.
        
        Args:
            session: Сессия базы данных
            filter_: Условие фильтрации
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def raw_get_all_with_filters(cls, session: AsyncSession, filters: Optional[List[Any]] = None, sort_by: Optional[Any] = None, sort_order: str = "asc", limit: Optional[int] = None, offset: Optional[int] = None) -> List[Any]:
        """
        Получает записи из базы данных с динамической фильтрацией и сортировкой.
        
        Args:
            session: Сессия базы данных
            filters: Список прямых условий SQLAlchemy
            sort_by: Поле для сортировки
            sort_order: Порядок сортировки
            limit: Ограничение количества записей
            offset: Смещение записей
            
        Returns:
            List[Any]: Список записей, удовлетворяющих условиям
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def raw_update_with_filters(cls, session: AsyncSession, data: Dict[str, Any], filters: Optional[List[Any]] = None) -> Any:
        """
        Обновляет записи в базе данных с динамической фильтрацией.
        
        Args:
            session: Сессия базы данных
            data: Данные для обновления
            filters: Список прямых условий SQLAlchemy
            
        Returns:
            Any: Результат выполнения запроса
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def raw_delete_with_filters(cls, session: AsyncSession, filters: Optional[List[Any]] = None) -> Any:
        """
        Удаляет записи из базы данных с динамической фильтрацией.
        
        Args:
            session: Сессия базы данных
            filters: Список прямых условий SQLAlchemy
            
        Returns:
            Any: Результат выполнения запроса
        """
        raise NotImplementedError


class AsyncSQLAlchemyRepository(AsyncAbstractRepository):
    """Базовый класс для работы с SQLAlchemy репозиториями."""
    model = None

    @classmethod
    async def raw_create(cls, session: AsyncSession, data: Dict[str, Any]) -> model: # type: ignore
        """
        Создает новую запись в базе данных.
        
        Args:
            session: Сессия базы данных
            data: Данные для создания записи
            
        Returns:
            model: Созданная запись
        """
        u = cls.model(**data)
        session.add(u)
        await session.commit()
        await session.refresh(u)
        return u

    async def raw_get(self, session: AsyncSession, filter_: BinaryExpression) -> model: # type: ignore
        """
        Получает запись из базы данных по фильтру.
        
        Args:
            session: Сессия базы данных
            filter_: Условие фильтрации
            
        Returns:
            model: Найденная запись
        """
        query = select(self.model).filter(filter_)
        return await session.scalar(query)

    @classmethod
    async def raw_get_all(cls, session: AsyncSession) -> List[model]: # type: ignore
        """
        Получает все записи из базы данных.
        
        Args:
            session: Сессия базы данных
            
        Returns:
            List: Список всех записей
        """
        query = select(cls.model)
        return await session.scalars(query)

    @classmethod
    async def raw_get_all_with_filters(cls, session: AsyncSession, filters: Optional[List[Any]] = None, sort_by: Optional[Any] = None, sort_order: str = "asc", limit: Optional[int] = None, offset: Optional[int] = None) -> List[model]: # type: ignore
        """
        Получает записи из базы данных с динамической фильтрацией и сортировкой.
        
        Args:
            session: Сессия базы данных
            filters: Список прямых условий SQLAlchemy
            sort_by: Поле для сортировки
            sort_order: Порядок сортировки
            limit: Ограничение количества записей
            offset: Смещение записей
            
        Returns:
            List[model]: Список записей, удовлетворяющих условиям
        """
        # Получаем все колонки модели
        columns = inspect(cls.model).columns
        column_names = {column.name: column for column in columns}
        
        # Создаем базовый запрос
        query = select(cls.model)
        
        # Добавляем условия фильтрации, если они есть
        if filters:
            query = query.filter(and_(*filters))
        
        # Добавляем сортировку, если она указана
        if sort_by:
            # Если sort_by - это строка (имя поля)
            if isinstance(sort_by, str) and sort_by in column_names:
                sort_column = getattr(cls.model, sort_by)
            # Если sort_by - это атрибут модели
            elif hasattr(sort_by, 'key') and getattr(sort_by, 'key') in column_names:
                sort_column = sort_by
            else:
                # Если не удалось определить поле для сортировки, пропускаем сортировку
                sort_column = None
            
            if sort_column:
                if sort_order.lower() == "desc":
                    query = query.order_by(desc(sort_column))
                else:
                    query = query.order_by(asc(sort_column))
        
        # Добавляем ограничение и смещение, если они указаны
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
        
        # Выполняем запрос
        result = await session.scalars(query)
        return list(result)

    @classmethod
    async def raw_update_with_filters(cls, session: AsyncSession, data: Dict[str, Any], filters: Optional[List[Any]] = None) -> Any:
        """
        Обновляет записи в базе данных с динамической фильтрацией.
        
        Args:
            session: Сессия базы данных
            data: Данные для обновления
            filters: Список прямых условий SQLAlchemy
            
        Returns:
            Any: Результат выполнения запроса
        """
        # Создаем базовый запрос
        query = update(cls.model)
        
        # Добавляем условия фильтрации, если они есть
        if filters:
            query = query.filter(and_(*filters))
        
        # Добавляем данные для обновления
        query = query.values(data)
        
        # Выполняем запрос
        result = await session.execute(query)
        await session.commit()
        return result

    @classmethod
    async def raw_delete_with_filters(cls, session: AsyncSession, filters: Optional[List[Any]] = None) -> Any:
        """
        Удаляет записи из базы данных с динамической фильтрацией.
        
        Args:
            session: Сессия базы данных
            filters: Список прямых условий SQLAlchemy
            
        Returns:
            Any: Результат выполнения запроса
        """
        # Создаем базовый запрос
        query = delete(cls.model)
        
        # Добавляем условия фильтрации, если они есть
        if filters:
            query = query.filter(and_(*filters))
        
        # Выполняем запрос
        result = await session.execute(query)
        await session.commit()
        return result

    async def raw_update(self, session: AsyncSession, data: Dict[str, Any], filter_: BinaryExpression) -> Any:
        """
        Обновляет запись в базе данных.
        
        Args:
            session: Сессия базы данных
            data: Данные для обновления
            filter_: Условие фильтрации
            
        Returns:
            Result: Результат выполнения запроса
        """
        query = update(self.model).filter(filter_).values(data)
        r_ = await session.execute(query)
        await session.commit()
        return r_

    async def raw_delete(self, session: AsyncSession, filter_: BinaryExpression) -> Any:
        """
        Удаляет запись из базы данных.
        
        Args:
            session: Сессия базы данных
            filter_: Условие фильтрации
            
        Returns:
            Result: Результат выполнения запроса
        """
        query = delete(self.model).filter(filter_)
        r_ = await session.execute(query)
        await session.commit()
        return r_


class AsyncBaseIdSQLAlchemyCRUD(AsyncSQLAlchemyRepository):
    """Базовый класс для CRUD операций с моделями по ID."""
    model = None
    field_id = None
    count_attemps = 10

    def __init__(self, __id: Any):
        """
        Инициализирует CRUD объект.
        
        Args:
            __id: ID записи
        """
        self.custom_id = __id
    
    @classmethod
    async def generate_unique_field_id(cls, *args, length: int = 12, return_type: Type = str) -> Any:
        """
        Генерирует уникальный ID для записи.
        
        Args:
            *args: Списки символов для генерации ID. По умолчанию используются цифры, заглавные и строчные буквы
            length: Длина генерируемого ID
            return_type: Тип возвращаемого значения (str, int, float)
            
        Returns:
            Any: Уникальный ID указанного типа
        """
        # Если не переданы списки символов, используем стандартные
        char_sets = args if args else [string.digits, string.ascii_uppercase, string.ascii_lowercase]
        # Объединяем все наборы символов
        all_chars = ''.join(char_sets)
        
        for attempt in range(cls.count_attemps):
            try:
                async with AsyncSessionLocal() as session:
                    while True:
                        # Генерируем строковый ID
                        str_id = "".join([random.choice(all_chars) for _ in range(length)])
                        
                        # Преобразуем ID в нужный тип
                        if return_type == int:
                            id_value = int(str_id)
                        elif return_type == float:
                            id_value = float(str_id)
                        else:
                            id_value = str_id
                        
                        # Проверяем уникальность ID
                        instance = cls(id_value)
                        if not await instance.raw_get(session=session, filter_=(getattr(cls.model, cls.field_id) == id_value)):
                            return id_value
            except Exception as ex_:
                await handle_async(function_category="database", function=f"{cls.model.__tablename__}  generate_id", exception=ex_)
                if attempt == cls.count_attemps - 1:  # Вызываем raise только на последней попытке
                    raise

    @classmethod
    async def create(cls, data: Dict[str, Any]) -> model: # type: ignore
        """
        Создает новую запись в базе данных с повторными попытками.
        
        Args:
            data: Данные для создания записи
            
        Returns:
            model: Созданная запись
        """
        for attempt in range(cls.count_attemps):
            try:
                async with AsyncSessionLocal() as session:
                    return await super().raw_create(session=session, data=data)
            except Exception as ex_:
                await handle_async(function_category="database", function=f"{cls.model.__tablename__}  create", exception=ex_)
                if attempt == cls.count_attemps - 1:  # Вызываем raise только на последней попытке
                    raise

    async def get(self) -> model: # type: ignore
        """
        Получает запись из базы данных по ID с повторными попытками.
        
        Returns:
            model: Найденная запись
        """
        for attempt in range(self.__class__.count_attemps):
            try:
                async with AsyncSessionLocal() as session:
                    return await super().raw_get(session=session, filter_=(getattr(self.model, self.field_id) == self.custom_id))
            except Exception as ex_:
                await handle_async(function_category="database", function=f"{self.model.__tablename__}  get", exception=ex_)
                if attempt == self.__class__.count_attemps - 1:  # Вызываем raise только на последней попытке
                    raise

    @classmethod
    async def get_all(cls) -> List[model]: # type: ignore
        """
        Получает все записи из базы данных с повторными попытками.
        
        Returns:
            List: Список всех записей
        """
        for attempt in range(cls.count_attemps):
            try:
                async with AsyncSessionLocal() as session:
                    return list(await super().raw_get_all(session=session))
            except Exception as ex_:
                await handle_async(function_category="database", function=f"{cls.model.__tablename__}  get_all", exception=ex_)
                if attempt == cls.count_attemps - 1:  # Вызываем raise только на последней попытке
                    raise

    @classmethod
    async def get_all_with_filters(cls, filters: Optional[List[Any]] = None, sort_by: Optional[Any] = None, sort_order: str = "asc", limit: Optional[int] = None, offset: Optional[int] = None) -> List[model]: # type: ignore
        """
        Получает записи из базы данных с динамической фильтрацией и сортировкой с повторными попытками.
        
        Args:
            filters: Список прямых условий SQLAlchemy (например, [Model.field > 5, Model.another_field == True])
            sort_by: Поле для сортировки. Может быть строкой с именем поля или прямой ссылкой на атрибут модели
            sort_order: Порядок сортировки ("asc" или "desc")
            limit: Ограничение количества записей
            offset: Смещение записей
            
        Returns:
            List[model]: Список записей, удовлетворяющих условиям
        """
        for attempt in range(cls.count_attemps):
            try:
                async with AsyncSessionLocal() as session:
                    return await super().raw_get_all_with_filters(session=session, filters=filters, sort_by=sort_by, sort_order=sort_order, limit=limit, offset=offset)
            except Exception as ex_:
                await handle_async(function_category="database", function=f"{cls.model.__tablename__}  get_all_with_filters", exception=ex_)
                if attempt == cls.count_attemps - 1:  # Вызываем raise только на последней попытке
                    raise

    @classmethod
    async def update_with_filters(cls, data: Dict[str, Any], filters: Optional[List[Any]] = None) -> Any:
        """
        Обновляет записи в базе данных с динамической фильтрацией с повторными попытками.
        
        Args:
            data: Данные для обновления
            filters: Список прямых условий SQLAlchemy (например, [Model.field > 5, Model.another_field == True])
            
        Returns:
            Any: Результат выполнения запроса
        """
        for attempt in range(cls.count_attemps):
            try:
                async with AsyncSessionLocal() as session:
                    return await super().raw_update_with_filters(session=session, data=data, filters=filters)
            except Exception as ex_:
                await handle_async(function_category="database", function=f"{cls.model.__tablename__}  update_with_filters", exception=ex_)
                if attempt == cls.count_attemps - 1:  # Вызываем raise только на последней попытке
                    raise

    @classmethod
    async def delete_with_filters(cls, filters: Optional[List[Any]] = None) -> Any:
        """
        Удаляет записи из базы данных с динамической фильтрацией с повторными попытками.
        
        Args:
            filters: Список прямых условий SQLAlchemy (например, [Model.field > 5, Model.another_field == True])
            
        Returns:
            Any: Результат выполнения запроса
        """
        for attempt in range(cls.count_attemps):
            try:
                async with AsyncSessionLocal() as session:
                    return await super().raw_delete_with_filters(session=session, filters=filters)
            except Exception as ex_:
                await handle_async(function_category="database", function=f"{cls.model.__tablename__}  delete_with_filters", exception=ex_)
                if attempt == cls.count_attemps - 1:  # Вызываем raise только на последней попытке
                    raise

    async def update(self, data: Dict[str, Any]) -> Any:
        """
        Обновляет запись в базе данных по ID с повторными попытками.
        
        Args:
            data: Данные для обновления
            
        Returns:
            Result: Результат выполнения запроса
        """
        for attempt in range(self.__class__.count_attemps):
            try:
                async with AsyncSessionLocal() as session:
                    return await super().raw_update(session=session, data=data, filter_=(getattr(self.model, self.field_id) == self.custom_id))
            except Exception as ex_:
                await handle_async(function_category="database", function=f"{self.model.__tablename__}  update", exception=ex_)
                if attempt == self.__class__.count_attemps - 1:  # Вызываем raise только на последней попытке
                    raise

    async def delete(self) -> Any:
        """
        Удаляет запись из базы данных по ID с повторными попытками.
        
        Returns:
            Result: Результат выполнения запроса
        """
        for attempt in range(self.__class__.count_attemps):
            try:
                async with AsyncSessionLocal() as session:
                    return await super().raw_delete(session=session, filter_=(getattr(self.model, self.field_id) == self.custom_id))
            except Exception as ex_:
                await handle_async(function_category="database", function=f"{self.model.__tablename__}  delete", exception=ex_)
                if attempt == self.__class__.count_attemps - 1:  # Вызываем raise только на последней попытке
                    raise