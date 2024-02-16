import json
import os
from typing import Any, Dict, Optional

import aiofiles
import aiofiles.ospath

import CynanBot.misc.utils as utils
from CynanBot.storage.jsonReaderInterface import JsonReaderInterface


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

    def readJson(self) -> Optional[Dict[Any, Any]]:
        if not self.fileExists():
            raise FileNotFoundError(f'File not found: \"{self.__fileName}\"')

        jsonContents: Optional[Dict[Any, Any]] = None

        with open(self.__fileName, mode = 'r', encoding = 'utf-8') as file:
            jsonContents = json.load(file)

        return jsonContents

    async def readJsonAsync(self) -> Optional[Dict[Any, Any]]:
        if not await self.fileExistsAsync():
            raise FileNotFoundError(f'File not found: \"{self.__fileName}\"')

        jsonContents: Optional[Dict[Any, Any]] = None

        async with aiofiles.open(self.__fileName, mode = 'r', encoding = 'utf-8') as file:
            data = await file.read()
            jsonContents = json.loads(data)

        return jsonContents

    def __str__(self) -> str:
        return f'fileName=\"{self.__fileName}\"'
