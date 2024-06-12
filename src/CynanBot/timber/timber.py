import asyncio
import queue
from collections import defaultdict
from queue import SimpleQueue

import aiofiles
import aiofiles.os
import aiofiles.ospath

from CynanBot.misc.simpleDateTime import SimpleDateTime
import CynanBot.misc.utils as utils
from CynanBot.misc.backgroundTaskHelperInterface import \
    BackgroundTaskHelperInterface
from CynanBot.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface
from CynanBot.timber.timberEntry import TimberEntry
from CynanBot.timber.timberInterface import TimberInterface


class Timber(TimberInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        sleepTimeSeconds: float = 15,
        timberRootDirectory: str = 'logs/timber'
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not utils.isValidNum(sleepTimeSeconds):
            raise TypeError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        elif sleepTimeSeconds < 1 or sleepTimeSeconds > 60:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')
        elif not utils.isValidStr(timberRootDirectory):
            raise TypeError(f'timberRootDirectory argument is malformed: \"{timberRootDirectory}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__sleepTimeSeconds: float = sleepTimeSeconds
        self.__timberRootDirectory: str = timberRootDirectory

        self.__isStarted: bool = False
        self.__entryQueue: SimpleQueue[TimberEntry] = SimpleQueue()

    def __getErrorStatement(self, ensureNewLine: bool, timberEntry: TimberEntry) -> str | None:
        if not utils.isValidBool(ensureNewLine):
            raise TypeError(f'ensureNewLine argument is malformed: \"{ensureNewLine}\"')
        elif not isinstance(timberEntry, TimberEntry):
            raise TypeError(f'timberEntry argument is malformed: \"{timberEntry}\"')

        if timberEntry.exception is None:
            return None

        errorStatement = str(timberEntry.exception)

        if utils.isValidStr(timberEntry.traceback):
            errorStatement = f'{errorStatement}\n{timberEntry.traceback}'.strip()

        if ensureNewLine:
            errorStatement = f'{errorStatement}\n'

        return errorStatement

    def __getLogStatement(self, ensureNewLine: bool, timberEntry: TimberEntry) -> str:
        if not utils.isValidBool(ensureNewLine):
            raise TypeError(f'ensureNewLine argument is malformed: \"{ensureNewLine}\"')
        elif not isinstance(timberEntry, TimberEntry):
            raise TypeError(f'timberEntry argument is malformed: \"{timberEntry}\"')

        logStatement = f'{timberEntry.logTime.getDateAndTimeStr(True)} — {timberEntry.tag} — {timberEntry.msg}'.strip()

        if utils.isValidStr(timberEntry.traceback):
            logStatement = f'{logStatement}\n{timberEntry.traceback}'.strip()

        if ensureNewLine:
            logStatement = f'{logStatement}\n'

        return logStatement

    def log(
        self,
        tag: str,
        msg: str,
        exception: Exception | None = None,
        traceback: str | None = None
    ):
        if not utils.isValidStr(tag):
            raise TypeError(f'tag argument is malformed: \"{tag}\"')
        elif not utils.isValidStr(msg):
            raise TypeError(f'msg argument is malformed: \"{msg}\"')
        elif exception is not None and not isinstance(exception, Exception):
            raise TypeError(f'exception argument is malformed: \"{exception}\"')
        elif traceback is not None and not isinstance(traceback, str):
            raise TypeError(f'traceback argument is malformed: \"{traceback}\"')

        logTime = SimpleDateTime(
            timeZone = self.__timeZoneRepository.getDefault()
        )

        timberEntry = TimberEntry(
            exception = exception,
            logTime = logTime,
            msg = msg,
            tag = tag,
            traceback = traceback
        )

        self.__entryQueue.put(timberEntry)
        print(self.__getLogStatement(False, timberEntry))

    def start(self):
        if self.__isStarted:
            self.log('Timber', 'Not starting Timber as it has already been started')
            return

        self.__isStarted = True
        self.__backgroundTaskHelper.createTask(self.__startEventLoop())

    async def __startEventLoop(self):
        while True:
            entries: list[TimberEntry] = list()

            try:
                while not self.__entryQueue.empty():
                    entry = self.__entryQueue.get_nowait()
                    entries.append(entry)
            except queue.Empty:
                pass

            await self.__writeToLogFiles(entries)
            await asyncio.sleep(self.__sleepTimeSeconds)

    async def __writeToLogFiles(self, entries: list[TimberEntry]):
        if len(entries) == 0:
            return

        # The logic below is kind of intense, but we do this in order to favor logical complexity
        # in exchange for I/O simplicity. By doing things this way, we only need to attempt to
        # create folders once, files once, and we also just open a file handle one time too.

        # This dictionary stores a directory, and then a list of files, and then the contents to
        # write into the files themselves. This dictionary does not make any attempt at handling
        # error logging.
        structure: dict[str, dict[str, list[TimberEntry]]] = defaultdict(lambda: defaultdict(lambda: list()))

        # This dictionary is used for error logging, and just like the dictionary above, stores
        # a directory, and then a list of files, and then the contents to write into the files
        # themselves.
        errorStructure: dict[str, dict[str, list[TimberEntry]]] = defaultdict(lambda: defaultdict(lambda: list()))

        for entry in entries:
            logTime = entry.logTime
            timberDirectory = f'{self.__timberRootDirectory}/{logTime.getYearStr()}/{logTime.getMonthStr()}'
            timberFile = f'{timberDirectory}/{logTime.getDayStr()}.log'
            structure[timberDirectory][timberFile].append(entry)

            if entry.exception is not None:
                timberErrorDirectory = f'{timberDirectory}/errors'
                timberErrorFile = f'{timberErrorDirectory}/{logTime.getDayStr()}.log'
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
