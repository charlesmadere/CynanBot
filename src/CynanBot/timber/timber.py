import asyncio
import queue
from collections import defaultdict
from queue import SimpleQueue
from typing import Dict, List, Optional

import aiofiles
import aiofiles.os
import aiofiles.ospath

import CynanBot.misc.utils as utils
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.timber.timberEntry import TimberEntry
from CynanBot.timber.timberInterface import TimberInterface


class Timber(TimberInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelper,
        sleepTimeSeconds: float = 15,
        timberRootDirectory: str = 'logs/timber'
    ):
        assert isinstance(backgroundTaskHelper, BackgroundTaskHelper), f"malformed {backgroundTaskHelper=}"
        if not utils.isValidNum(sleepTimeSeconds):
            raise ValueError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        if sleepTimeSeconds < 1 or sleepTimeSeconds > 60:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')
        if not utils.isValidStr(timberRootDirectory):
            raise ValueError(f'timberRootDirectory argument is malformed: \"{timberRootDirectory}\"')

        self.__sleepTimeSeconds: float = sleepTimeSeconds
        self.__timberRootDirectory: str = timberRootDirectory

        self.__entryQueue: SimpleQueue[TimberEntry] = SimpleQueue()
        backgroundTaskHelper.createTask(self.__startEventLoop())

    def __getErrorStatement(self, ensureNewLine: bool, timberEntry: TimberEntry) -> Optional[str]:
        if not utils.isValidBool(ensureNewLine):
            raise ValueError(f'ensureNewLine argument is malformed: \"{ensureNewLine}\"')
        assert isinstance(timberEntry, TimberEntry), f"malformed {timberEntry=}"

        if not timberEntry.hasException():
            return None

        errorStatement = f'{timberEntry.getException()}'

        if timberEntry.hasTraceback():
            errorStatement = f'{errorStatement}\n{timberEntry.getTraceback()}'.strip()

        if ensureNewLine:
            errorStatement = f'{errorStatement}\n'

        return errorStatement

    def __getLogStatement(self, ensureNewLine: bool, timberEntry: TimberEntry) -> str:
        if not utils.isValidBool(ensureNewLine):
            raise ValueError(f'ensureNewLine argument is malformed: \"{ensureNewLine}\"')
        assert isinstance(timberEntry, TimberEntry), f"malformed {timberEntry=}"

        logStatement = f'{timberEntry.getSimpleDateTime().getDateAndTimeStr(True)} — {timberEntry.getTag()} — {timberEntry.getMsg()}'.strip()

        if timberEntry.hasTraceback():
            logStatement = f'{logStatement}\n{timberEntry.getTraceback()}'.strip()

        if ensureNewLine:
            logStatement = f'{logStatement}\n'

        return logStatement

    def log(
        self,
        tag: str,
        msg: str,
        exception: Optional[Exception] = None,
        traceback: Optional[str] = None
    ):
        if not utils.isValidStr(tag):
            raise ValueError(f'tag argument is malformed: \"{tag}\"')
        if not utils.isValidStr(msg):
            raise ValueError(f'msg argument is malformed: \"{msg}\"')
        assert exception is None or isinstance(exception, Exception), f"malformed {exception=}"
        assert traceback is None or isinstance(traceback, str), f"malformed {traceback=}"

        timberEntry = TimberEntry(
            tag = tag,
            msg = msg,
            exception = exception,
            traceback = traceback
        )

        self.__entryQueue.put(timberEntry)
        print(self.__getLogStatement(False, timberEntry))

    async def __startEventLoop(self):
        while True:
            entries: List[TimberEntry] = list()

            try:
                while not self.__entryQueue.empty():
                    entry = self.__entryQueue.get_nowait()
                    entries.append(entry)
            except queue.Empty:
                pass

            await self.__writeToLogFiles(entries)
            await asyncio.sleep(self.__sleepTimeSeconds)

    async def __writeToLogFiles(self, entries: List[TimberEntry]):
        if len(entries) == 0:
            return

        # The logic below is kind of intense, but we do this in order to favor logical complexity
        # in exchange for I/O simplicity. By doing things this way, we only need to attempt to
        # create folders once, files once, and we also just open a file handle one time too.

        # This dictionary stores a directory, and then a list of files, and then the contents to
        # write into the files themselves. This dictionary does not make any attempt at handling
        # error logging.
        structure: Dict[str, Dict[str, List[TimberEntry]]] = defaultdict(lambda: defaultdict(lambda: list()))

        # This dictionary is used for error logging, and just like the dictionary above, stores
        # a directory, and then a list of files, and then the contents to write into the files
        # themselves.
        errorStructure: Dict[str, Dict[str, List[TimberEntry]]] = defaultdict(lambda: defaultdict(lambda: list()))

        for entry in entries:
            simpleDateTime = entry.getSimpleDateTime()
            timberDirectory = f'{self.__timberRootDirectory}/{simpleDateTime.getYearStr()}/{simpleDateTime.getMonthStr()}'
            timberFile = f'{timberDirectory}/{simpleDateTime.getDayStr()}.log'
            structure[timberDirectory][timberFile].append(entry)

            if entry.hasException():
                timberErrorDirectory = f'{timberDirectory}/errors'
                timberErrorFile = f'{timberErrorDirectory}/{simpleDateTime.getDayStr()}.log'
                errorStructure[timberErrorDirectory][timberErrorFile].append(entry)

        for timberDirectory, timberFileToEntriesDict in structure.items():
            if not await aiofiles.ospath.exists(timberDirectory):
                await aiofiles.os.makedirs(timberDirectory)

            for timberFile, entriesList in timberFileToEntriesDict.items():
                async with aiofiles.open(timberFile, mode = 'a', encoding = 'utf-8') as file:
                    for entry in entriesList:
                        logStatement = self.__getLogStatement(True, entry)
                        await file.write(logStatement)

        for timberErrorDirectory, timberErrorFileToEntriesDict in errorStructure.items():
            if not await aiofiles.ospath.exists(timberErrorDirectory):
                await aiofiles.os.makedirs(timberErrorDirectory)

            for timberErrorFile, entriesList in timberErrorFileToEntriesDict.items():
                async with aiofiles.open(timberErrorFile, mode = 'a', encoding = 'utf-8') as file:
                    for entry in entriesList:
                        errorStatement = self.__getErrorStatement(True, entry)

                        if utils.isValidStr(errorStatement):
                            await file.write(errorStatement)
