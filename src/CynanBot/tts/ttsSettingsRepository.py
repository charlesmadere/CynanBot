from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.google.googleJsonMapperInterface import GoogleJsonMapperInterface
from CynanBot.google.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding
from CynanBot.storage.jsonReaderInterface import JsonReaderInterface
from CynanBot.tts.ttsSettingsRepositoryInterface import \
    TtsSettingsRepositoryInterface


class TtsSettingsRepository(TtsSettingsRepositoryInterface):

    def __init__(
        self,
        googleJsonMapper: GoogleJsonMapperInterface,
        settingsJsonReader: JsonReaderInterface,
        defaultGoogleVoiceAudioEncoding: GoogleVoiceAudioEncoding = GoogleVoiceAudioEncoding.OGG_OPUS
    ):
        if not isinstance(googleJsonMapper, GoogleJsonMapperInterface):
            raise TypeError(f'googleJsonMapper argument is malformed: \"{googleJsonMapper}\"')
        elif not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(defaultGoogleVoiceAudioEncoding, GoogleVoiceAudioEncoding):
            raise TypeError(f'defaultGoogleVoiceAudioEncoding argument is malformed: \"{defaultGoogleVoiceAudioEncoding}\"')

        self.__googleJsonMapper: GoogleJsonMapperInterface = googleJsonMapper
        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader
        self.__defaultGoogleVoiceAudioEncoding: GoogleVoiceAudioEncoding = defaultGoogleVoiceAudioEncoding

        self.__settingsCache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__settingsCache = None

    async def getGoogleVoiceAudioEncoding(self) -> GoogleVoiceAudioEncoding:
        jsonContents = await self.__readJson()

        defaultAudioEncoding = await self.__googleJsonMapper.serializeVoiceAudioEncoding(
            voiceAudioEncoding = self.__defaultGoogleVoiceAudioEncoding
        )

        audioEncodingString = utils.getStrFromDict(
            d = jsonContents,
            key = 'googleVoiceAudioEncoding',
            fallback = defaultAudioEncoding
        )

        audioEncoding = await self.__googleJsonMapper.parseVoiceAudioEncoding(
            jsonString = audioEncodingString
        )

        if audioEncoding is None:
            return self.__defaultGoogleVoiceAudioEncoding
        else:
            return audioEncoding

    async def getGoogleVolumeGainDb(self) -> float | None:
        jsonContents = await self.__readJson()
        return utils.getFloatFromDict(jsonContents, 'googleVolumeGainDb', fallback = -5)

    async def getMaximumMessageSize(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'maxMessageSize', fallback = 200)

    async def getTtsDelayBetweenSeconds(self) -> float:
        jsonContents = await self.__readJson()

        ttsDelayBetweenSeconds = utils.getFloatFromDict(
            d = jsonContents,
            key = 'ttsDelayBetweenSeconds',
            fallback = 0.25
        )

        if ttsDelayBetweenSeconds < 0 or ttsDelayBetweenSeconds > 10:
            raise ValueError(f'ttsDelayBetweenSeconds is out of bounds: \"{ttsDelayBetweenSeconds}\"')

        return ttsDelayBetweenSeconds

    async def getTtsTimeoutSeconds(self) -> float:
        jsonContents = await self.__readJson()

        ttsTimeoutSeconds = utils.getFloatFromDict(
            d = jsonContents,
            key = 'ttsTimeoutSeconds',
            fallback = 10
        )

        if ttsTimeoutSeconds < 0 or ttsTimeoutSeconds > 30:
            raise ValueError(f'ttsTimeoutSeconds is out of bounds: \"{ttsTimeoutSeconds}\"')

        return ttsTimeoutSeconds

    async def isEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'isEnabled', fallback = False)

    async def __readJson(self) -> dict[str, Any]:
        if self.__settingsCache is not None:
            return self.__settingsCache

        jsonContents: dict[str, Any] | None = None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if jsonContents is None:
            raise IOError(f'Error reading from TTS settings file: {self.__settingsJsonReader}')

        self.__settingsCache = jsonContents
        return jsonContents

    async def requireDecTalkPath(self) -> str:
        jsonContents = await self.__readJson()
        decTalkPath = utils.getStrFromDict(jsonContents, 'decTalkPath', fallback = '')

        if not utils.isValidStr(decTalkPath):
            raise ValueError(f'\"decTalkPath\" value is malformed: \"{decTalkPath}\"')

        return decTalkPath
