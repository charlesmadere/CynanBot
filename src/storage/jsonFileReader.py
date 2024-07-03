import json
import os
from typing import Any

import aiofiles
import aiofiles.ospath

from .jsonReaderInterface import JsonReaderInterface
from ..misc import utils as utils


class JsonFileReader(JsonReaderInterface):

    def __init__(self, fileName: str):
        if not utils.isValidStr(fileName):
            raise TypeError(f'fileName argument is malformed: \"{fileName}\"')

        self.__fileName: str = fileName

    def deleteFile(self):
        if self.fileExists():
            os.remove(self.__fileName)

    async def deleteFileAsync(self):
        if await self.fileExistsAsync():
            os.remove(self.__fileName)

    def fileExists(self) -> bool:
        return os.path.exists(self.__fileName)

    async def fileExistsAsync(self) -> bool:
        return await aiofiles.ospath.exists(self.__fileName)

    def readJson(self) -> dict[Any, Any] | None:
        if not self.fileExists():
            raise FileNotFoundError(f'File not found: \"{self.__fileName}\"')

        jsonContents: dict[Any, Any] | None = None

        with open(self.__fileName, mode = 'r', encoding = 'utf-8') as file:
            jsonContents = json.load(file)

        return jsonContents

    async def readJsonAsync(self) -> dict[Any, Any] | None:
        if not await self.fileExistsAsync():
            raise FileNotFoundError(f'File not found: \"{self.__fileName}\"')

        jsonContents: dict[Any, Any] | None = None

        async with aiofiles.open(
            file = self.__fileName,
            mode = 'r',
            encoding = 'utf-8'
        ) as file:
            data = await file.read()
            jsonContents = json.loads(data)

        return jsonContents

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'fileName': self.__fileName
        }
