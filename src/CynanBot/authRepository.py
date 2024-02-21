from typing import Any, Dict, Optional

from CynanBot.authRepositorySnapshot import AuthRepositorySnapshot
from CynanBot.misc.clearable import Clearable
from CynanBot.storage.jsonReaderInterface import JsonReaderInterface
from CynanBot.twitch.twitchCredentialsProviderInterface import \
    TwitchCredentialsProviderInterface
from CynanBot.twitch.twitchHandleProviderInterface import \
    TwitchHandleProviderInterface


class AuthRepository(Clearable, TwitchCredentialsProviderInterface, TwitchHandleProviderInterface):

    def __init__(self, authJsonReader: JsonReaderInterface):
        assert isinstance(authJsonReader, JsonReaderInterface), f"malformed {authJsonReader=}"

        self.__authJsonReader: JsonReaderInterface = authJsonReader

        self.__cache: Optional[AuthRepositorySnapshot] = None

    async def clearCaches(self):
        self.__cache = None

    def getAll(self) -> AuthRepositorySnapshot:
        cache = self.__cache

        if cache is not None:
            return cache

        jsonContents = self.__readJson()
        snapshot = AuthRepositorySnapshot(jsonContents)
        self.__cache = snapshot

        return snapshot

    async def getAllAsync(self) -> AuthRepositorySnapshot:
        cache = self.__cache

        if cache is not None:
            return cache

        jsonContents = await self.__readJsonAsync()
        snapshot = AuthRepositorySnapshot(jsonContents)
        self.__cache = snapshot

        return snapshot

    async def getTwitchClientId(self) -> str:
        snapshot = await self.getAllAsync()
        return snapshot.requireTwitchClientId()

    async def getTwitchClientSecret(self) -> str:
        snapshot = await self.getAllAsync()
        return snapshot.requireTwitchClientSecret()

    async def getTwitchHandle(self) -> str:
        snapshot = await self.getAllAsync()
        return snapshot.requireTwitchHandle()

    def __readJson(self) -> Dict[str, Any]:
        if not self.__authJsonReader.fileExists():
            raise FileNotFoundError(f'Auth Repository file not found: \"{self.__authJsonReader}\"')

        jsonContents = self.__authJsonReader.readJson()

        if jsonContents is None:
            raise IOError(f'Error reading from Auth Repository file: \"{self.__authJsonReader}\"')
        if len(jsonContents) == 0:
            raise ValueError(f'JSON contents of Auth Repository file \"{self.__authJsonReader}\" is empty')

        return jsonContents

    async def __readJsonAsync(self) -> Dict[str, Any]:
        if not await self.__authJsonReader.fileExistsAsync():
            raise FileNotFoundError(f'Auth Repository file not found: \"{self.__authJsonReader}\"')

        jsonContents = await self.__authJsonReader.readJsonAsync()

        if jsonContents is None:
            raise IOError(f'Error reading from Auth Repository file: \"{self.__authJsonReader}\"')
        if len(jsonContents) == 0:
            raise ValueError(f'JSON contents of Auth Repository file \"{self.__authJsonReader}\" is empty')

        return jsonContents
