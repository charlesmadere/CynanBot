from typing import Any

from .ttsMonsterKeyAndUserId import TtsMonsterKeyAndUserId
from .ttsMonsterKeyAndUserIdRepositoryInterface import TtsMonsterKeyAndUserIdRepositoryInterface
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class TtsMonsterKeyAndUserIdRepository(TtsMonsterKeyAndUserIdRepositoryInterface):

    def __init__(self, settingsJsonReader: JsonReaderInterface):
        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader

        self.__settingsCache: dict[str, Any] | None = None

    async def clearCaches(self):
        self.__settingsCache = None

    async def get(self, twitchChannel: str) -> TtsMonsterKeyAndUserId | None:
        jsonContents = await self.__readJson()
        userConfiguration: dict[str, Any] | Any | None = jsonContents.get(twitchChannel.lower())

        if not isinstance(userConfiguration, dict) or len(userConfiguration) == 0:
            return None

        key = utils.getStrFromDict(userConfiguration, 'key', fallback = '')
        userId = utils.getStrFromDict(userConfiguration, 'userId', fallback = '')

        if not utils.isValidStr(key) or not utils.isValidStr(userId):
            return None

        return TtsMonsterKeyAndUserId(
            key = key,
            twitchChannel = twitchChannel,
            userId = userId
        )

    async def __readJson(self) -> dict[str, Any]:
        if self.__settingsCache is not None:
            return self.__settingsCache

        jsonContents: dict[str, Any] | None = None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if jsonContents is None:
            raise IOError(f'Error reading from TTS Monster Key and User ID repository file: {self.__settingsJsonReader}')

        self.__settingsCache = jsonContents
        return jsonContents
