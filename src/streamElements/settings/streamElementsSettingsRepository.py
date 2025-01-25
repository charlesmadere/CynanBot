from typing import Any

from .streamElementsSettingsRepositoryInterface import StreamElementsSettingsRepositoryInterface
from ..models.streamElementsVoice import StreamElementsVoice
from ..parser.streamElementsJsonParserInterface import StreamElementsJsonParserInterface
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class StreamElementsSettingsRepository(StreamElementsSettingsRepositoryInterface):

    def __init__(
        self,
        settingsJsonReader: JsonReaderInterface,
        streamElementsJsonParser: StreamElementsJsonParserInterface,
        defaultVoice: StreamElementsVoice = StreamElementsVoice.JOEY
    ):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(streamElementsJsonParser, StreamElementsJsonParserInterface):
            raise TypeError(f'streamElementsJsonParser argument is malformed: \"{streamElementsJsonParser}\"')
        elif not isinstance(defaultVoice, StreamElementsVoice):
            raise TypeError(f'defaultVoice argument is malformed: \"{defaultVoice}\"')

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader
        self.__streamElementsJsonParser: StreamElementsJsonParserInterface = streamElementsJsonParser
        self.__defaultVoice: StreamElementsVoice = defaultVoice

        self.__cache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__cache = None

    async def getDefaultVoice(self) -> StreamElementsVoice:
        jsonContents = await self.__readJson()

        defaultVoice = utils.getStrFromDict(
            d = jsonContents,
            key = 'default_voice',
            fallback = self.__streamElementsJsonParser.serializeVoice(self.__defaultVoice)
        )

        return self.__streamElementsJsonParser.requireVoice(defaultVoice)

    async def getMediaPlayerVolume(self) -> int | None:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'media_player_volume', fallback = 40)

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None = None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if jsonContents is None:
            raise IOError(f'Error reading from Stream Elements settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents
