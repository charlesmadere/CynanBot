import os

import aiofiles
import aiofiles.ospath

import CynanBot.misc.utils as utils
from CynanBot.storage.linesReaderInterface import LinesReaderInterface


class LinesFileReader(LinesReaderInterface):

    def __init__(self, fileName: str):
        if not utils.isValidStr(fileName):
            raise TypeError(f'fileName argument is malformed: \"{fileName}\"')

        self.__fileName: str = fileName

    def readLines(self) -> list[str] | None:
        if not os.path.exists(self.__fileName):
            raise FileNotFoundError(f'File not found: \"{self.__fileName}\"')

        lines: list[str] | None = None

        with open(self.__fileName, mode = 'r', encoding = 'utf-8') as file:
            lines = file.readlines()

        return lines

    async def readLinesAsync(self) -> list[str] | None:
        if not await aiofiles.ospath.exists(self.__fileName):
            raise FileNotFoundError(f'File not found: \"{self.__fileName}\"')

        lines: list[str] | None = None

        async with aiofiles.open(self.__fileName, mode = 'r', encoding = 'utf-8') as file:
            lines = await file.readlines()

        return lines
