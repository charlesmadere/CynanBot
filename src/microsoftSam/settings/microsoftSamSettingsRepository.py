from typing import Any

from .microsoftSamSettingsRepositoryInterface import MicrosoftSamSettingsRepositoryInterface
from ..microsoftSamJsonParserInterface import MicrosoftSamJsonParserInterface
from ..models.microsoftSamVoice import MicrosoftSamVoice
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class MicrosoftSamSettingsRepository(MicrosoftSamSettingsRepositoryInterface):

    def __init__(
        self,
        microsoftSamJsonParser: MicrosoftSamJsonParserInterface,
        settingsJsonReader: JsonReaderInterface,
        defaultVoice: MicrosoftSamVoice = MicrosoftSamVoice.SAM
    ):
        if not isinstance(microsoftSamJsonParser, MicrosoftSamJsonParserInterface):
            raise TypeError(f'microsoftSamJsonParser argument is malformed: \"{microsoftSamJsonParser}\"')
        elif not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(defaultVoice, MicrosoftSamVoice):
            raise TypeError(f'defaultVoice argument is malformed: \"{defaultVoice}\"')

        self.__microsoftSamJsonParser: MicrosoftSamJsonParserInterface = microsoftSamJsonParser
        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader
        self.__defaultVoice: MicrosoftSamVoice = defaultVoice

        self.__cache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__cache = None

    async def getDefaultVoice(self) -> MicrosoftSamVoice | None:
        jsonContents = await self.__readJson()

        defaultVoice = utils.getStrFromDict(
            d = jsonContents,
            key = 'defaultVoice',
            fallback = self.__microsoftSamJsonParser.serializeVoice(self.__defaultVoice)
        )

        return self.__microsoftSamJsonParser.requireVoice(defaultVoice)

    async def getMediaPlayerVolume(self) -> int | None:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'mediaPlayerVolume', fallback = 46)

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None = None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from Microsoft Sam settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents
