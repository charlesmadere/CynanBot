from typing import Any

from .ttsMonsterSettingsRepositoryInterface import TtsMonsterSettingsRepositoryInterface
from ..mapper.ttsMonsterPrivateApiJsonMapperInterface import TtsMonsterPrivateApiJsonMapperInterface
from ..models.ttsMonsterVoice import TtsMonsterVoice
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class TtsMonsterSettingsRepository(TtsMonsterSettingsRepositoryInterface):

    def __init__(
        self,
        settingsJsonReader: JsonReaderInterface,
        ttsMonsterPrivateApiJsonMapper: TtsMonsterPrivateApiJsonMapperInterface,
        defaultVoice: TtsMonsterVoice = TtsMonsterVoice.BRIAN
    ):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(ttsMonsterPrivateApiJsonMapper, TtsMonsterPrivateApiJsonMapperInterface):
            raise TypeError(f'ttsMonsterPrivateApiJsonMapper argument is malformed: \"{ttsMonsterPrivateApiJsonMapper}\"')
        elif not isinstance(defaultVoice, TtsMonsterVoice):
            raise TypeError(f'defaultVoice argument is malformed: \"{defaultVoice}\"')

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader
        self.__ttsMonsterPrivateApiJsonMapper: TtsMonsterPrivateApiJsonMapperInterface = ttsMonsterPrivateApiJsonMapper
        self.__defaultVoice: TtsMonsterVoice = defaultVoice

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

    async def getFileExtension(self) -> str:
        jsonContents = await self.__readJson()
        return utils.getStrFromDict(jsonContents, 'file_extension', fallback = 'wav')

    async def getLoudVoiceMediaPlayerVolume(self) -> int | None:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'loud_voice_media_player_volume', fallback = 7)

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

    async def useDonationPrefix(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'use_donation_prefix', fallback = False)

    async def useVoiceDependentMediaPlayerVolume(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'voice_dependent_media_player_volume', fallback = True)
