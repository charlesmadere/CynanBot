from typing import Any, Final

from frozendict import frozendict

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
        defaultVoiceVolumes: frozendict[HalfLifeVoice, int | None] | None = frozendict({
            HalfLifeVoice.INTERCOM: 4,
            HalfLifeVoice.SCIENTIST: 4,
            HalfLifeVoice.SOLDIER: 2,
        }),
        defaultVoice: HalfLifeVoice = HalfLifeVoice.ALL,
    ):
        if not isinstance(halfLifeJsonParser, HalfLifeVoiceParserInterface):
            raise TypeError(f'halfLifeJsonParser argument is malformed: \"{halfLifeJsonParser}\"')
        elif not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif defaultVoiceVolumes is not None and not isinstance(defaultVoiceVolumes, frozendict):
            raise TypeError(f'defaultVoiceVolumes argument is malformed: \"{defaultVoiceVolumes}\"')
        elif not isinstance(defaultVoice, HalfLifeVoice):
            raise TypeError(f'defaultVoice argument is malformed: \"{defaultVoice}\"')

        self.__halfLifeJsonParser: Final[HalfLifeVoiceParserInterface] = halfLifeJsonParser
        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader
        self.__defaultVoiceVolumes: Final[frozendict[HalfLifeVoice, int | None] | None] = defaultVoiceVolumes
        self.__defaultVoice: Final[HalfLifeVoice] = defaultVoice

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
        return utils.getIntFromDict(jsonContents, 'media_player_volume', fallback = 5)

    async def getVoiceVolumes(self) -> frozendict[HalfLifeVoice, int | None]:
        jsonContents = await self.__readJson()
        rawVoiceVolumes: dict[str, int] | None = jsonContents.get('voice_volumes', None)

        if rawVoiceVolumes is None:
            return self.__defaultVoiceVolumes

        voiceVolumes: dict[HalfLifeVoice, int | None] = dict()

        for voiceString, volume in rawVoiceVolumes.items():
            voice = self.__halfLifeJsonParser.requireVoice(voiceString)
            voiceVolumes[voice] = volume

        return frozendict(voiceVolumes)

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

    async def requireFileExtension(self) -> str:
        jsonContents = await self.__readJson()
        return utils.getStrFromDict(jsonContents, 'file_extension', fallback = 'wav')

    async def requireSoundsDirectory(self) -> str:
        jsonContents = await self.__readJson()
        return utils.getStrFromDict(jsonContents, 'sounds_directory', fallback = '../halfLife')
