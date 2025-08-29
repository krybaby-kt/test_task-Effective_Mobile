"""
Модуль конфигурации базы данных.

Содержит настройки подключения к PostgreSQL базе данных,
создание асинхронного движка SQLAlchemy и базового класса для моделей.
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import URL

# URL подключения к PostgreSQL базе данных через asyncpg драйвер
url = URL.create(
    drivername="postgresql+asyncpg",
    username="postgres",
    password="admin",
    host="localhost",
    port=5432,
    database="test_task_effective_mobile",
)

# Асинхронный движок SQLAlchemy с настройками пула подключений
engine = create_async_engine(url, pool_size=25, max_overflow=50, pool_timeout=300)

# Фабрика для создания асинхронных сессий базы данных
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autocommit=False)

# Базовый класс для всех ORM моделей
Base = declarative_base()
