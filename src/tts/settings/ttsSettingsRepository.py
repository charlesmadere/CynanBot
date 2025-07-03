from typing import Any, Final

from .ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ..jsonMapper.ttsJsonMapperInterface import TtsJsonMapperInterface
from ..models.shotgun.shotgunProviderUseParameters import ShotgunProviderUseParameters
from ..models.shotgun.useAllShotgunParameters import UseAllShotgunParameters
from ..models.ttsProvider import TtsProvider
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class TtsSettingsRepository(TtsSettingsRepositoryInterface):

    def __init__(
        self,
        settingsJsonReader: JsonReaderInterface,
        ttsJsonMapper: TtsJsonMapperInterface,
        defaultRandoEnabledTtsProviders: frozenset[TtsProvider] = frozenset({
            TtsProvider.DEC_TALK,
            TtsProvider.HALF_LIFE,
            TtsProvider.MICROSOFT,
            TtsProvider.MICROSOFT_SAM,
            TtsProvider.STREAM_ELEMENTS,
            TtsProvider.TTS_MONSTER,
        }),
        defaultShotgunEnabledTtsProviders: frozenset[TtsProvider] = frozenset({
            TtsProvider.DEC_TALK,
            TtsProvider.HALF_LIFE,
            TtsProvider.MICROSOFT,
            TtsProvider.MICROSOFT_SAM,
            TtsProvider.STREAM_ELEMENTS,
            TtsProvider.TTS_MONSTER,
        }),
        defaultShotgunProviderUseParameters: ShotgunProviderUseParameters = UseAllShotgunParameters(),
    ):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(ttsJsonMapper, TtsJsonMapperInterface):
            raise TypeError(f'ttsJsonMapper argument is malformed: \"{ttsJsonMapper}\"')
        elif not isinstance(defaultRandoEnabledTtsProviders, frozenset):
            raise TypeError(f'defaultRandoEnabledTtsProviders argument is malformed: \"{defaultRandoEnabledTtsProviders}\"')
        elif not isinstance(defaultShotgunEnabledTtsProviders, frozenset):
            raise TypeError(f'defaultShotgunEnabledTtsProviders argument is malformed: \"{defaultShotgunEnabledTtsProviders}\"')
        elif not isinstance(defaultShotgunProviderUseParameters, ShotgunProviderUseParameters):
            raise TypeError(f'defaultShotgunProviderUseParameters argument is malformed: \"{defaultShotgunProviderUseParameters}\"')

        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader
        self.__ttsJsonMapper: Final[TtsJsonMapperInterface] = ttsJsonMapper
        self.__defaultRandoEnabledTtsProviders: Final[frozenset[TtsProvider]] = defaultRandoEnabledTtsProviders
        self.__defaultShotgunEnabledTtsProviders: Final[frozenset[TtsProvider]] = defaultShotgunEnabledTtsProviders
        self.__defaultShotgunProviderUseParameters: Final[ShotgunProviderUseParameters] = defaultShotgunProviderUseParameters

        self.__settingsCache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__settingsCache = None

    async def getMaximumMessageSize(self) -> int:
        jsonContents = await self.__readJson()

        maxMessageSize = utils.getIntFromDict(
            d = jsonContents,
            key = 'maxMessageSize',
            fallback = 500
        )

        if maxMessageSize < 1 or maxMessageSize > utils.getIntMaxSafeSize():
            raise ValueError(f'maxMessageSize is out of bounds: \"{maxMessageSize}\"')

        return maxMessageSize

    async def getRandoEnabledProviders(self) -> frozenset[TtsProvider]:
        jsonContents = await self.__readJson()
        enabledProvidersStrings: list[str] | None = jsonContents.get('randoEnabledProviders', None)

        if enabledProvidersStrings is None:
            return self.__defaultRandoEnabledTtsProviders

        enabledProviders: set[TtsProvider] = set()

        for enabledProviderString in enabledProvidersStrings:
            enabledProviders.add(await self.__ttsJsonMapper.asyncRequireProvider(enabledProviderString))

        return frozenset(enabledProviders)

    async def getShotgunEnabledProviders(self) -> frozenset[TtsProvider]:
        jsonContents = await self.__readJson()
        enabledProvidersStrings: list[str] | None = jsonContents.get('shotgunEnabledProviders', None)

        if enabledProvidersStrings is None:
            return self.__defaultShotgunEnabledTtsProviders

        enabledProviders: set[TtsProvider] = set()

        for enabledProviderString in enabledProvidersStrings:
            enabledProviders.add(await self.__ttsJsonMapper.asyncRequireProvider(enabledProviderString))

        return frozenset(enabledProviders)

    async def getShotgunProviderUseParameters(self) -> ShotgunProviderUseParameters:
        jsonContents = await self.__readJson()
        shotgunParametersJson: dict[str, Any] | Any | None = jsonContents.get('shotgunParameters', None)
        shotgunParameters: ShotgunProviderUseParameters | None = None

        if isinstance(shotgunParametersJson, dict):
            shotgunParameters = await self.__ttsJsonMapper.asyncParseShotgunProviderUseParameters(
                jsonContents = shotgunParametersJson
            )

        if shotgunParameters is None:
            return self.__defaultShotgunProviderUseParameters
        else:
            return shotgunParameters

    async def getTtsTimeoutSeconds(self) -> float:
        jsonContents = await self.__readJson()

        timeoutSeconds = utils.getFloatFromDict(
            d = jsonContents,
            key = 'timeoutSeconds',
            fallback = 45
        )

        if timeoutSeconds < 3 or timeoutSeconds > utils.getIntMaxSafeSize():
            raise ValueError(f'timeoutSeconds is out of bounds: \"{timeoutSeconds}\"')

        return timeoutSeconds

    async def isEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'isEnabled', fallback = False)

    async def __readJson(self) -> dict[str, Any]:
        if self.__settingsCache is not None:
            return self.__settingsCache

        jsonContents: dict[str, Any] | None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from TTS settings file: {self.__settingsJsonReader}')

        self.__settingsCache = jsonContents
        return jsonContents
