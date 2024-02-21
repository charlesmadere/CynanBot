from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.misc.clearable import Clearable
from CynanBot.storage.jsonReaderInterface import JsonReaderInterface


class PsqlCredentialsProvider(Clearable):

    def __init__(self, credentialsJsonReader: JsonReaderInterface):
        assert isinstance(credentialsJsonReader, JsonReaderInterface), f"malformed {credentialsJsonReader=}"

        self.__credentialsJsonReader: JsonReaderInterface = credentialsJsonReader

        self.__jsonCache: Optional[Dict[str, Any]] = None

    async def clearCaches(self):
        self.__jsonCache = None

    async def getPassword(self) -> Optional[str]:
        jsonContents = await self.__readJsonAsync()
        return utils.getStrFromDict(jsonContents, 'password', fallback = '')

    async def __readJsonAsync(self) -> Dict[str, Any]:
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
