from typing import Any, Final

from .websocketConnectionServerSettingsInterface import WebsocketConnectionServerSettingsInterface
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class WebsocketConnectionServerSettings(WebsocketConnectionServerSettingsInterface):

    def __init__(
        self,
        settingsJsonReader: JsonReaderInterface,
        defaultPort: int = 8765,
        defaultHost: str = '0.0.0.0',
    ):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not utils.isValidInt(defaultPort):
            raise TypeError(f'defaultPort argument is malformed: \"{defaultPort}\"')
        elif defaultPort < 1024 or defaultPort > 65535:
            raise ValueError(f'defaultPort argument is out of bounds: {defaultPort}')
        elif not utils.isValidStr(defaultHost):
            raise TypeError(f'defaultHost argument is malformed: \"{defaultHost}\"')

        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader
        self.__defaultPort: Final[int] = defaultPort
        self.__defaultHost: Final[str] = defaultHost

        self.__settingsCache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__settingsCache = None

    async def getEventTimeToLiveSeconds(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'eventTimeToLiveSeconds', 30)

    async def getHost(self) -> str:
        jsonContents = await self.__readJson()

        return utils.getStrFromDict(
            d = jsonContents,
            key = 'host',
            fallback = self.__defaultHost,
        )

    async def getPort(self) -> int:
        jsonContents = await self.__readJson()

        return utils.getIntFromDict(
            d = jsonContents,
            key = 'port',
            fallback = self.__defaultPort,
        )

    async def __readJson(self) -> dict[str, Any]:
        if self.__settingsCache is not None:
            return self.__settingsCache

        jsonContents: dict[str, Any] | None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from Websocket Connection Server settings file: {self.__settingsJsonReader}')

        self.__settingsCache = jsonContents
        return jsonContents
