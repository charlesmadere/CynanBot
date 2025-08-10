import json
import os
from asyncio import AbstractEventLoop
from typing import Any, Final

import aiofiles
import aiofiles.ospath

from .jsonReaderInterface import JsonReaderInterface
from ..misc import utils as utils


class JsonFileReader(JsonReaderInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        fileName: str,
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not utils.isValidStr(fileName):
            raise TypeError(f'fileName argument is malformed: \"{fileName}\"')

        self.__eventLoop: Final[AbstractEventLoop] = eventLoop
        self.__fileName: Final[str] = fileName

    def deleteFile(self):
        if self.fileExists():
            os.remove(self.__fileName)

    async def deleteFileAsync(self):
        if await self.fileExistsAsync():
            os.remove(self.__fileName)

    def fileExists(self) -> bool:
        return os.path.exists(self.__fileName)

    async def fileExistsAsync(self) -> bool:
        return await aiofiles.ospath.exists(
            path = self.__fileName,
            loop = self.__eventLoop,
        )

    @property
    def fileName(self) -> str:
        return self.__fileName

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
            encoding = 'utf-8',
            loop = self.__eventLoop,
        ) as file:
            data = await file.read()
            jsonContents = json.loads(data)

        return jsonContents

    def __repr__(self) -> str:
        return self.__fileName
