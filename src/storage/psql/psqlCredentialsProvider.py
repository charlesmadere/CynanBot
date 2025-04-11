from typing import Any, Final

from .psqlCredentialsProviderInterface import PsqlCredentialsProviderInterface
from ..jsonReaderInterface import JsonReaderInterface
from ...misc import utils as utils


class PsqlCredentialsProvider(PsqlCredentialsProviderInterface):

    def __init__(self, credentialsJsonReader: JsonReaderInterface):
        if not isinstance(credentialsJsonReader, JsonReaderInterface):
            raise TypeError(f'credentialsJsonReader argument is malformed: \"{credentialsJsonReader}\"')

        self.__credentialsJsonReader: Final[JsonReaderInterface] = credentialsJsonReader

        self.__jsonCache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__jsonCache = None

    async def getHost(self) -> str | None:
        jsonContents = await self.__readJsonAsync()

        host: str | None = None
        if 'host' in jsonContents and utils.isValidStr(jsonContents.get('host')):
            host = utils.getStrFromDict(jsonContents, 'host')

        return host

    async def getPassword(self) -> str | None:
        jsonContents = await self.__readJsonAsync()

        password: str | None = None
        if 'password' in jsonContents and utils.isValidStr(jsonContents.get('password')):
            password = utils.getStrFromDict(jsonContents, 'password')

        return password

    async def getPort(self) -> int | None:
        jsonContents = await self.__readJsonAsync()

        port: int | None = None
        if 'port' in jsonContents and utils.isValidInt(jsonContents.get('port')):
            port = utils.getIntFromDict(jsonContents, 'port')

        return port

    async def __readJsonAsync(self) -> dict[str, Any]:
        if self.__jsonCache is not None:
            return self.__jsonCache

        jsonContents = await self.__credentialsJsonReader.readJsonAsync()

        if jsonContents is None:
            jsonContents = dict()

        self.__jsonCache = jsonContents
        return jsonContents

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
