from typing import Any

from .googleSettingsRepositoryInterface import GoogleSettingsRepositoryInterface
from ..jsonMapper.googleJsonMapperInterface import GoogleJsonMapperInterface
from ..models.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class GoogleSettingsRepository(GoogleSettingsRepositoryInterface):

    def __init__(
        self,
        googleJsonMapper: GoogleJsonMapperInterface,
        settingsJsonReader: JsonReaderInterface,
        defaultVoiceAudioEncoding: GoogleVoiceAudioEncoding = GoogleVoiceAudioEncoding.MP3
    ):
        if not isinstance(googleJsonMapper, GoogleJsonMapperInterface):
            raise TypeError(f'googleJsonMapper argument is malformed: \"{googleJsonMapper}\"')
        elif not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(defaultVoiceAudioEncoding, GoogleVoiceAudioEncoding):
            raise TypeError(f'defaultVoiceAudioEncoding argument is malformed: \"{defaultVoiceAudioEncoding}\"')

        self.__googleJsonMapper: GoogleJsonMapperInterface = googleJsonMapper
        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader
        self.__defaultVoiceAudioEncoding: GoogleVoiceAudioEncoding = defaultVoiceAudioEncoding

        self.__cache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__cache = None

    async def getMediaPlayerVolume(self) -> int | None:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'media_player_volume', fallback = 10)

    async def getVoiceAudioEncoding(self) -> GoogleVoiceAudioEncoding:
        jsonContents = await self.__readJson()

        defaultAudioEncoding = await self.__googleJsonMapper.serializeVoiceAudioEncoding(
            voiceAudioEncoding = self.__defaultVoiceAudioEncoding
        )

        audioEncodingString = utils.getStrFromDict(
            d = jsonContents,
            key = 'googleVoiceAudioEncoding',
            fallback = defaultAudioEncoding
        )

        return await self.__googleJsonMapper.requireVoiceAudioEncoding(
            jsonString = audioEncodingString
        )

    async def getVolumeGainDb(self) -> float | None:
        jsonContents = await self.__readJson()

        volumeGainDb: float | None = None
        if 'volume_gain_db' in jsonContents and utils.isValidNum(jsonContents.get('volume_gain_db')):
            volumeGainDb = utils.getFloatFromDict(jsonContents, 'volume_gain_db')

        return volumeGainDb

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from Google settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents

    async def useDonationPrefix(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'use_donation_prefix', fallback = True)
