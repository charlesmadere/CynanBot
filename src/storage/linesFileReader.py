import os
from asyncio import AbstractEventLoop
from typing import Final

import aiofiles
import aiofiles.ospath

from .linesReaderInterface import LinesReaderInterface
from ..misc import utils as utils


class LinesFileReader(LinesReaderInterface):

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

    @property
    def fileName(self) -> str:
        return self.__fileName

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

        async with aiofiles.open(
            file = self.__fileName,
            mode = 'r',
            encoding = 'utf-8',
            loop = self.__eventLoop,
        ) as file:
            lines = await file.readlines()

        return lines

    def __repr__(self) -> str:
        return self.__fileName
