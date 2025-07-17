from asyncio import AbstractEventLoop, Task
from typing import Coroutine, Final

from .backgroundTaskHelperInterface import BackgroundTaskHelperInterface


class BackgroundTaskHelper(BackgroundTaskHelperInterface):

    def __init__(self, eventLoop: AbstractEventLoop):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')

        self.__eventLoop: Final[AbstractEventLoop] = eventLoop
        self.__backgroundTasks: Final[set[Task]] = set()

    def createTask(self, coro: Coroutine):
        if not isinstance(coro, Coroutine):
            raise TypeError(f'coro argument is malformed: \"{coro}\"')

        task = self.__eventLoop.create_task(coro)
        self.__backgroundTasks.add(task)
        task.add_done_callback(self.__backgroundTasks.discard)

    @property
    def eventLoop(self) -> AbstractEventLoop:
        return self.__eventLoop
