from functools import wraps
import inspect
from typing import Any, Callable
from utils.exception_handler.handler import (
    handle_async,
    handle_sync
)


def handle(function_category: str = None):
    """
    Декоратор для автоматической обработки исключений в функциях.
    
    Перехватывает исключения и логирует их с помощью системы обработки ошибок,
    после чего повторно поднимает исключение. Работает как с синхронными,
    так и с асинхронными функциями.
    
    Args:
        function_category: Категория функции для логирования. 
                         Если не указана, используется имя класса или модуля.
                         
    Returns:
        Декорированная функция с обработкой исключений.
        
    Example:
        @handle("database")
        async def create_user(data):
            # код функции
            pass
    """
    def decorator(func: Callable) -> Callable:
        is_async = inspect.iscoroutinefunction(func)
        is_method = inspect.ismethod(func) or inspect.isfunction(func) and hasattr(func, '__self__')
        
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            try:
                return await func(*args, **kwargs)
            except Exception as ex_:
                category = function_category or (func.__self__.__class__.__name__ if is_method else func.__module__)
                await handle_async(
                    function_category=category,
                    function=func.__name__,
                    exception=ex_   
                )
                raise
                
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as ex_:
                category = function_category or (func.__self__.__class__.__name__ if is_method else func.__module__)
                handle_sync(
                    function_category=category,
                    function=func.__name__,
                    exception=ex_
                )
                raise
                
        return async_wrapper if is_async else sync_wrapper
    return decorator 
