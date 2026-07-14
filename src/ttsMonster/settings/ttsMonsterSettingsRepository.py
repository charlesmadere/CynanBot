from typing import Any, Final

from frozendict import frozendict

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
        defaultVoiceVolumes: frozendict[TtsMonsterVoice, int | None] = frozendict({
            TtsMonsterVoice.BRIAN: 13,
            TtsMonsterVoice.GLADOS: 7,
            TtsMonsterVoice.JAZZ: 7,
            TtsMonsterVoice.SPONGEBOB: 7,
            TtsMonsterVoice.SHADOW: 8,
        }),
        defaultMediaPlayerVolume: int | None = 11,
        defaultDonationPrefixConfig: TtsMonsterDonationPrefixConfig = TtsMonsterDonationPrefixConfig.IF_MESSAGE_IS_BLANK,
        defaultVoice: TtsMonsterVoice = TtsMonsterVoice.BRIAN,
    ):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(ttsMonsterPrivateApiJsonMapper, TtsMonsterPrivateApiJsonMapperInterface):
            raise TypeError(f'ttsMonsterPrivateApiJsonMapper argument is malformed: \"{ttsMonsterPrivateApiJsonMapper}\"')
        elif not isinstance(defaultVoiceVolumes, frozendict):
            raise TypeError(f'defaultVoiceVolumes argument is malformed: \"{defaultVoiceVolumes}\"')
        elif defaultMediaPlayerVolume is not None and not utils.isValidInt(defaultMediaPlayerVolume):
            raise TypeError(f'defaultMediaPlayerVolume argument is malformed: \"{defaultMediaPlayerVolume}\"')
        elif defaultMediaPlayerVolume is not None and (defaultMediaPlayerVolume < 1 or defaultMediaPlayerVolume > 100):
            raise ValueError(f'defaultMediaPlayerVolume argument is out of range: {defaultMediaPlayerVolume}')
        elif not isinstance(defaultDonationPrefixConfig, TtsMonsterDonationPrefixConfig):
            raise TypeError(f'defaultDonationPrefixConfig argument is malformed: \"{defaultDonationPrefixConfig}\"')
        elif not isinstance(defaultVoice, TtsMonsterVoice):
            raise TypeError(f'defaultVoice argument is malformed: \"{defaultVoice}\"')

        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader
        self.__ttsMonsterPrivateApiJsonMapper: Final[TtsMonsterPrivateApiJsonMapperInterface] = ttsMonsterPrivateApiJsonMapper
        self.__defaultVoiceVolumes: Final[frozendict[TtsMonsterVoice, int | None]] = defaultVoiceVolumes
        self.__defaultMediaPlayerVolume: Final[int | None] = defaultMediaPlayerVolume
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
            fallback = await self.__ttsMonsterPrivateApiJsonMapper.serializeVoice(self.__defaultVoice),
        )

        return await self.__ttsMonsterPrivateApiJsonMapper.requireVoice(defaultVoiceString)

    async def getDonationPrefixConfig(self) -> TtsMonsterDonationPrefixConfig:
        jsonContents = await self.__readJson()

        donationPrefixConfigString = utils.getStrFromDict(
            d = jsonContents,
            key = 'donation_prefix_config',
            fallback = await self.__ttsMonsterPrivateApiJsonMapper.serializeDonationPrefixConfig(self.__defaultDonationPrefixConfig),
        )

        return await self.__ttsMonsterPrivateApiJsonMapper.requireDonationPrefixConfig(donationPrefixConfigString)

    async def getFileExtension(self) -> str:
        jsonContents = await self.__readJson()

        return utils.getStrFromDict(
            d = jsonContents,
            key = 'file_extension',
            fallback = 'wav',
        )

    async def getMediaPlayerVolume(self) -> int | None:
        jsonContents = await self.__readJson()

        return utils.getIntFromDict(
            d = jsonContents,
            key = 'media_player_volume',
            fallback = self.__defaultMediaPlayerVolume,
        )

    async def getVoiceVolumes(self) -> frozendict[TtsMonsterVoice, int | None]:
        jsonContents = await self.__readJson()
        rawVoiceToVolume: dict[str, int | None] | None = jsonContents.get('voice_volumes', None)
        voiceToVolume: dict[TtsMonsterVoice, int | None] = dict()

        for voice, volume in self.__defaultVoiceVolumes.items():
            voiceToVolume[voice] = volume

        if rawVoiceToVolume is not None and len(rawVoiceToVolume) >= 1:
            for voiceString, volume in rawVoiceToVolume.items():
                voice = await self.__ttsMonsterPrivateApiJsonMapper.requireVoice(voiceString)
                voiceToVolume[voice] = volume

        defaultVoiceVolume = await self.getMediaPlayerVolume()

        for voice in TtsMonsterVoice:
            if voice not in voiceToVolume or voiceToVolume.get(voice) is None:
                voiceToVolume[voice] = defaultVoiceVolume

        return frozendict(voiceToVolume)

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
