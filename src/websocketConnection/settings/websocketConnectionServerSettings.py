from typing import Any, Final

from .websocketConnectionServerSettingsInterface import WebsocketConnectionServerSettingsInterface
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class WebsocketConnectionServerSettings(WebsocketConnectionServerSettingsInterface):

    def __init__(self, settingsJsonReader: JsonReaderInterface):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')

        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader

        self.__settingsCache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__settingsCache = None

    async def getEventTimeToLiveSeconds(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'eventTimeToLiveSeconds', 30)

    async def getHost(self) -> str:
        jsonContents = await self.__readJson()
        return utils.getStrFromDict(jsonContents, 'host', '0.0.0.0')

    async def getPort(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'port', 8765)

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
