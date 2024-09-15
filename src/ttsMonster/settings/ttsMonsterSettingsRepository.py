from typing import Any

from .ttsMonsterSettingsRepositoryInterface import TtsMonsterSettingsRepositoryInterface
from ..mapper.ttsMonsterWebsiteVoiceMapperInterface import TtsMonsterWebsiteVoiceMapperInterface
from ..models.ttsMonsterWebsiteVoice import TtsMonsterWebsiteVoice
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class TtsMonsterSettingsRepository(TtsMonsterSettingsRepositoryInterface):

    def __init__(
        self,
        settingsJsonReader: JsonReaderInterface,
        ttsMonsterWebsiteVoiceMapper: TtsMonsterWebsiteVoiceMapperInterface,
        defaultVoice: TtsMonsterWebsiteVoice = TtsMonsterWebsiteVoice.BRIAN
    ):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(ttsMonsterWebsiteVoiceMapper, TtsMonsterWebsiteVoiceMapperInterface):
            raise TypeError(f'ttsMonsterWebsiteVoiceMapper argument is malformed: \"{ttsMonsterWebsiteVoiceMapper}\"')
        elif not isinstance(defaultVoice, TtsMonsterWebsiteVoice):
            raise TypeError(f'defaultVoice argument is malformed: \"{defaultVoice}\"')

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader
        self.__ttsMonsterWebsiteVoiceMapper: TtsMonsterWebsiteVoiceMapperInterface = ttsMonsterWebsiteVoiceMapper
        self.__defaultVoice: TtsMonsterWebsiteVoice = defaultVoice

        self.__cache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__cache = None

    async def getDefaultVoice(self) -> TtsMonsterWebsiteVoice:
        jsonContents = await self.__readJson()

        defaultVoice = utils.getStrFromDict(
            d = jsonContents,
            key = 'default_voice',
            fallback = self.__defaultVoice.websiteName
        )

        return await self.__ttsMonsterWebsiteVoiceMapper.fromWebsiteName(defaultVoice)

    async def getMediaPlayerVolume(self) -> int | None:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'media_player_volume', fallback = 48)

    async def isReturnCharacterUsageEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'is_return_character_usage_enabled', fallback = True)

    async def isUsePrivateApiEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'is_use_private_api_enabled', fallback = True)

    async def isWebsiteVoiceEnabled(self, websiteVoice: TtsMonsterWebsiteVoice) -> bool:
        if not isinstance(websiteVoice, TtsMonsterWebsiteVoice):
            raise TypeError(f'websiteVoice argument is malformed: \"{websiteVoice}\"')

        websiteName = websiteVoice.websiteName.lower()
        jsonContents = await self.__readJson()

        return utils.getBoolFromDict(
            d = jsonContents,
            key = f'is_{websiteName}_enabled',
            fallback = False
        )

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None = None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if jsonContents is None:
            raise IOError(f'Error reading from TTS Monster settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents
