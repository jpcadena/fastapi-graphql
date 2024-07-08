"""
This module provides decorators designed to provide additional
 functionality to the functions they are used with.
"""

import logging
from functools import wraps
from time import perf_counter
from typing import Any, Callable

logger: logging.Logger = logging.getLogger(__name__)


def with_logging(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    This decorator logs when a function starts and finishes its
     execution.
    :param func: The function to be decorated
    :type func: Callable
    :return: The decorated function that logs its call
    :rtype: Callable
    """

    @wraps(func)
    async def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Any:
        """
        A wrapper function that adds logging functionality
        :param args: Positional arguments to be passed to the decorated
         function
        :type args: tuple[Any, ...]
        :param kwargs: Keyword arguments to be passed to the decorated
         function
        :type kwargs: dict[str, Any]
        :return: The result of the decorated function's execution
        :rtype: Any
        """
        logger.info("Calling %s", func.__name__)
        value = await func(*args, **kwargs)
        logger.info("Finished %s", func.__name__)
        return value

    return wrapper


def benchmark(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    This decorator provides a benchmarking feature by logging the
     execution time of the decorated function
    :param func: The function to be executed
    :type func: Callable
    :return: The decorated function that logs its execution time
    :rtype: Callable
    """

    @wraps(func)
    async def wrapper(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> Any:
        """
        A wrapper function that adds benchmarking functionality
        :param args: Positional arguments to be passed to the decorated
         function
        :type args: tuple[Any, ...]
        :param kwargs: Keyword arguments to be passed to the decorated
         function
        :type kwargs: dict[str, Any]
        :return: The result of the decorated function's execution
        :rtype: Any
        """
        start_time: float = perf_counter()
        value = await func(*args, **kwargs)
        end_time: float = perf_counter()
        run_time: float = end_time - start_time
        logger.info("Execution of %s took %s seconds.", func.__name__, run_time)
        return value

    return wrapper
