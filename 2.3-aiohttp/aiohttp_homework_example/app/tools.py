import asyncio
from functools import wraps
from typing import Any, Awaitable, Callable


def singleton(func: Callable[..., Awaitable[Any]] | Callable) -> Callable[..., Awaitable[Any]] | Callable:

    result = None
    ready = False

    @wraps(func)
    async def new_async_func(*args, **kwargs):
        nonlocal result, ready

        if ready:
            return result

        result = await func(*args, **kwargs)
        ready = True

        return result

    @wraps(func)
    def new_func(*args, **kwargs):
        nonlocal result, ready

        if ready:
            return result

        result = func(*args, **kwargs)
        ready = True

        return result

    return new_async_func if asyncio.iscoroutinefunction(func) else new_func
