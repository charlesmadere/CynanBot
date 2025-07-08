from typing import Any

from .halfLifeSettingsRepositoryInterface import HalfLifeSettingsRepositoryInterface
from ..models.halfLifeVoice import HalfLifeVoice
from ..parser.halfLifeVoiceParserInterface import HalfLifeVoiceParserInterface
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class HalfLifeSettingsRepository(HalfLifeSettingsRepositoryInterface):

    def __init__(
        self,
        halfLifeJsonParser: HalfLifeVoiceParserInterface,
        settingsJsonReader: JsonReaderInterface,
        defaultVoice: HalfLifeVoice = HalfLifeVoice.INTERCOM
    ):
        if not isinstance(halfLifeJsonParser, HalfLifeVoiceParserInterface):
            raise TypeError(f'halfLifeJsonParser argument is malformed: \"{halfLifeJsonParser}\"')
        elif not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(defaultVoice, HalfLifeVoice):
            raise TypeError(f'defaultVoice argument is malformed: \"{defaultVoice}\"')

        self.__halfLifeJsonParser: HalfLifeVoiceParserInterface = halfLifeJsonParser
        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader
        self.__defaultVoice: HalfLifeVoice = defaultVoice

        self.__cache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__cache = None

    async def getDefaultVoice(self) -> HalfLifeVoice:
        jsonContents = await self.__readJson()

        defaultVoice = utils.getStrFromDict(
            d = jsonContents,
            key = 'default_voice',
            fallback = self.__halfLifeJsonParser.serializeVoice(self.__defaultVoice)
        )

        return self.__halfLifeJsonParser.requireVoice(defaultVoice)

    async def getMediaPlayerVolume(self) -> int | None:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'media_player_volume', fallback = 7)

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from Half Life settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents

    async def requireSoundsDirectory(self) -> str:
        jsonContents = await self.__readJson()
        return utils.getStrFromDict(d = jsonContents, key = 'sounds_directory', fallback = '../halfLife')
