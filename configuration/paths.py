"""
Модуль конфигурации путей к файлам и директориям.

Определяет основные пути для хранения ассетов и логов исключений.
Создает необходимые директории при импорте модуля.
"""
from pathlib import Path

# Основная директория для хранения ассетов приложения
PATH_TO_ASSETS = Path("assets")
PATH_TO_ASSETS.mkdir(parents=True, exist_ok=True)

# Директория для хранения логов исключений
PATH_TO_EXCEPTIONS = Path(PATH_TO_ASSETS, "exceptions")
PATH_TO_EXCEPTIONS.mkdir(parents=True, exist_ok=True)
