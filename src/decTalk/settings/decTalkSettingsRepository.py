from typing import Any, Final

from .decTalkSettingsRepositoryInterface import DecTalkSettingsRepositoryInterface
from ..mapper.decTalkVoiceMapperInterface import DecTalkVoiceMapperInterface
from ..models.decTalkVoice import DecTalkVoice
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class DecTalkSettingsRepository(DecTalkSettingsRepositoryInterface):

    def __init__(
        self,
        decTalkVoiceMapper: DecTalkVoiceMapperInterface,
        settingsJsonReader: JsonReaderInterface,
        defaultDecTalkVoice: DecTalkVoice = DecTalkVoice.PAUL,
    ):
        if not isinstance(decTalkVoiceMapper, DecTalkVoiceMapperInterface):
            raise TypeError(f'decTalkVoiceMapper argument is malformed: \"{decTalkVoiceMapper}\"')
        elif not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(defaultDecTalkVoice, DecTalkVoice):
            raise TypeError(f'defaultDecTalkVoice argument is malformed: \"{defaultDecTalkVoice}\"')

        self.__decTalkVoiceMapper: Final[DecTalkVoiceMapperInterface] = decTalkVoiceMapper
        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader
        self.__defaultDecTalkVoice: Final[DecTalkVoice] = defaultDecTalkVoice

        self.__cache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__cache = None

    async def getDecTalkExecutablePath(self) -> str | None:
        jsonContents = await self.__readJson()
        return utils.getStrFromDict(jsonContents, 'decTalkPath', fallback = '../dectalk/say.exe')

    async def getDefaultVoice(self) -> DecTalkVoice:
        jsonContents = await self.__readJson()

        decTalkVoiceStr = utils.getStrFromDict(
            d = jsonContents,
            key = 'defaultVoice',
            fallback = await self.__decTalkVoiceMapper.serializeVoice(self.__defaultDecTalkVoice),
        )

        return await self.__decTalkVoiceMapper.requireVoice(decTalkVoiceStr)

    async def getMediaPlayerVolume(self) -> int | None:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'mediaPlayerVolume', fallback = 10)

    async def requireDecTalkExecutablePath(self) -> str:
        decTalkPath = await self.getDecTalkExecutablePath()

        if not utils.isValidStr(decTalkPath):
            raise ValueError(f'\"decTalkPath\" value is missing/malformed: \"{decTalkPath}\"')

        return decTalkPath

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from Dec Talk settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents

    async def useDonationPrefix(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'useDonationPrefix', fallback = True)
