import json
import os
from typing import Any, Dict, Optional

import aiofiles
import aiofiles.ospath

import CynanBotCommon.utils as utils
from generalSettingsSnapshot import GeneralSettingsSnapshot


class GeneralSettingsRepository():

    def __init__(
        self,
        generalSettingsFile: str = 'generalSettingsRepository.json'
    ):
        if not utils.isValidStr(generalSettingsFile):
            raise ValueError(f'generalSettingsFile argument is malformed: \"{generalSettingsFile}\"')

        self.__generalSettingsFile: str = generalSettingsFile
        self.__cache: Optional[Dict[str, Any]] = None

    async def clearCaches(self):
        self.__cache = None

    def getAll(self) -> GeneralSettingsSnapshot:
        jsonContents = self.__readJson()
        return GeneralSettingsSnapshot(jsonContents, self.__generalSettingsFile)

    async def getAllAsync(self) -> GeneralSettingsSnapshot:
        jsonContents = await self.__readJsonAsync()
        return GeneralSettingsSnapshot(jsonContents, self.__generalSettingsFile)

    def __readJson(self) -> Dict[str, Any]:
        if self.__cache:
            return self.__cache

        if not os.path.exists(self.__generalSettingsFile):
            raise FileNotFoundError(f'General Settings file not found: \"{self.__generalSettingsFile}\"')

        with open(self.__generalSettingsFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents is None:
            raise IOError(f'Error reading from General Settings file: \"{self.__generalSettingsFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of General Settings file \"{self.__generalSettingsFile}\" is empty')

        self.__cache = jsonContents
        return jsonContents

    async def __readJsonAsync(self) -> Dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        if not await aiofiles.ospath.exists(self.__generalSettingsFile):
            raise FileNotFoundError(f'General Settings file not found: \"{self.__generalSettingsFile}\"')

        async with aiofiles.open(self.__generalSettingsFile, mode = 'r') as file:
            data = await file.read()
            jsonContents = json.loads(data)

        if jsonContents is None:
            raise IOError(f'Error reading from General Settings file: \"{self.__generalSettingsFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of General Settings file \"{self.__generalSettingsFile}\" is empty')

        self.__cache = jsonContents
        return jsonContents
