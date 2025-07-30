import re
import uuid
from typing import Final, Pattern

from .timeoutIdGeneratorInterface import TimeoutIdGeneratorInterface


class TimeoutIdGenerator(TimeoutIdGeneratorInterface):

    def __init__(self):
        self.__idRegEx: Final[Pattern] = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def generateActionId(self) -> str:
        return await self.__generateId()

    async def generateEventId(self) -> str:
        return await self.__generateId()

    async def __generateId(self) -> str:
        timeoutId = str(uuid.uuid4())
        return self.__idRegEx.sub('', timeoutId)
