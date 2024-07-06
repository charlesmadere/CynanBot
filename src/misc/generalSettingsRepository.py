from typing import Any

from .clearable import Clearable
from .generalSettingsRepositorySnapshot import GeneralSettingsRepositorySnapshot
from ..storage.jsonReaderInterface import JsonReaderInterface
from ..storage.storageJsonMapperInterface import StorageJsonMapperInterface
from ..trivia.builder.triviaGameBuilderSettingsInterface import TriviaGameBuilderSettingsInterface


class GeneralSettingsRepository(Clearable, TriviaGameBuilderSettingsInterface):

    def __init__(
        self,
        settingsJsonReader: JsonReaderInterface,
        storageJsonMapper: StorageJsonMapperInterface
    ):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(storageJsonMapper, StorageJsonMapperInterface):
            raise TypeError(f'storageJsonMapper argument is malformed: \"{storageJsonMapper}\"')

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader
        self.__storageJsonMapper: StorageJsonMapperInterface = storageJsonMapper

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
            jsonContents = jsonContents,
            storageJsonMapper = self.__storageJsonMapper
        )

        self.__cache = snapshot
        return snapshot

    async def getAllAsync(self) -> GeneralSettingsRepositorySnapshot:
        if self.__cache is not None:
            return self.__cache

        jsonContents = await self.__readJsonAsync()
        snapshot = GeneralSettingsRepositorySnapshot(
            jsonContents = jsonContents,
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

    async def isCommandsChatCommandEnabled(self) -> bool:
        snapshot = await self.getAllAsync()
        return snapshot.isCommandsChatCommandEnabled()

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
