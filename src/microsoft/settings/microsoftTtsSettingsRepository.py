from typing import Any, Final

from .microsoftTtsSettingsRepositoryInterface import MicrosoftTtsSettingsRepositoryInterface
from ..models.microsoftTtsVoice import MicrosoftTtsVoice
from ..parser.microsoftTtsJsonParserInterface import MicrosoftTtsJsonParserInterface
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class MicrosoftTtsSettingsRepository(MicrosoftTtsSettingsRepositoryInterface):

    def __init__(
        self,
        microsoftTtsJsonParser: MicrosoftTtsJsonParserInterface,
        settingsJsonReader: JsonReaderInterface,
        defaultVoice: MicrosoftTtsVoice = MicrosoftTtsVoice.ZIRA,
    ):
        if not isinstance(microsoftTtsJsonParser, MicrosoftTtsJsonParserInterface):
            raise TypeError(f'microsoftTtsJsonParser argument is malformed: \"{microsoftTtsJsonParser}\"')
        elif not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(defaultVoice, MicrosoftTtsVoice):
            raise TypeError(f'defaultVoice argument is malformed: \"{defaultVoice}\"')

        self.__microsoftTtsJsonParser: Final[MicrosoftTtsJsonParserInterface] = microsoftTtsJsonParser
        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader
        self.__defaultVoice: Final[MicrosoftTtsVoice] = defaultVoice

        self.__cache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__cache = None

    async def getDefaultVoice(self) -> MicrosoftTtsVoice | None:
        jsonContents = await self.__readJson()

        fallbackVoice = await self.__microsoftTtsJsonParser.serializeVoice(
            voice = self.__defaultVoice,
        )

        defaultVoice = utils.getStrFromDict(
            d = jsonContents,
            key = 'defaultVoice',
            fallback = fallbackVoice,
        )

        return await self.__microsoftTtsJsonParser.requireVoice(
            string = defaultVoice,
        )

    async def getFileExtension(self) -> str:
        jsonContents = await self.__readJson()
        return utils.getStrFromDict(jsonContents, 'fileExtension', fallback = 'wav')

    async def getMediaPlayerVolume(self) -> int | None:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'mediaPlayerVolume', fallback = 10)

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from Microsoft Tts settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents

    async def useDonationPrefix(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'useDonationPrefix', fallback = True)
