import json
import os
from typing import Any, Dict, Optional

import aiofiles
import aiofiles.ospath
import CynanBotCommon.utils as utils

from persistence.authRepositorySnapshot import AuthRepositorySnapshot


class AuthRepository():

    def __init__(
        self,
        authFile: str = 'persistence/authRepository.json'
    ):
        if not utils.isValidStr(authFile):
            raise ValueError(f'authFile argument is malformed: \"{authFile}\"')

        self.__authFile: str = authFile

        self.__cache: Optional[Dict[str, Any]] = None

    async def clearCaches(self):
        self.__cache = None

    def getAll(self) -> AuthRepositorySnapshot:
        jsonContents = self.__readJson()
        return AuthRepositorySnapshot(jsonContents, self.__authFile)

    async def getAllAsync(self) -> AuthRepositorySnapshot:
        jsonContents = await self.__readJsonAsync()
        return AuthRepositorySnapshot(jsonContents, self.__authFile)

    def __readJson(self) -> Dict[str, object]:
        if self.__cache:
            return self.__cache

        if not os.path.exists(self.__authFile):
            raise FileNotFoundError(f'Auth Repository file not found: \"{self.__authFile}\"')

        with open(self.__authFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents is None:
            raise IOError(f'Error reading from Auth Repository file: \"{self.__authFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of Auth Repository file \"{self.__authFile}\" is empty')

        self.__cache = jsonContents
        return jsonContents

    async def __readJsonAsync(self) -> Dict[str, object]:
        if self.__cache:
            return self.__cache

        if not await aiofiles.ospath.exists(self.__authFile):
            raise FileNotFoundError(f'Auth Repository file not found: \"{self.__authFile}\"')

        async with aiofiles.open(self.__authFile, mode = 'r') as file:
            data = await file.read()
            jsonContents = json.loads(data)

        if jsonContents is None:
            raise IOError(f'Error reading from Auth Repository file: \"{self.__authFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of Auth Repository file \"{self.__authFile}\" is empty')

        self.__cache = jsonContents
        return jsonContents
