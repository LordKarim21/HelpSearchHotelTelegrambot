from typing import Callable


def exception_handler(func: Callable) -> Callable:
    """
    Декоратор - оборачивающий функцию в try-except блок.

    :param func: Callable
    :return: Callable
    """
    def wrapped_func(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print('Что-то пошло не так! Давайте попробуем снова.', e)
    return wrapped_func


def exception_request_handler(func: Callable) -> Callable:
    """
    Декоратор - оборачивающий функцию request в try-except блок.

    :param func: Callable
    :return: Callable
    """
    def wrapped_func(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except (ConnectionError, TimeoutError):
            print('Что-то пошло не так! Давайте попробуем снова.')
    return wrapped_func
