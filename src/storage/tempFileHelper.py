import re
import uuid
from asyncio import AbstractEventLoop
from typing import Pattern

import aiofiles
import aiofiles.os
import aiofiles.ospath
from frozenlist import FrozenList

from .tempFileHelperInterface import TempFileHelperInterface
from ..misc import utils as utils


class TempFileHelper(TempFileHelperInterface):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        directory: str = '../temp'
    ):
        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not utils.isValidStr(directory):
            raise TypeError(f'directory argument is malformed: \"{directory}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__directory: str = directory

        self.__fileNameRegEx: Pattern = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def __generateFileName(self, prefix: str, extension: str) -> str:
        randomUuid = self.__fileNameRegEx.sub('', str(uuid.uuid4()))
        fileName = f'{self.__directory}/{prefix}-{randomUuid}.{extension}'.casefold()
        return utils.cleanPath(fileName)

    async def getTempFileName(
        self,
        prefix: str,
        extension: str
    ) -> str:
        if not utils.isValidStr(prefix):
            raise TypeError(f'prefix argument is malformed: \"{prefix}\"')
        elif not utils.isValidStr(extension):
            raise TypeError(f'extension argument is malformed: \"{extension}\"')

        fileNames = await self.getTempFileNames(
            prefix = prefix,
            extension = extension,
            amount = 1
        )

        return fileNames[0]

    async def getTempFileNames(
        self,
        amount: int,
        prefix: str,
        extension: str
    ) -> FrozenList[str]:
        if not utils.isValidInt(amount):
            raise TypeError(f'amount argument is malformed: \"{amount}\"')
        elif amount < 1 or amount > utils.getIntMaxSafeSize():
            raise ValueError(f'amount argument is malformed: {amount}')
        elif not utils.isValidStr(prefix):
            raise TypeError(f'prefix argument is malformed: \"{prefix}\"')
        elif not utils.isValidStr(extension):
            raise TypeError(f'extension argument is malformed: \"{extension}\"')

        directory = utils.cleanPath(self.__directory)

        if not await aiofiles.ospath.exists(
            path = directory,
            loop = self.__eventLoop
        ):
            await aiofiles.os.makedirs(
                name = directory,
                loop = self.__eventLoop
            )

        fileNames: set[str] = set()

        while len(fileNames) < amount:
            newFileName = await self.__generateFileName(
                prefix = prefix,
                extension = extension
            )

            if not await aiofiles.ospath.exists(newFileName):
                fileNames.add(newFileName)

        frozenFileNames: FrozenList[str] = FrozenList(fileNames)
        frozenFileNames.freeze()

        return frozenFileNames
