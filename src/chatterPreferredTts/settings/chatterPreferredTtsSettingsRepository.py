from typing import Any, Final

from .chatterPreferredTtsSettingsRepositoryInterface import ChatterPreferredTtsSettingsRepositoryInterface
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface
from ...tts.jsonMapper.ttsJsonMapperInterface import TtsJsonMapperInterface
from ...tts.models.ttsProvider import TtsProvider


class ChatterPreferredTtsSettingsRepository(ChatterPreferredTtsSettingsRepositoryInterface):

    def __init__(
        self,
        settingsJsonReader: JsonReaderInterface,
        ttsJsonMapper: TtsJsonMapperInterface,
        defaultEnabledTtsProviders: frozenset[TtsProvider] = frozenset({
            TtsProvider.DEC_TALK,
            TtsProvider.MICROSOFT_SAM,
        }),
    ):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(ttsJsonMapper, TtsJsonMapperInterface):
            raise TypeError(f'ttsJsonMapper argument is malformed: \"{ttsJsonMapper}\"')
        elif not isinstance(defaultEnabledTtsProviders, frozenset):
            raise TypeError(f'defaultEnabledTtsProviders argument is malformed: \"{defaultEnabledTtsProviders}\"')

        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader
        self.__ttsJsonMapper: Final[TtsJsonMapperInterface] = ttsJsonMapper
        self.__defaultEnabledTtsProviders: Final[frozenset[TtsProvider]] = defaultEnabledTtsProviders

        self.__cache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__cache = None

    async def getEnabledTtsProviders(self) -> frozenset[TtsProvider]:
        jsonContents = await self.__readJson()
        enabledProvidersStrings: list[str] | None = jsonContents.get('enabledProviders', None)

        if enabledProvidersStrings is None:
            return self.__defaultEnabledTtsProviders

        enabledProviders: set[TtsProvider] = set()

        for enabledProviderString in enabledProvidersStrings:
            enabledProviders.add(await self.__ttsJsonMapper.asyncRequireProvider(enabledProviderString))

        return frozenset(enabledProviders)

    async def isEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'isEnabled', fallback = True)

    async def isTtsProviderEnabled(self, provider: TtsProvider) -> bool:
        enabledProviders = await self.getEnabledTtsProviders()
        return provider in enabledProviders

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from Chatter Preferred TTS settings file: {self.__settingsJsonReader}')

        self.__settingsCache = jsonContents
        return jsonContents
