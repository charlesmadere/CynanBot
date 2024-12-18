from typing import Any

from .decTalkSettingsRepositoryInterface import DecTalkSettingsRepositoryInterface
from ..decTalkVoiceMapperInterface import DecTalkVoiceMapperInterface
from ..models.decTalkVoice import DecTalkVoice
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class DecTalkSettingsRepository(DecTalkSettingsRepositoryInterface):

    def __init__(self,
        decTalkVoiceMapper: DecTalkVoiceMapperInterface,
        settingsJsonReader: JsonReaderInterface
    ):
        if not isinstance(decTalkVoiceMapper, DecTalkVoiceMapperInterface):
            raise TypeError(f'decTalkVoiceMapper argument is malformed: \"{decTalkVoiceMapper}\"')
        elif not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')

        self.__decTalkVoiceMapper: DecTalkVoiceMapperInterface = decTalkVoiceMapper
        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader

        self.__cache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__cache = None

    async def getDecTalkExecutablePath(self) -> str | None:
        jsonContents = await self.__readJson()
        decTalkPath = utils.getStrFromDict(jsonContents, 'decTalkPath', fallback = "../dectalk/say.exe")

        return utils.cleanPath(decTalkPath)

    async def getDefaultVoice(self) -> DecTalkVoice:
        jsonContents = await self.__readJson()
        decTalkVoiceStr = utils.getStrFromDict(jsonContents, 'defaultVoice', fallback = DecTalkVoice.PAUL.name)

        return await self.__decTalkVoiceMapper.fromString(decTalkVoiceStr)

    async def getMediaPlayerVolume(self) -> int | None:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'media_player_volume', fallback = 46)

    async def requireDecTalkExecutablePath(self) -> str:
        decTalkPath = await self.getDecTalkExecutablePath()

        if not utils.isValidStr(decTalkPath):
            raise ValueError(f'\"decTalkPath\" value is malformed: \"{decTalkPath}\"')

        return decTalkPath

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None = None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from DecTalk settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents