from typing import Any

from .ttsMonsterSettingsRepositoryInterface import TtsMonsterSettingsRepositoryInterface
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class TtsMonsterSettingsRepository(TtsMonsterSettingsRepositoryInterface):

    def __init__(
        self,
        settingsJsonReader: JsonReaderInterface
    ):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader

        self.__cache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__cache = None

    async def getFileExtension(self) -> str:
        jsonContents = await self.__readJson()
        return utils.getStrFromDict(jsonContents, 'file_extension', fallback = 'wav')

    async def getMediaPlayerVolume(self) -> int | None:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'media_player_volume', fallback = 8)

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
