from typing import Any

from .clearable import Clearable
from .generalSettingsRepositorySnapshot import GeneralSettingsRepositorySnapshot
from ..network.networkClientType import NetworkClientType
from ..network.networkJsonMapperInterface import NetworkJsonMapperInterface
from ..soundPlayerManager.jsonMapper.soundPlayerJsonMapperInterface import SoundPlayerJsonMapperInterface
from ..soundPlayerManager.soundPlayerType import SoundPlayerType
from ..storage.databaseType import DatabaseType
from ..storage.jsonReaderInterface import JsonReaderInterface
from ..storage.storageJsonMapperInterface import StorageJsonMapperInterface
from ..trivia.builder.triviaGameBuilderSettingsInterface import TriviaGameBuilderSettingsInterface


class GeneralSettingsRepository(
    Clearable,
    TriviaGameBuilderSettingsInterface
):

    def __init__(
        self,
        settingsJsonReader: JsonReaderInterface,
        networkJsonMapper: NetworkJsonMapperInterface,
        soundPlayerJsonMapper: SoundPlayerJsonMapperInterface,
        storageJsonMapper: StorageJsonMapperInterface,
        defaultDatabaseType: DatabaseType = DatabaseType.SQLITE,
        defaultNetworkClientType: NetworkClientType = NetworkClientType.AIOHTTP,
        defaultSoundPlayerType: SoundPlayerType = SoundPlayerType.AUDIO_PLAYER,
    ):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(networkJsonMapper, NetworkJsonMapperInterface):
            raise TypeError(f'networkJsonMapper argument is malformed: \"{networkJsonMapper}\"')
        elif not isinstance(soundPlayerJsonMapper, SoundPlayerJsonMapperInterface):
            raise TypeError(f'soundPlayerJsonMapper argument is malformed: \"{soundPlayerJsonMapper}\"')
        elif not isinstance(storageJsonMapper, StorageJsonMapperInterface):
            raise TypeError(f'storageJsonMapper argument is malformed: \"{storageJsonMapper}\"')
        elif not isinstance(defaultDatabaseType, DatabaseType):
            raise TypeError(f'defaultDatabaseType argument is malformed: \"{defaultDatabaseType}\"')
        elif not isinstance(defaultNetworkClientType, NetworkClientType):
            raise TypeError(f'defaultNetworkClientType argument is malformed: \"{defaultNetworkClientType}\"')
        elif not isinstance(defaultSoundPlayerType, SoundPlayerType):
            raise TypeError(f'defaultSoundPlayerType argument is malformed: \"{defaultSoundPlayerType}\"')

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader
        self.__networkJsonMapper: NetworkJsonMapperInterface = networkJsonMapper
        self.__soundPlayerJsonMapper: SoundPlayerJsonMapperInterface = soundPlayerJsonMapper
        self.__storageJsonMapper: StorageJsonMapperInterface = storageJsonMapper
        self.__defaultDatabaseType: DatabaseType = defaultDatabaseType
        self.__defaultNetworkClientType: NetworkClientType = defaultNetworkClientType
        self.__defaultSoundPlayerType: SoundPlayerType = defaultSoundPlayerType

        self.__cache: GeneralSettingsRepositorySnapshot | None = None

    async def clearCaches(self):
        self.__cache = None

    async def getAdministrator(self) -> str:
        snapshot = await self.getAllAsync()
        return snapshot.requireAdministrator()

    def getAll(self) -> GeneralSettingsRepositorySnapshot:
        if self.__cache is not None:
            return self.__cache

        jsonContents = self.__readJson()

        snapshot = GeneralSettingsRepositorySnapshot(
            defaultDatabaseType = self.__defaultDatabaseType,
            defaultNetworkClientType = self.__defaultNetworkClientType,
            jsonContents = jsonContents,
            networkJsonMapper = self.__networkJsonMapper,
            soundPlayerJsonMapper = self.__soundPlayerJsonMapper,
            defaultSoundPlayerType = self.__defaultSoundPlayerType,
            storageJsonMapper = self.__storageJsonMapper
        )

        self.__cache = snapshot
        return snapshot

    async def getAllAsync(self) -> GeneralSettingsRepositorySnapshot:
        if self.__cache is not None:
            return self.__cache

        jsonContents = await self.__readJsonAsync()

        snapshot = GeneralSettingsRepositorySnapshot(
            defaultDatabaseType = self.__defaultDatabaseType,
            defaultNetworkClientType = self.__defaultNetworkClientType,
            jsonContents = jsonContents,
            networkJsonMapper = self.__networkJsonMapper,
            soundPlayerJsonMapper = self.__soundPlayerJsonMapper,
            defaultSoundPlayerType = self.__defaultSoundPlayerType,
            storageJsonMapper = self.__storageJsonMapper
        )

        self.__cache = snapshot
        return snapshot

    async def getSuperTriviaGamePerUserAttempts(self) -> int:
        snapshot = await self.getAllAsync()
        return snapshot.getSuperTriviaGamePerUserAttempts()

    async def getSuperTriviaGamePoints(self) -> int:
        snapshot = await self.getAllAsync()
        return snapshot.getSuperTriviaGamePoints()

    async def getSuperTriviaGameShinyMultiplier(self) -> int:
        snapshot = await self.getAllAsync()
        return snapshot.getSuperTriviaGameShinyMultiplier()

    async def getSuperTriviaGameToxicMultiplier(self) -> int:
        snapshot = await self.getAllAsync()
        return snapshot.getSuperTriviaGameToxicMultiplier()

    async def getSuperTriviaGameToxicPunishmentMultiplier(self) -> int:
        snapshot = await self.getAllAsync()
        return snapshot.getSuperTriviaGameToxicPunishmentMultiplier()

    async def getTriviaGamePoints(self) -> int:
        snapshot = await self.getAllAsync()
        return snapshot.getTriviaGamePoints()

    async def getTriviaGameShinyMultiplier(self) -> int:
        snapshot = await self.getAllAsync()
        return snapshot.getTriviaGameShinyMultiplier()

    async def getWaitForSuperTriviaAnswerDelay(self) -> int:
        snapshot = await self.getAllAsync()
        return snapshot.getWaitForSuperTriviaAnswerDelay()

    async def getWaitForTriviaAnswerDelay(self) -> int:
        snapshot = await self.getAllAsync()
        return snapshot.getWaitForTriviaAnswerDelay()

    async def isSuperTriviaGameEnabled(self) -> bool:
        snapshot = await self.getAllAsync()
        return snapshot.isSuperTriviaGameEnabled()

    async def isTriviaGameEnabled(self) -> bool:
        snapshot = await self.getAllAsync()
        return snapshot.isTriviaGameEnabled()

    def __readJson(self) -> dict[str, Any]:
        if not self.__settingsJsonReader.fileExists():
            raise FileNotFoundError(f'General Settings file not found: \"{self.__settingsJsonReader}\"')

        jsonContents = self.__settingsJsonReader.readJson()

        if jsonContents is None:
            raise IOError(f'Error reading from General Settings file: \"{self.__settingsJsonReader}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of General Settings file \"{self.__settingsJsonReader}\" is empty')

        return jsonContents

    async def __readJsonAsync(self) -> dict[str, Any]:
        if not await self.__settingsJsonReader.fileExistsAsync():
            raise FileNotFoundError(f'General Settings file not found: \"{self.__settingsJsonReader}\"')

        jsonContents = await self.__settingsJsonReader.readJsonAsync()

        if jsonContents is None:
            raise IOError(f'Error reading from General Settings file: \"{self.__settingsJsonReader}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of General Settings file \"{self.__settingsJsonReader}\" is empty')

        return jsonContents
