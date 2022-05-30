import asyncio
from functools import wraps


# 定时任务装饰器
def timer(second):
    def timer_function(func):
        @wraps(func)
        async def wrapper(*arg, **kwargs):
            while True:
                await func(*arg, **kwargs)
                await asyncio.sleep(second)
            return

        return wrapper

    return timer_function
