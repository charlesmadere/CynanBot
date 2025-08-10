import re
import uuid
from typing import Final, Pattern

from .chatterInventoryIdGeneratorInterface import ChatterInventoryIdGeneratorInterface


class ChatterInventoryIdGenerator(ChatterInventoryIdGeneratorInterface):

    def __init__(self):
        self.__idRegEx: Final[Pattern] = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def generateActionId(self) -> str:
        return await self.__generateId()

    async def __generateId(self) -> str:
        randomUuid = str(uuid.uuid4())
        randomUuid = self.__idRegEx.sub('', randomUuid)
        return randomUuid.casefold()

    async def generateEventId(self) -> str:
        return await self.__generateId()

    async def generateRequestId(self) -> str:
        return await self.__generateId()
