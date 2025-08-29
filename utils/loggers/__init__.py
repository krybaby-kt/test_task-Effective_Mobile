"""
Модуль системы логирования.

Предоставляет цветные логгеры для консоли и запись логов в файлы.
"""
from typing import Any
import logging
from pathlib import Path


# ANSI коды цветов для форматирования логов в консоли
COLORS = {
    'DEBUG': '\033[94m',    # Синий
    'INFO': '\033[92m',     # Зеленый
    'WARNING': '\033[93m',  # Желтый
    'ERROR': '\033[91m',    # Красный
    'CRITICAL': '\033[91m', # Красный
    'RESET': '\033[0m',     # Сброс цвета
}


class ColoredFormatter(logging.Formatter):
    """
    Форматтер для обработки логов с поддержкой цветов.
    
    Добавляет цветовое форматирование к логам в зависимости от уровня.
    """
    
    def format(self, record):
        message = super().format(record)
        return f"{COLORS.get(record.levelname, '')}{message}{COLORS['RESET']}"


class Handler(logging.Handler):
    """
    Кастомный обработчик логов для записи в файлы.
    
    Создает текстовые файлы логов на основе атрибутов path и log_filename.
    """
    
    def emit(self, record):
        path = getattr(record, "path", None)
        log_filename = getattr(record, "log_filename", None)
        if not path or not log_filename:
            return

        with open(Path(path, f"{log_filename}.txt"), "a", encoding="utf-8") as log_file:
            log_file.write(str(self.format(record=record)) + "\n")


def _create_logger(name: str, level: int, fmt: str = None, datefmt: str = None, handler: Any = None):
    """
    Создает сконфигурированный логгер с цветным консольным выводом и опциональной записью в файл.
    
    Args:
        name: Имя логгера
        level: Уровень логирования для консоли
        fmt: Формат сообщений лога
        datefmt: Формат даты/времени
        handler: Опциональный обработчик для записи в файл
        
    Returns:
        Настроенный объект логгера
    """
    logger = logging.getLogger(name=name)
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    console_formatter = ColoredFormatter(
        fmt=fmt,
        datefmt=datefmt,
    )
    
    file_formatter = logging.Formatter(
        fmt=fmt,
        datefmt=datefmt,
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level=level)
    console_handler.setFormatter(fmt=console_formatter)
    logger.addHandler(hdlr=console_handler)

    if handler:
        file_handler = handler()
        file_handler.setLevel(level=logging.DEBUG)
        file_handler.setFormatter(fmt=file_formatter)
        logger.addHandler(hdlr=file_handler)

    return logger


# Основной логгер приложения с поддержкой цветов и записи в файлы
logger = _create_logger(
    name="logger",
    level=logging.DEBUG,
    fmt="%(asctime)s | %(levelname)s:%(name)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    handler=Handler
)