from typing import Any, Final

from frozendict import frozendict

from .authRepositorySnapshot import AuthRepositorySnapshot
from .clearable import Clearable
from ..deepL.deepLAuthKeyProviderInterface import DeepLAuthKeyProviderInterface
from ..google.googleCloudProjectCredentialsProviderInterface import GoogleCloudProjectCredentialsProviderInterface
from ..openWeather.apiService.openWeatherApiKeyProvider import OpenWeatherApiKeyProvider
from ..storage.jsonReaderInterface import JsonReaderInterface
from ..twitch.credentialsProvider.twitchCredentialsProviderInterface import TwitchCredentialsProviderInterface
from ..twitch.handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface


class AuthRepository(
    Clearable,
    DeepLAuthKeyProviderInterface,
    GoogleCloudProjectCredentialsProviderInterface,
    OpenWeatherApiKeyProvider,
    TwitchCredentialsProviderInterface,
    TwitchHandleProviderInterface,
):

    def __init__(self, authJsonReader: JsonReaderInterface):
        if not isinstance(authJsonReader, JsonReaderInterface):
            raise TypeError(f'authJsonReader argument is malformed: \"{authJsonReader}\"')

        self.__authJsonReader: Final[JsonReaderInterface] = authJsonReader
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

    async def getGoogleCloudProjectKeyId(self) -> str | None:
        snapshot = await self.getAllAsync()
        return snapshot.getGoogleCloudProjectKeyId()

    async def getGoogleCloudProjectId(self) -> str | None:
        snapshot = await self.getAllAsync()
        return snapshot.getGoogleCloudProjectId()

    async def getGoogleCloudProjectPrivateKey(self) -> str | None:
        snapshot = await self.getAllAsync()
        return snapshot.getGoogleCloudProjectPrivateKey()

    async def getGoogleCloudServiceAccountEmail(self) -> str | None:
        snapshot = await self.getAllAsync()
        return snapshot.getGoogleCloudServiceAccountEmail()

    async def getOpenWeatherApiKey(self) -> str | None:
        snapshot = await self.getAllAsync()
        return snapshot.getOpenWeatherApiKey()

    async def getTwitchClientId(self) -> str:
        snapshot = await self.getAllAsync()
        return snapshot.requireTwitchClientId()

    async def getTwitchClientSecret(self) -> str:
        snapshot = await self.getAllAsync()
        return snapshot.requireTwitchClientSecret()

    async def getTwitchHandle(self) -> str:
        snapshot = await self.getAllAsync()
        return snapshot.requireTwitchHandle()

    def __readJson(self) -> frozendict[str, Any]:
        if not self.__authJsonReader.fileExists():
            raise FileNotFoundError(f'Auth Repository file not found ({self.__authJsonReader=})')

        jsonContents = self.__authJsonReader.readJson()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from Auth Repository file ({self.__authJsonReader=})')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of Auth Repository file ({self.__authJsonReader=}) ({jsonContents=})')

        return frozendict(jsonContents)

    async def __readJsonAsync(self) -> frozendict[str, Any]:
        if not await self.__authJsonReader.fileExistsAsync():
            raise FileNotFoundError(f'Auth Repository file not found ({self.__authJsonReader=})')

        jsonContents = await self.__authJsonReader.readJsonAsync()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from Auth Repository file ({self.__authJsonReader=})')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of Auth Repository file is empty ({self.__authJsonReader=}) ({jsonContents=})')

        return frozendict(jsonContents)
