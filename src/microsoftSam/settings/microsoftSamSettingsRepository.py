from typing import Any, Final

from .microsoftSamSettingsRepositoryInterface import MicrosoftSamSettingsRepositoryInterface
from ..models.microsoftSamVoice import MicrosoftSamVoice
from ..parser.microsoftSamJsonParserInterface import MicrosoftSamJsonParserInterface
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class MicrosoftSamSettingsRepository(MicrosoftSamSettingsRepositoryInterface):

    def __init__(
        self,
        microsoftSamJsonParser: MicrosoftSamJsonParserInterface,
        settingsJsonReader: JsonReaderInterface,
        defaultMediaPlayerVolume: int = 36,
        defaultVoice: MicrosoftSamVoice = MicrosoftSamVoice.SAM,
        defaultFileExtension: str = 'wav',
    ):
        if not isinstance(microsoftSamJsonParser, MicrosoftSamJsonParserInterface):
            raise TypeError(f'microsoftSamJsonParser argument is malformed: \"{microsoftSamJsonParser}\"')
        elif not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not utils.isValidInt(defaultMediaPlayerVolume):
            raise TypeError(f'defaultMediaPlayerVolume argument is malformed: \"{defaultMediaPlayerVolume}\"')
        elif defaultMediaPlayerVolume < 1 or defaultMediaPlayerVolume > 100:
            raise ValueError(f'defaultMediaPlayerVolume argument is out of bounds: {defaultMediaPlayerVolume}')
        elif not isinstance(defaultVoice, MicrosoftSamVoice):
            raise TypeError(f'defaultVoice argument is malformed: \"{defaultVoice}\"')
        elif not utils.isValidStr(defaultFileExtension):
            raise TypeError(f'defaultFileExtension argument is malformed: \"{defaultFileExtension}\"')

        self.__microsoftSamJsonParser: Final[MicrosoftSamJsonParserInterface] = microsoftSamJsonParser
        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader
        self.__defaultMediaPlayerVolume: Final[int] = defaultMediaPlayerVolume
        self.__defaultVoice: Final[MicrosoftSamVoice] = defaultVoice
        self.__defaultFileExtension: Final[str] = defaultFileExtension

        self.__cache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__cache = None

    async def getDefaultVoice(self) -> MicrosoftSamVoice:
        jsonContents = await self.__readJson()

        defaultVoice = utils.getStrFromDict(
            d = jsonContents,
            key = 'defaultVoice',
            fallback = await self.__microsoftSamJsonParser.serializeVoice(self.__defaultVoice),
        )

        return await self.__microsoftSamJsonParser.requireVoice(defaultVoice)

    async def getFileExtension(self) -> str:
        jsonContents = await self.__readJson()

        return utils.getStrFromDict(
            d = jsonContents,
            key = 'fileExtension',
            fallback = self.__defaultFileExtension,
        )

    async def getMediaPlayerVolume(self) -> int | None:
        jsonContents = await self.__readJson()

        return utils.getIntFromDict(
            d = jsonContents,
            key = 'mediaPlayerVolume',
            fallback = self.__defaultMediaPlayerVolume,
        )

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from Microsoft Sam settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents

    async def useDonationPrefix(self) -> bool:
        jsonContents = await self.__readJson()

        return utils.getBoolFromDict(
            d = jsonContents,
            key = 'useDonationPrefix',
            fallback = True,
        )
