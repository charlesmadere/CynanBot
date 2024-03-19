from typing import Any

from CynanBot.authRepositorySnapshot import AuthRepositorySnapshot
from CynanBot.deepL.deepLAuthKeyProviderInterface import \
    DeepLAuthKeyProviderInterface
from CynanBot.google.googleCloudProjectIdProviderInterface import \
    GoogleCloudProjectCredentialsProviderInterface
from CynanBot.misc.clearable import Clearable
from CynanBot.storage.jsonReaderInterface import JsonReaderInterface
from CynanBot.twitch.twitchCredentialsProviderInterface import \
    TwitchCredentialsProviderInterface
from CynanBot.twitch.twitchHandleProviderInterface import \
    TwitchHandleProviderInterface
from CynanBot.weather.oneWeatherApiKeyProvider import OneWeatherApiKeyProvider


class AuthRepository(
    Clearable,
    DeepLAuthKeyProviderInterface,
    GoogleCloudProjectCredentialsProviderInterface,
    TwitchCredentialsProviderInterface,
    TwitchHandleProviderInterface,
    OneWeatherApiKeyProvider
):

    def __init__(self, authJsonReader: JsonReaderInterface):
        if not isinstance(authJsonReader, JsonReaderInterface):
            raise TypeError(f'authJsonReader argument is malformed: \"{authJsonReader}\"')

        self.__authJsonReader: JsonReaderInterface = authJsonReader
        self.__cache: AuthRepositorySnapshot | None = None

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

    async def getDeepLAuthKey(self) -> str | None:
        snapshot = await self.getAllAsync()
        return snapshot.getDeepLAuthKey()

    async def getGoogleCloudApiKey(self) -> str | None:
        snapshot = await self.getAllAsync()
        return snapshot.getGoogleCloudApiKey()

    async def getGoogleCloudProjectId(self) -> str | None:
        snapshot = await self.getAllAsync()
        return snapshot.getGoogleCloudProjectId()

    async def getOneWeatherApiKey(self) -> str | None:
        snapshot = await self.getAllAsync()
        return snapshot.getOneWeatherApiKey()

    async def getTwitchClientId(self) -> str:
        snapshot = await self.getAllAsync()
        return snapshot.requireTwitchClientId()

    async def getTwitchClientSecret(self) -> str:
        snapshot = await self.getAllAsync()
        return snapshot.requireTwitchClientSecret()

    async def getTwitchHandle(self) -> str:
        snapshot = await self.getAllAsync()
        return snapshot.requireTwitchHandle()

    def __readJson(self) -> dict[str, Any]:
        if not self.__authJsonReader.fileExists():
            raise FileNotFoundError(f'Auth Repository file not found: \"{self.__authJsonReader}\"')

        jsonContents = self.__authJsonReader.readJson()

        if jsonContents is None:
            raise IOError(f'Error reading from Auth Repository file: \"{self.__authJsonReader}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of Auth Repository file \"{self.__authJsonReader}\" is empty')

        return jsonContents

    async def __readJsonAsync(self) -> dict[str, Any]:
        if not await self.__authJsonReader.fileExistsAsync():
            raise FileNotFoundError(f'Auth Repository file not found: \"{self.__authJsonReader}\"')

        jsonContents = await self.__authJsonReader.readJsonAsync()

        if jsonContents is None:
            raise IOError(f'Error reading from Auth Repository file: \"{self.__authJsonReader}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of Auth Repository file \"{self.__authJsonReader}\" is empty')

        return jsonContents
