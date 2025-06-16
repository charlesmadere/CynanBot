from typing import Any, Final

from .ttsMonsterSettingsRepositoryInterface import TtsMonsterSettingsRepositoryInterface
from ..mapper.ttsMonsterPrivateApiJsonMapperInterface import TtsMonsterPrivateApiJsonMapperInterface
from ..models.ttsMonsterDonationPrefixConfig import TtsMonsterDonationPrefixConfig
from ..models.ttsMonsterVoice import TtsMonsterVoice
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class TtsMonsterSettingsRepository(TtsMonsterSettingsRepositoryInterface):

    def __init__(
        self,
        settingsJsonReader: JsonReaderInterface,
        ttsMonsterPrivateApiJsonMapper: TtsMonsterPrivateApiJsonMapperInterface,
        defaultLoudVoices: frozenset[TtsMonsterVoice] = frozenset({
            TtsMonsterVoice.GLADOS,
            TtsMonsterVoice.JAZZ,
            TtsMonsterVoice.SHADOW,
            TtsMonsterVoice.SPONGEBOB,
        }),
        defaultDonationPrefixConfig: TtsMonsterDonationPrefixConfig = TtsMonsterDonationPrefixConfig.IF_MESSAGE_IS_BLANK,
        defaultVoice: TtsMonsterVoice = TtsMonsterVoice.BRIAN,
    ):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(ttsMonsterPrivateApiJsonMapper, TtsMonsterPrivateApiJsonMapperInterface):
            raise TypeError(f'ttsMonsterPrivateApiJsonMapper argument is malformed: \"{ttsMonsterPrivateApiJsonMapper}\"')
        elif not isinstance(defaultLoudVoices, frozenset):
            raise TypeError(f'defaultLoudVoices argument is malformed: \"{defaultLoudVoices}\"')
        elif not isinstance(defaultDonationPrefixConfig, TtsMonsterDonationPrefixConfig):
            raise TypeError(f'defaultDonationPrefixConfig argument is malformed: \"{defaultDonationPrefixConfig}\"')
        elif not isinstance(defaultVoice, TtsMonsterVoice):
            raise TypeError(f'defaultVoice argument is malformed: \"{defaultVoice}\"')

        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader
        self.__ttsMonsterPrivateApiJsonMapper: Final[TtsMonsterPrivateApiJsonMapperInterface] = ttsMonsterPrivateApiJsonMapper
        self.__defaultLoudVoices: Final[frozenset[TtsMonsterVoice]] = defaultLoudVoices
        self.__defaultDonationPrefixConfig: Final[TtsMonsterDonationPrefixConfig] = defaultDonationPrefixConfig
        self.__defaultVoice: Final[TtsMonsterVoice] = defaultVoice

        self.__cache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__cache = None

    async def getDefaultVoice(self) -> TtsMonsterVoice:
        jsonContents = await self.__readJson()

        defaultVoiceString = utils.getStrFromDict(
            d = jsonContents,
            key = 'default_voice',
            fallback = await self.__ttsMonsterPrivateApiJsonMapper.serializeVoice(self.__defaultVoice)
        )

        return await self.__ttsMonsterPrivateApiJsonMapper.requireVoice(defaultVoiceString)

    async def getDonationPrefixConfig(self) -> TtsMonsterDonationPrefixConfig:
        jsonContents = await self.__readJson()

        donationPrefixConfigString = utils.getStrFromDict(
            d = jsonContents,
            key = 'donation_prefix_config',
            fallback = await self.__ttsMonsterPrivateApiJsonMapper.serializeDonationPrefixConfig(self.__defaultDonationPrefixConfig)
        )

        return await self.__ttsMonsterPrivateApiJsonMapper.requireDonationPrefixConfig(donationPrefixConfigString)

    async def getFileExtension(self) -> str:
        jsonContents = await self.__readJson()
        return utils.getStrFromDict(jsonContents, 'file_extension', fallback = 'wav')

    async def getLoudVoiceMediaPlayerVolume(self) -> int | None:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'loud_voice_media_player_volume', fallback = 7)

    async def getLoudVoices(self) -> frozenset[TtsMonsterVoice]:
        jsonContents = await self.__readJson()
        loudVoicesStrings: list[str] | None = jsonContents.get('loud_voices', None)

        if loudVoicesStrings is None:
            return self.__defaultLoudVoices

        loudVoices: set[TtsMonsterVoice] = set()

        for loudVoiceString in loudVoicesStrings:
            loudVoices.add(await self.__ttsMonsterPrivateApiJsonMapper.requireVoice(loudVoiceString))

        return frozenset(loudVoices)

    async def getMediaPlayerVolume(self) -> int | None:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'media_player_volume', fallback = 10)

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from TTS Monster settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents

    async def useVoiceDependentMediaPlayerVolume(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'voice_dependent_media_player_volume', fallback = True)
