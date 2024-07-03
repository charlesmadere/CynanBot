from typing import Any

from .jsonReaderInterface import JsonReaderInterface
from ..misc import utils as utils
from ..misc.clearable import Clearable


class PsqlCredentialsProvider(Clearable):

    def __init__(self, credentialsJsonReader: JsonReaderInterface):
        if not isinstance(credentialsJsonReader, JsonReaderInterface):
            raise TypeError(f'credentialsJsonReader argument is malformed: \"{credentialsJsonReader}\"')

        self.__credentialsJsonReader: JsonReaderInterface = credentialsJsonReader

        self.__jsonCache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__jsonCache = None

    async def getPassword(self) -> str | None:
        jsonContents = await self.__readJsonAsync()
        return utils.getStrFromDict(jsonContents, 'password', fallback = '')

    async def __readJsonAsync(self) -> dict[str, Any] | None:
        if self.__jsonCache is not None:
            return self.__jsonCache

        jsonCache = await self.__credentialsJsonReader.readJsonAsync()
        self.__jsonCache = jsonCache

        return jsonCache

    async def requireDatabaseName(self) -> str:
        jsonContents = await self.__readJsonAsync()
        return utils.getStrFromDict(jsonContents, 'databaseName')

    async def requireMaxConnections(self) -> int:
        jsonContents = await self.__readJsonAsync()

        maxConnections = utils.getIntFromDict(
            d = jsonContents,
            key = 'maxConnections',
            fallback = 100
        )

        if maxConnections < 1 or maxConnections > utils.getIntMaxSafeSize():
            raise ValueError(f'\"maxConnections\" value is malformed: \"{maxConnections}\"')

        return maxConnections

    async def requireUser(self) -> str:
        jsonContents = await self.__readJsonAsync()
        return utils.getStrFromDict(jsonContents, 'user')
