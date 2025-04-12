from typing import Any

from .chatterPreferredTtsSettingsRepositoryInterface import ChatterPreferredTtsSettingsRepositoryInterface
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface
from ...tts.jsonMapper.ttsJsonMapperInterface import TtsJsonMapperInterface
from ...tts.models.ttsProvider import TtsProvider


class ChatterPreferredTtsSettingsRepository(ChatterPreferredTtsSettingsRepositoryInterface):

    def __init__(
        self,
        settingsJsonReader: JsonReaderInterface,
        ttsJsonMapper: TtsJsonMapperInterface):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(ttsJsonMapper, TtsJsonMapperInterface):
            raise TypeError(f'ttsJsonMapper argument is malformed: \"{ttsJsonMapper}\"')

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader
        self.__ttsJsonMapper: TtsJsonMapperInterface = ttsJsonMapper

        self.__settingsCache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__settingsCache = None

    async def isEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'isEnabled', fallback = True)

    async def isTtsProviderEnabled(self, provider: TtsProvider) -> bool:
        jsonContents = await self.__readJson()
        enabledProviders: list[str] | None = jsonContents.get('enabledProviders')

        if enabledProviders is None:
            return False

        for enabledProvider in enabledProviders:
            if provider is self.__ttsJsonMapper.parseProvider(enabledProvider):
                return True

        return False

    async def __readJson(self) -> dict[str, Any]:
        if self.__settingsCache is not None:
            return self.__settingsCache

        jsonContents: dict[str, Any] | None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from Chatter Preferred TTS settings file: {self.__settingsJsonReader}')

        self.__settingsCache = jsonContents
        return jsonContents
