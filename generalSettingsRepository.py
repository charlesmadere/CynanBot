from typing import Any, Dict, Optional

from CynanBotCommon.storage.jsonReaderInterface import JsonReaderInterface
from generalSettingsRepositorySnapshot import GeneralSettingsRepositorySnapshot


class GeneralSettingsRepository():

    def __init__(self, settingsJsonReader: JsonReaderInterface):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise ValueError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader

        self.__cache: Optional[GeneralSettingsRepositorySnapshot] = None

    async def clearCaches(self):
        self.__cache = None

    async def getAdministrator(self) -> str:
        snapshot = await self.getAllAsync()
        return snapshot.requireAdministrator()

    def getAll(self) -> GeneralSettingsRepositorySnapshot:
        if self.__cache is not None:
            return self.__cache

        jsonContents = self.__readJson()
        snapshot = GeneralSettingsRepositorySnapshot(jsonContents)
        self.__cache = snapshot

        return snapshot

    async def getAllAsync(self) -> GeneralSettingsRepositorySnapshot:
        if self.__cache is not None:
            return self.__cache

        jsonContents = await self.__readJsonAsync()
        snapshot = GeneralSettingsRepositorySnapshot(jsonContents)
        self.__cache = snapshot

        return snapshot

    def __readJson(self) -> Dict[str, Any]:
        if not self.__settingsJsonReader.fileExists():
            raise FileNotFoundError(f'General Settings file not found: \"{self.__settingsJsonReader}\"')

        jsonContents = self.__settingsJsonReader.readJson()

        if jsonContents is None:
            raise IOError(f'Error reading from General Settings file: \"{self.__settingsJsonReader}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of General Settings file \"{self.__settingsJsonReader}\" is empty')

        return jsonContents

    async def __readJsonAsync(self) -> Dict[str, Any]:
        if not await self.__settingsJsonReader.fileExistsAsync():
            raise FileNotFoundError(f'General Settings file not found: \"{self.__settingsJsonReader}\"')

        jsonContents = await self.__settingsJsonReader.readJsonAsync()

        if jsonContents is None:
            raise IOError(f'Error reading from General Settings file: \"{self.__settingsJsonReader}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of General Settings file \"{self.__settingsJsonReader}\" is empty')

        return jsonContents
