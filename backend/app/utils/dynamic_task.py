# -*- coding: UTF-8 -*-
"""
动态添加Task
auther: colin
date: 2018-12-29
"""
import asyncio
import uvloop
from threading import Thread

_tasks_loop = None


def init():
    global _tasks_loop

    def start_loop(loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    _tasks_loop = asyncio.new_event_loop()
    tasks_thread = Thread(target=start_loop, args=(_tasks_loop, ))
    tasks_thread.start()


def run_async(fut):
    asyncio.run_coroutine_threadsafe(fut, _tasks_loop)
