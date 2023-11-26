from asyncio import AbstractEventLoop
from typing import Any, Coroutine, Set


class BackgroundTaskHelper():

    def __init__(self, eventLoop: AbstractEventLoop):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise ValueError(f'eventLoop argument is malformed: \"{eventLoop}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__backgroundTasks: Set[Any] = set()

    def createTask(self, coro: Coroutine):
        if coro is None:
            raise ValueError(f'coro argument is malformed: \"{coro}\"')

        task = self.__eventLoop.create_task(coro)
        self.__backgroundTasks.add(task)
        task.add_done_callback(self.__backgroundTasks.discard)

    def getEventLoop(self) -> AbstractEventLoop:
        return self.__eventLoop
