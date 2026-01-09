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
        defaultHighTierTtsProviders: frozenset[TtsProvider] = frozenset(),
    ):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(ttsJsonMapper, TtsJsonMapperInterface):
            raise TypeError(f'ttsJsonMapper argument is malformed: \"{ttsJsonMapper}\"')
        elif not isinstance(defaultEnabledTtsProviders, frozenset):
            raise TypeError(f'defaultEnabledTtsProviders argument is malformed: \"{defaultEnabledTtsProviders}\"')
        elif not isinstance(defaultHighTierTtsProviders, frozenset):
            raise TypeError(f'defaultHighTierTtsProviders argument is malformed: \"{defaultHighTierTtsProviders}\"')

        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader
        self.__ttsJsonMapper: Final[TtsJsonMapperInterface] = ttsJsonMapper
        self.__defaultEnabledTtsProviders: Final[frozenset[TtsProvider]] = defaultEnabledTtsProviders
        self.__defaultHighTierTtsProviders: Final[frozenset[TtsProvider]] = defaultHighTierTtsProviders

        self.__cache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__cache = None

    async def getEnabledTtsProviders(self) -> frozenset[TtsProvider]:
        jsonContents = await self.__readJson()
        providersStrings: list[str] | None = jsonContents.get('enabledProviders', None)

        return await self.__parseTtsProviders(
            providersStrings = providersStrings,
            fallbackProviders = self.__defaultEnabledTtsProviders,
        )

    async def getHighTierTtsProviders(self) -> frozenset[TtsProvider]:
        jsonContents = await self.__readJson()
        providersStrings: list[str] | None = jsonContents.get('highTierProviders', None)

        return await self.__parseTtsProviders(
            providersStrings = providersStrings,
            fallbackProviders = self.__defaultHighTierTtsProviders,
        )

    async def isEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'isEnabled', fallback = True)

    async def __parseTtsProviders(
        self,
        providersStrings: list[str] | None,
        fallbackProviders: frozenset[TtsProvider],
    ) -> frozenset[TtsProvider]:
        if providersStrings is None:
            return fallbackProviders

        providers: set[TtsProvider] = set()

        for providerString in providersStrings:
            providers.add(await self.__ttsJsonMapper.asyncRequireProvider(providerString))

        return frozenset(providers)

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
